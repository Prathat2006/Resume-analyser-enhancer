from resume_enhancer.formater import format_resume


resume_text=r"""
AGASTHYA OMKUMAR
About:
Data-driven Machine-Learning Engineer with experience building predictive models, data-fusion pipelines, and interactive dashboards; skilled in SEM, PPC, Google Analytics, Python, and visualization; passionate about applying analytical expertise to digital-marketing and campaign management.

Education:

M.Sc. Applied Mathematics – Defence Institute of Advanced Technology (DIAT) (2022–2024, CGPA 8.26)

B.E. Mechanical Engineering – BNM Institute of Technology (VTU) (2017–2021, CGPA 8.34)

Experience:

Project Trainee – Digital-Analytics & Computer-Vision, CAIR‑DRDO, Bengaluru (Aug 2023 – Mar 2024)

Intern – Software Development & Data Engineering, Cognizant, Bengaluru (Mar 2021 – Sep 2021)

Skills:

Digital Marketing: SEM, PPC, Google Ads, SEO, Keyword research, On-page optimisation, Email marketing, Social-media analytics, Content performance tracking, Campaign-budget monitoring, ROI analysis

Data & Analytics: Google Analytics, Tag Manager, Data visualisation (Streamlit, Tableau, Power BI), Marketing-operations reporting, KPI dashboards, Statistical modelling, Hypothesis testing

Programming & Tools: Python, SQL, R, MATLAB, Pandas, NumPy, Scikit-Learn, TensorFlow, PyTorch, REST APIs, Flask, FastAPI, Git, Docker, Azure, AWS, Linux (Ubuntu), Windows

Projects:

Fund-Trail Analysis & Predictive Modelling – Flask + ML web app with Hidden Markov Models and event tracking

Sign-Language Recognition (Computer-Vision) – Real-time LRCN model

HR Attrition Analytics – End-to-end exploratory data analysis on IBM HR dataset

Contact & Location:

Location: Bengaluru, Karnataka, India

Phone: +91 98765 43210

Email: agasthya.omkumar.mock@email.com

Links:

LinkedIn: https://linkedin.com/in/agasthya-omkumar

GitHub: https://github.com/AGasthya283

Other:

Certifications: Google Analytics for Beginners (2023), Fundamentals of Digital Marketing (2022)

Leadership: Head Volunteer – ICDMAI 2023, Team Lead – CHANAKYA Hackathon (Top‑5), Founder – Robotics Club

Languages: English (Professional proficiency), Hindi (Native)
"""
# print(resume_text)

print(format_resume(resume_text))