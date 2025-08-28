import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    Image, ListFlowable, ListItem, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab import rl_config
from reportlab.lib import colors

# =====================================================================
# CONFIGURATION SECTION - Styling
# =====================================================================
CONFIG = {
    'default_encoding': 'utf8',
    'fonts': {
        'primary': 'Segoe UI Emoji',
        'primary_path': r'fonts\Segoe UI Emoji.TTF',
        'heading': 'arialrounded',
        'heading_path': r'fonts\arialroundedmtbold.ttf',
        'alternative': 'Helvetica',
        'code': 'Courier',
    },
    'colors': {
        'heading1': colors.darkblue,
        'heading2': colors.darkblue,
        'heading3': colors.black,
        'heading4': colors.black,
        'body_text': colors.black,
        'blockquote': colors.gray,
        'horizontal_rule': colors.black,
        'bullet': 'midnightblue',
    },
    'font_sizes': {
        'heading1': 48,
        'heading2': 24,
        'heading3': 18,
        'heading4': 16,
        'body_text': 14,
        'blockquote': 16,
        'bullet': 16,
        'ordered_bullet': 12,
        'table_header': 12,
        'table_cell': 10,
    },
    'leading': {
        'heading1': 50,
        'heading2': 25,
        'heading3': 22,
        'heading4': 20,
        'body_text': 17,
    },
    'spacing': {
        'heading1_after': 18,
        'heading2_after': 14,
        'heading3_after': 12,
        'heading4_after': 10,
        'paragraph_after': 8,
        'blockquote_after': 6,
        'list_after': 10,
        'horizontal_rule_before': 6,
        'horizontal_rule_after': 6,
    },
    'indentation': {
        'blockquote_left': 20,
        'blockquote_right': 10,
        'list_left_base': 20,
    },
    'alignment': {
        'heading1': TA_CENTER,
        'body': TA_LEFT,
        'blockquote': TA_LEFT,
    },
    'table': {
        'padding': 6,
        'header_bottom_padding': 8,
    },
}

# =================================================================
# Register Fonts
# =================================================================
rl_config.defaultEncoding = CONFIG['default_encoding']
try:
    pdfmetrics.registerFont(TTFont(CONFIG['fonts']['primary'], CONFIG['fonts']['primary_path']))
    pdfmetrics.registerFont(TTFont(CONFIG['fonts']['heading'], CONFIG['fonts']['heading_path']))
except:
    print(f"Warning: Could not register custom fonts. Using fallback font: {CONFIG['fonts']['alternative']}")

