from resume_enhancer.src.elements.resume_education import Education
from resume_enhancer.src.elements.resume_experience import Experience
from resume_enhancer.src.elements.resume_project import Project
from resume_enhancer.src.elements.resume_skill import Skill
from resume_enhancer.src.elements.resume_contact import Contact
from resume_enhancer.src.elements.resume_personal import Personal
from resume_enhancer.src.sections.resume_section import Section


from resume_enhancer.src.constants.resume_constants import RESUME_ELEMENTS_ORDER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from resume_enhancer.src.constants.resume_constants import NAME_PARAGRAPH_STYLE, CONTACT_PARAGRAPH_STYLE
from resume_enhancer.src.constants import FULL_COLUMN_WIDTH
import json
import os
import configparser


def get_education_element(element) -> Education:
    e = Education()
    e.set_institution(element['institution'])
    e.set_course(element['course'])
    e.set_location(element['location'])
    e.set_start_date(element['start_date'])
    e.set_end_date(element['end_date'])
    return e

def get_contact_element(element) -> Contact:
    e = Contact()
    e.set_email(element['email'])
    e.set_phone(element['phone'])
    e.set_location(element['location'])
    e.set_linkedIn(element.get('linkedIn', ''))
    e.set_github(element.get('github', ''))
    return e

def get_experience_element(element) -> Experience:
    e = Experience()
    e.set_company(element['company'])
    e.set_title(element['title'])
    e.set_location(element['location'])
    e.set_start_date(element['start_date'])
    e.set_end_date(element['end_date'])
    e.set_description(element['description'])
    return e

def get_project_element(element) -> Project:
    e = Project()
    e.set_title(element['title'])
    e.set_description(element['description'])
    e.set_link(element['link'])
    return e

def get_skills_element(element) -> Skill:
    e = Skill()
    e.set_title(element['title'])
    e.set_elements(element['elements'])
    return e
def get_personal_element(element) -> Personal:
    e = Personal()
    e.set_name(element['name'])
    e.set_about(element['about'])
    return e
def generate_resume(output_file_path, author, elements, table_styles) -> None:
    resume_doc = SimpleDocTemplate(
        output_file_path,
        pagesize=A4,
        showBoundary=0,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.2 * inch,
        bottomMargin=0.1 * inch,
        title=f"Resume of {author}",
        author=author
    )
    table = Table(elements, colWidths=[FULL_COLUMN_WIDTH * 0.7, FULL_COLUMN_WIDTH * 0.3], spaceBefore=0, spaceAfter=0)
    table.setStyle(TableStyle(table_styles))
    resume_elements = [table]
    resume_doc.build(resume_elements)


def generate_resume_from_json(enhance_json):
    # Load data from JSON
    # file_path = 'resume_enhancer/src/data/input.json'
    # with open(file_path, 'r') as file:
    #     data = json.load(file)
    data=enhance_json
    # Personal and Contact details now come from JSON
    author = data['personal'][0]['name']
    email = data['contact'][0]['email']
    phone = data['contact'][0]['phone']
    address = data['contact'][0]['location']
    linkedin = data['contact'][0]['linkedin']
    github = data['contact'][0]['github']

    OUTPUT_PDF_PATH = f"./{author.lower().replace(' ', '_')}_resume.pdf"
    
    education_elements = []
    experience_elements = []
    project_elements = []
    skill_elements = []
    profile_elements = []
    contact_elements = []

    for element in data['education']:
        education_elements.append(get_education_element(element))
        
    for element in data['experience']:
        experience_elements.append(get_experience_element(element))
        
    for element in data['projects']:
        project_elements.append(get_project_element(element))
        
    for element in data['skills']:
        skill_elements.append(get_skills_element(element))

    for element in data['personal']:
        profile_elements.append(get_personal_element(element))

    for element in data['contact']:
        contact_elements.append(get_contact_element(element))

    resume_data = {
        'education': Section('Education', education_elements),
        'profile': Section('Profile', profile_elements),
        'experience': Section('Experience', experience_elements),
        'projects': Section('Projects', project_elements),
        'skills': Section('Skills', skill_elements),
        'contact': Section('Contact', contact_elements),
    }
    
    table = []
    running_row_index = [0]
    table_styles = [
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, running_row_index[0]), (1, running_row_index[0]), 6)
    ]
    
    # Add header info (Name, Contact)
    table.append([
        Paragraph(author, NAME_PARAGRAPH_STYLE)
    ])
    running_row_index[0] += 1
    contact_info = (
    f'<a href="mailto:{email}">{email}</a> | '
    f'{phone} | {address} | '
    f'<a href="{linkedin}" color="blue">{linkedin}</a> | '
    f'<a href="{github}" color="blue">{github}</a>'
)
    table.append([Paragraph(contact_info, CONTACT_PARAGRAPH_STYLE)])
    table_styles.append(('BOTTOMPADDING', (0, running_row_index[0]), (1, running_row_index[0]), 1))
    running_row_index[0] += 1
    
    for element in RESUME_ELEMENTS_ORDER:
        if element in resume_data:
            section_table = resume_data[element].get_section_table(running_row_index, table_styles)
            for entry in section_table:
                table.append(entry)
    
    print("Building resume...")
    generate_resume(OUTPUT_PDF_PATH, author, table, table_styles)
    # pdf.save(OUTPUT_PDF_PATH)
    return OUTPUT_PDF_PATH
    # print(f"Resume generated at {OUTPUT_PDF_PATH}")