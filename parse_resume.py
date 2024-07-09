import re
import json

def parse_resume(resume_text):
    resume_json = {
        "personal_information": {
            "name": extract_name(resume_text),
            "email": extract_email(resume_text),
            "phone": extract_phone(resume_text),
            "address": extract_address(resume_text)
        },
        "professional_summary": extract_professional_summary(resume_text),
        "experience": extract_experience(resume_text),
        "education": extract_education(resume_text),
        "skills": extract_skills(resume_text),
        "certifications": extract_certifications(resume_text),
        "projects": extract_projects(resume_text),
        "languages": extract_languages(resume_text),
        "interests": extract_interests(resume_text)
    }
    return resume_json

def extract_name(text):
    name_pattern = re.compile(r'^([A-Z][a-z]*\s[A-Z][a-z]*)$', re.MULTILINE)
    match = name_pattern.search(text)
    return match.group(0) if match else None

def extract_email(text):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    match = email_pattern.search(text)
    return match.group(0) if match else None

def extract_phone(text):
    phone_pattern = re.compile(r'\+?\d[\d -]{8,12}\d')
    match = phone_pattern.search(text)
    return match.group(0) if match else None

def extract_address(text):
    address_pattern = re.compile(r'Address:\s*(.+)', re.IGNORECASE)
    match = address_pattern.search(text)
    return match.group(1).strip() if match else None

def extract_professional_summary(text):
    summary_pattern = re.compile(r'Professional Summary:\s*(.*?)\s*(Experience|Education|Skills|Certifications|Projects|Languages|Interests):', re.S)
    match = summary_pattern.search(text)
    return match.group(1).strip() if match else None

def extract_experience(text):
    experience_pattern = re.compile(r'Experience:\s*(.*?)\s*(Education|Skills|Certifications|Projects|Languages|Interests):', re.S)
    match = experience_pattern.search(text)
    if match:
        experiences = match.group(1).strip()
        experience_entries = experiences.split('\n\n')
        experience_list = []
        for entry in experience_entries:
            lines = entry.split('\n')
            if len(lines) >= 2:
                title_company = lines[0].split(',')
                job_title = title_company[0].strip()
                company = title_company[1].strip() if len(title_company) > 1 else ''
                date_location = lines[1].split(',')
                start_date = date_location[0].strip()
                end_date = date_location[1].strip() if len(date_location) > 1 else ''
                responsibilities = '\n'.join(lines[2:]).strip()
                experience_list.append({
                    "job_title": job_title,
                    "company": company,
                    "start_date": start_date,
                    "end_date": end_date,
                    "responsibilities": responsibilities
                })
        return experience_list
    return None

def extract_education(text):
    education_pattern = re.compile(r'Education:\s*(.*?)\s*(Skills|Certifications|Projects|Languages|Interests):', re.S)
    match = education_pattern.search(text)
    if match:
        educations = match.group(1).strip()
        education_entries = educations.split('\n\n')
        education_list = []
        for entry in education_entries:
            lines = entry.split('\n')
            if len(lines) >= 1:
                degree_institution = lines[0].split(',')
                degree = degree_institution[0].strip()
                institution = degree_institution[1].strip() if len(degree_institution) > 1 else ''
                start_end_date = lines[1].split('-') if len(lines) > 1 else ''
                start_date = start_end_date[0].strip() if len(start_end_date) > 0 else ''
                end_date = start_end_date[1].strip() if len(start_end_date) > 1 else ''
                education_list.append({
                    "degree": degree,
                    "institution": institution,
                    "start_date": start_date,
                    "end_date": end_date
                })
        return education_list
    return None

def extract_skills(text):
    skills_pattern = re.compile(r'Skills:\s*(.*?)\s*(Certifications|Projects|Languages|Interests):', re.S)
    match = skills_pattern.search(text)
    return [skill.strip() for skill in match.group(1).split(',')] if match else None

def extract_certifications(text):
    certifications_pattern = re.compile(r'Certifications:\s*(.*?)\s*(Projects|Languages|Interests):', re.S)
    match = certifications_pattern.search(text)
    if match:
        certifications = match.group(1).strip()
        certification_entries = certifications.split('\n\n')
        certification_list = []
        for entry in certification_entries:
            lines = entry.split('\n')
            if len(lines) >= 1:
                name_institution = lines[0].split(',')
                name = name_institution[0].strip()
                institution = name_institution[1].strip() if len(name_institution) > 1 else ''
                date = lines[1].strip() if len(lines) > 1 else ''
                certification_list.append({
                    "name": name,
                    "institution": institution,
                    "date": date
                })
        return certification_list
    return None

def extract_projects(text):
    projects_pattern = re.compile(r'Projects:\s*(.*?)\s*(Languages|Interests):', re.S)
    match = projects_pattern.search(text)
    if match:
        projects = match.group(1).strip()
        project_entries = projects.split('\n\n')
        project_list = []
        for entry in project_entries:
            lines = entry.split('\n')
            if len(lines) >= 1:
                title = lines[0].strip()
                description = lines[1].strip() if len(lines) > 1 else ''
                technologies = [tech.strip() for tech in lines[2].split(',')] if len(lines) > 2 else []
                project_list.append({
                    "title": title,
                    "description": description,
                    "technologies": technologies
                })
        return project_list
    return None

def extract_languages(text):
    languages_pattern = re.compile(r'Languages:\s*(.*?)\s*(Interests):', re.S)
    match = languages_pattern.search(text)
    return [language.strip() for language in match.group(1).split(',')] if match else None

def extract_interests(text):
    interests_pattern = re.compile(r'Interests:\s*(.*?)$', re.S)
    match = interests_pattern.search(text)
    return [interest.strip() for interest in match.group(1).split(',')] if match else None

# Example usage
# Provide information extracted from the prompt after giving in resume as input in place of the example usage provided here
resume_text = """
Harika Vundru
Email: vv8850@srmist.edu.in
Phone: +91 9701810979
Address: Villa no 130, APR Signator, Mallampet, Hyderabad, Telangana-500090

Professional Summary:
Highly motivated and creative B.Tech Computer Science Engineering student with a passion for Coding, Artificial Intelligence, Machine Learning, UI/UX designing, and App development...

Experience:
Research Intern, Samsung PRISM, Chennai, Tamil Nadu
Sept 2023 - Feb 2024
- Worked on a project that consisted on developing an app which reads users’ lip movements and converts it to text.

AI-ML Virtual Internship, AICTE, AWS, Online
May 2023 - July 2023
- A three-month online AI-ML internship conducted by AICTE.

Education:
B.Tech in CSE, SRM Institute of Science and Technology, Chennai, Tamil Nadu
2021 - 2025

High School/Intermediate, FIITJEE Jr College
2019 - 2021

10th Standard, Silver Oaks International School
2009 - 2019

Skills:
C, C++, Python, HTML, CSS, Flutter, Android Studio, MySQL, SQLite, Figma, Machine Learning, Deep Learning, UI/UX Design, Problem Solving, Analytical Skills

Certifications:
AWS Machine Learning Foundation Certificate, AWS, April 2023
Geodata Processing using Python, IIRS, February 2023

Projects:
Lip2Text
- Identifying and reading the user's lip movements and converting that into text with the help of data sets. Executed using neural networks like CNN and RNN.

Languages:
English, Telugu, Hindi

Interests:
AI/ML, Web Development, Mobile App Development
"""

parsed_resume = parse_resume(resume_text)
print(json.dumps(parsed_resume, indent=4))