# =================================================================
# PDF Generator Class
# =================================================================
class PDFGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.story = []
        self.styles = getSampleStyleSheet()
        self.initialize_styles()

    def initialize_styles(self):
        primary_font = CONFIG['fonts']['primary'] if CONFIG['fonts']['primary'] in pdfmetrics.getRegisteredFontNames() else CONFIG['fonts']['alternative']
        heading_font = CONFIG['fonts']['heading'] if CONFIG['fonts']['heading'] in pdfmetrics.getRegisteredFontNames() else CONFIG['fonts']['alternative']

        self.heading_styles = {
            1: ParagraphStyle(
                name='Heading1', parent=self.styles['Heading1'], fontSize=CONFIG['font_sizes']['heading1'],
                textColor=CONFIG['colors']['heading1'], leading=CONFIG['leading']['heading1'],
                spaceAfter=CONFIG['spacing']['heading1_after'], alignment=CONFIG['alignment']['heading1'], fontName=heading_font
            ),
            2: ParagraphStyle(
                name='Heading2', parent=self.styles['Heading2'], fontSize=CONFIG['font_sizes']['heading2'],
                textColor=CONFIG['colors']['heading2'], leading=CONFIG['leading']['heading2'],
                spaceAfter=CONFIG['spacing']['heading2_after'], fontName=primary_font
            ),
            3: ParagraphStyle(
                name='Heading3', parent=self.styles['Heading3'], fontSize=CONFIG['font_sizes']['heading3'],
                textColor=CONFIG['colors']['heading3'], leading=CONFIG['leading']['heading3'],
                spaceAfter=CONFIG['spacing']['heading3_after'], fontName=primary_font
            ),
            4: ParagraphStyle(
                name='Heading4', parent=self.styles['Normal'], fontSize=CONFIG['font_sizes']['heading4'],
                textColor=CONFIG['colors']['heading4'], leading=CONFIG['leading']['heading4'],
                spaceAfter=CONFIG['spacing']['heading4_after'], fontName=primary_font
            ),
        }

        self.body_style = ParagraphStyle(
            name='BodyText', parent=self.styles['BodyText'], fontSize=CONFIG['font_sizes']['body_text'],
            textColor=CONFIG['colors']['body_text'], leading=CONFIG['leading']['body_text'],
            alignment=CONFIG['alignment']['body'], fontName=primary_font
        )

        self.blockquote_style = ParagraphStyle(
            name='Blockquote', parent=self.styles['Normal'], fontSize=CONFIG['font_sizes']['blockquote'],
            textColor=CONFIG['colors']['blockquote'], leftIndent=CONFIG['indentation']['blockquote_left'],
            rightIndent=CONFIG['indentation']['blockquote_right'], alignment=CONFIG['alignment']['blockquote'],
            italic=True, spaceBefore=CONFIG['spacing']['blockquote_after'], spaceAfter=CONFIG['spacing']['blockquote_after'],
            fontName=primary_font
        )

    def add_horizontal_line(self):
        self.story.append(Spacer(1, CONFIG['spacing']['horizontal_rule_before']))
        self.story.append(HRFlowable(width="100%", thickness=1, color=CONFIG['colors']['horizontal_rule']))
        self.story.append(Spacer(1, CONFIG['spacing']['horizontal_rule_after']))

    def format_text(self, text):
        text = re.sub(r'`(.*?)`', f'<font face="{CONFIG["fonts"]["code"]}">\\1</font>', text)
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.*?)__', r'<b>\1</b>', text)
        text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)
        text = re.sub(r'~~(.+?)~~', r'<strike>\1</strike>', text)
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
        return text

    def break_page(self):
        self.story.append(PageBreak())

    def process_table_cell_content(self, cell_content):
        formatted_content = self.format_text(cell_content)
        return Paragraph(formatted_content, self.body_style)

    def parse_table(self, lines, start_index):
        """Parse markdown tables"""
        table_data = []
        alignment = []
        i = start_index

        # Header row
        if i < len(lines) and re.match(r'^\s*\|.*\|\s*$', lines[i]):
            row = lines[i].strip()
            cells = [cell.strip() for cell in row.strip('|').split('|')]
            header_cells = [self.process_table_cell_content(cell) for cell in cells]
            table_data.append(header_cells)
            i += 1
        else:
            return i  # Not a table

        # Separator row
        if i < len(lines) and re.match(r'^\s*\|[-:|. ]+\|\s*$', lines[i]):
            row = lines[i].strip()
            separator_cells = [cell.strip() for cell in row.strip('|').split('|')]

            for cell in separator_cells:
                if cell.startswith(':') and cell.endswith(':'):
                    alignment.append('CENTER')
                elif cell.endswith(':'):
                    alignment.append('RIGHT')
                else:
                    alignment.append('LEFT')
            i += 1
        else:
            alignment = ['LEFT'] * len(table_data[0])

        # Data rows
        while i < len(lines) and re.match(r'^\s*\|.*\|\s*$', lines[i]):
            row = lines[i].strip()
            cells = [cell.strip() for cell in row.strip('|').split('|')]
            processed_cells = [self.process_table_cell_content(cell) for cell in cells]
            table_data.append(processed_cells)
            i += 1

        if len(table_data) > 1:
            doc = SimpleDocTemplate(self.filename, pagesize=A4)
            available_width = doc.width * 0.95
            col_widths = [available_width / len(table_data[0])] * len(table_data[0])

            table = Table(table_data, colWidths=col_widths)
            style = [
                ('GRID', (0, 0), (-1, -1), 0.5, CONFIG['colors']['body_text']),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), CONFIG['colors']['heading3']),
                ('FONTNAME', (0, 0), (-1, 0), CONFIG['fonts']['primary']),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]
            for col_idx, align in enumerate(alignment):
                style.append(('ALIGN', (col_idx, 0), (col_idx, -1), align))

            table.setStyle(TableStyle(style))
            self.story.append(Spacer(1, CONFIG['spacing']['paragraph_after']))
            self.story.append(table)
            self.story.append(Spacer(1, CONFIG['spacing']['paragraph_after'] * 1.5))

        return i

    def parse_headings(self, line):
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            hashes, heading_text = heading_match.groups()
            level = len(hashes)
            style = self.heading_styles.get(level, self.body_style)
            formatted_heading = self.format_text(heading_text.strip())
            self.story.append(Paragraph(formatted_heading, style))
            self.story.append(Spacer(1, 12))
            return True
        return False

    def parse_blockquote(self, line):
        blockquote_match = re.match(r'^>\s?(.*)', line)
        if blockquote_match:
            quote_text = blockquote_match.group(1)
            formatted_text = self.format_text(quote_text.strip())
            self.story.append(Paragraph(formatted_text, self.blockquote_style))
            self.story.append(Spacer(1, CONFIG['spacing']['blockquote_after']))
            return True
        return False

    def parse_list(self, lines, start_index):
        def parse_list_level(lines, start_index, indent_level=0):
            items = []
            i = start_index
            indent_pattern = r'^\s{' + str(indent_level) + r'}'

            while i < len(lines):
                line = lines[i]
                if not re.match(indent_pattern, line):
                    break
                line = line[indent_level:].strip()

                match = re.match(r'^[-*+]\s+(.*)', line) or re.match(r'^\d+\.\s+(.*)', line)
                if not match:
                    break
                content = match.group(1).strip()
                parsed_paragraph = Paragraph(self.format_text(content), self.body_style)
                item = ListItem([parsed_paragraph], bulletColor=CONFIG['colors']['bullet'])
                items.append(item)
                i += 1

            if items:
                left_indent = CONFIG['indentation']['list_left_base'] + indent_level
                list_flowable = ListFlowable(
                    items,
                    bulletFontName=CONFIG['fonts']['primary'],
                    bulletFontSize=CONFIG['font_sizes']['bullet'],
                    leftIndent=left_indent,
                )
                return i, list_flowable
            return i, None

        next_index, list_flowable = parse_list_level(lines, start_index)
        if list_flowable:
            self.story.append(list_flowable)
            self.story.append(Spacer(1, CONFIG['spacing']['list_after']))
        return next_index

    def build_pdf(self, content):
        lines = content.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()

            if not line.strip():
                i += 1
                continue

            if self.parse_headings(line):
                i += 1
                continue

            if self.parse_blockquote(line):
                i += 1
                continue

            if line.startswith("|"):
                i = self.parse_table(lines, i)
                continue

            if re.match(r'^(\s*[-*+]|\s*\d+\.)\s+', line):
                i = self.parse_list(lines, i)
                continue

            formatted_text = self.format_text(line.strip())
            self.story.append(Paragraph(formatted_text, self.body_style))
            self.story.append(Spacer(1, CONFIG['spacing']['paragraph_after']))
            i += 1

        doc = SimpleDocTemplate(self.filename, pagesize=A4)
        doc.build(self.story)

