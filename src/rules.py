import re

def check_sections(resume_text):
    """
    Check which standard sections are present in the resume.
    
    Args:
        resume_text (str): Resume text
        
    Returns:
        dict: Dictionary with present sections and missing sections
    """
    sections = {
        'summary': ['summary', 'profile', 'objective', 'about me'],
        'experience': ['experience', 'work experience', 'employment', 'work history'],
        'education': ['education', 'academic', 'qualifications'],
        'skills': ['skills', 'technical skills', 'core competencies'],
        'projects': ['projects', 'project experience', 'portfolio']
    }
    
    text_lower = resume_text.lower()
    present_sections = []
    missing_sections = []
    
    for section, keywords in sections.items():
        found = False
        for keyword in keywords:
            if keyword in text_lower:
                present_sections.append(section)
                found = True
                break
        if not found:
            missing_sections.append(section)
    
    return {
        'present_sections': present_sections,
        'missing_sections': missing_sections,
        'section_score': (len(present_sections) / len(sections)) * 100
    }

def check_formatting(resume_text):
    """
    Check for common formatting issues in the resume.
    
    Args:
        resume_text (str): Resume text
        
    Returns:
        dict: Dictionary with formatting issues and score
    """
    issues = []
    score = 100
    
    # Check for bullet points
    if not re.search(r'[•·*\-]\s', resume_text):
        issues.append("No bullet points found - consider using bullet points for better readability")
        score -= 15
    
    # Check for dates (YYYY-YYYY, MM/YYYY, etc.)
    date_patterns = [
        r'\d{4}\s*[-–]\s*\d{4}',  # 2020-2022
        r'\d{2}/\d{4}',           # 12/2020
        r'\d{4}\s*(to|-|–|present)', # 2020-present
    ]
    has_dates = any(re.search(pattern, resume_text, re.IGNORECASE) for pattern in date_patterns)
    if not has_dates:
        issues.append("No dates found - include dates for work experience and education")
        score -= 15
    
    # Check for sections with consistent formatting
    lines = resume_text.split('\n')
    section_markers = ['summary', 'experience', 'education', 'skills', 'projects']
    has_section_headers = False
    for line in lines:
        line_lower = line.lower().strip()
        if any(marker in line_lower for marker in section_markers):
            has_section_headers = True
            break
    
    if not has_section_headers:
        issues.append("No clear section headers found - use clear headers for each section")
        score -= 20
    
    # Check for email
    if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
        issues.append("No email address found - include contact information")
        score -= 10
    
    # Check for phone number
    if not re.search(r'\+?\d[\d -]{8,}\d', resume_text):
        issues.append("No phone number found - include contact information")
        score -= 10
    
    # Check for location
    if not re.search(r'\b[A-Z][a-z]+[,]?\s*[A-Z]{2}\b', resume_text):
        issues.append("No location found - include your location")
        score -= 10
    
    # Check for consistent formatting (lines length)
    line_lengths = [len(line.strip()) for line in lines if len(line.strip()) > 0]
    if line_lengths:
        avg_length = sum(line_lengths) / len(line_lengths)
        if avg_length < 20:
            issues.append("Lines are too short - may indicate poor formatting")
            score -= 10
    
    return {
        'formatting_issues': issues,
        'formatting_score': max(0, score)
    }

def extract_skills(resume_text, job_description=None):
    """
    Extract skills from resume and compare with job description.
    
    Args:
        resume_text (str): Resume text
        job_description (str, optional): Job description for comparison
        
    Returns:
        dict: Dictionary with skills information
    """
    # Common skills keywords
    common_skills = [
        'python', 'sql', 'java', 'javascript', 'html', 'css', 'react', 'angular',
        'node.js', 'django', 'flask', 'tableau', 'power bi', 'excel', 'spss',
        'r', 'sas', 'stata', 'machine learning', 'deep learning', 'nlp',
        'data visualization', 'statistical analysis', 'predictive modeling',
        'etl', 'data mining', 'data cleaning', 'data warehousing',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git',
        'agile', 'scrum', 'project management', 'leadership',
        'communication', 'problem solving', 'critical thinking',
        'team collaboration', 'customer service', 'sales', 'marketing',
        'finance', 'accounting', 'human resources', 'operations'
    ]
    
    text_lower = resume_text.lower()
    found_skills = []
    
    for skill in common_skills:
        if skill in text_lower:
            found_skills.append(skill)
    
    # Compare with job description if provided
    matched_skills = []
    missing_skills = []
    
    if job_description:
        jd_lower = job_description.lower()
        jd_skills = [skill for skill in common_skills if skill in jd_lower]
        
        for skill in jd_skills:
            if skill in text_lower:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
        
        skills_score = (len(matched_skills) / len(jd_skills) * 100) if jd_skills else 0
    else:
        skills_score = 0
        missing_skills = []
        matched_skills = []
    
    return {
        'found_skills': found_skills,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'skills_score': skills_score
    }