# =================================================================
# Example usage
# =================================================================
def main():
    content = """
AGASTHYA OMKUMAR
+91 9844805398 ⋄ Bengaluru, KA
agsthya611@gmail.com ⋄ linkedin.com/in/agasthya-omkumar ⋄ github.com/AGasthya283

**OBJECTIVE**
Highly skilled ML Engineer with expertise in Machine Learning, Computer Vision and NLP. Leveraging research experience at CAIR‑DRDO and advanced training I am now seeking Data Scientist or AI‑related roles to drive impactful results in a dynamic organization.

**EDUCATION**
**Master’s** in Applied Mathematics, Defence Institute of Advanced Technology 2022 – 2024
Relevant Coursework: Advanced Statistical Techniques, Machine Learning, Deep Learning, Computer Vision
CGPA: 8.26

**Bachelor’s** in Mechanical Engineering, BNM Institute of Technology, VTU 2017 – 2021
CGPA: 8.34

**SKILLS**

*Technical Skills* Machine Learning, Computer Vision, Image Processing, OCR, NLP, Time‑Series Image Recognition, Multi‑Object Tracking, Spatial Data Analysis, GenAI, LLMs, Mathematical Modelling, Azure, AWS, LaTeX

*Programming Languages* Python, MATLAB, SQL, R, C#

*Libraries / Frameworks* NumPy, Pandas, Matplotlib, Scikit‑Learn, OpenCV, **PyTorch**, Streamlit, ultralytics, TensorFlow, NLTK, mmtrack, sqlite3, geopy, geopandas, geographiclib, Keras, fastdtw

*OS* Windows, Linux (Ubuntu)

*Other Skills* Corporate Communication, Leadership, Event Management, Critical Thinking

**EXPERIENCE**

*Project Trainee* Aug 2023 – Mar 2024
CAIR‑DRDO, Bengaluru, KA
- Conducted research on UAV‑based Multi‑Object Tracking in the maritime domain for surveillance and Search & Rescue operations.
- Developed tracking models for specific use‑cases with high accuracy, tackling problems like occlusion and re‑identification using sensor data and image‑recognition techniques respectively.
- Developed data‑fusion models for visual and sensor data to tackle occlusion and re‑identification challenges.
- Visualized model performance and metrics using frameworks like Streamlit.
- Trained models on standalone GPU systems and edge‑computing technology.

*Intern* Mar 2021 – Sept 2021
Cognizant, Bengaluru, KA
- Underwent .NET training.
- Up‑skilled in Python and SQL.
- Trained in SQL database design.

**PROJECTS**

*UAV‑based Maritime Multi‑Object Tracking – Master’s Thesis Project*
Conducted research on multi‑object tracking methods with a focus on integrating image‑recognition techniques. Performed experiments on various object‑detection models and object‑tracking models such as YOLO, transformer‑based detectors, Kalman‑filter‑based tracking algorithms, and spatio‑temporal transformers. Applied image‑recognition techniques to enhance object‑detection accuracy, particularly in challenging scenarios like occlusion and re‑identification. Developed novel tracking algorithms that utilized AIS data to improve maritime tracking. Additionally, created a Streamlit‑based GUI for visualizing model performance and facilitating ready‑to‑deploy solutions.

*Vittiya Anveshak*
Built a fund‑trail analysis tool implemented in a web‑based application using Flask and Machine Learning. Hidden Markov Models were implemented to generate fund trails on datasets generated using Gen AI (CTGAN). Project presented at KAVACH, Cybersecurity Hackathon organized by AICTE, MoE’s Innovation Cell, MHA, BPRD, I4C. Selected among the top 5 out of 3,900 teams nationwide.

*Sign Language Recognition from Videos*
Developed a sign‑language recognition model using a custom LRCN (Long‑Range Convolutional Network), integrating advanced image‑recognition techniques to effectively recognize and interpret sign‑language gestures. These techniques were crucial in accurately identifying and processing the visual features of each gesture, enabling seamless communication between the hearing‑impaired and others. Successfully trained and fine‑tuned the model, achieving a high accuracy rate in sign‑language gesture recognition.

*EDA on IBM HR Employee Attrition Data*
Conducted HR‑analytics exploratory data analysis (EDA) on the IBM HR Employee Attrition dataset, revealing that job roles, job satisfaction, and compensation significantly impact attrition rates, while factors such as education, experience, job involvement, and work‑life balance are closely associated with employee performance. Provided actionable insights to inform HR strategies for talent retention, employee‑satisfaction improvement, and organizational‑performance optimization.

**LEADERSHIP**

- **Head Volunteer**, International Conference on Data Management, Analytics and Innovation (ICD‑MAI) 2023: Led a team of 20+ volunteers to organize the 7th ICD‑MAI held at DIAT, Pune. Managed smooth functioning of paper presentations under different sections simultaneously. Coordinated with DIAT non‑technical staff and hostel staff and facilitated accommodation, food, and transport facilities for ICD‑MAI participants, chief guests, and other dignitaries.

- **Team Lead**, team “CHANAKYA” for “KAVACH” Cybersecurity Hackathon: Managed a team of 5 and got selected in the top 5 of 3,900 teams for the Grand Finale conducted at GL Bajaj Institute of Technology, Greater Noida.

- **Captain**, Chess team, BNMIT.

**EXTRA‑CURRICULAR ACTIVITIES**

- Actively contribute and maintain a GitHub profile, testing machine‑learning models and creating tutorial repositories for various applications involving computer vision and deep learning.

- Actively participate in chess competitions; represented DIAT in West Zoneals chess competitions and BNM Institute of Technology in VTU South Zoneals chess competition.

- Founded Robotics Club at BNM Institute of Technology: Conducted workshops and trained new members in Arduino, Raspberry Pi, and basic Internet of Things (IoT) projects.
"""
    output_pdf = "output.pdf"
    pdf_gen = PDFGenerator(output_pdf)
    pdf_gen.build_pdf(content)
    print(f"PDF successfully generated: {output_pdf}")

if __name__ == "__main__":
    main()
