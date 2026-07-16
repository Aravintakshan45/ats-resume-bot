from src.utils import extract_keywords
from src.rules import check_sections, check_formatting, extract_skills

def calculate_ats_score(resume_text, job_description):
    """
    Calculate the overall ATS score for a resume against a job description.
    
    Args:
        resume_text (str): Resume text
        job_description (str): Job description text
        
    Returns:
        dict: Dictionary containing all scores and analysis results
    """
    # Extract keywords
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)
    
    # Calculate keyword match
    if job_keywords:
        matched_keywords = [kw for kw in job_keywords if kw in resume_keywords]
        keyword_score = (len(matched_keywords) / len(job_keywords)) * 100
        missing_keywords = [kw for kw in job_keywords if kw not in resume_keywords]
    else:
        keyword_score = 0
        matched_keywords = []
        missing_keywords = []
    
    # Check sections
    section_results = check_sections(resume_text)
    section_score = section_results['section_score']
    present_sections = section_results['present_sections']
    missing_sections = section_results['missing_sections']
    
    # Check formatting
    formatting_results = check_formatting(resume_text)
    formatting_score = formatting_results['formatting_score']
    formatting_issues = formatting_results['formatting_issues']
    
    # Extract and score skills
    skills_results = extract_skills(resume_text, job_description)
    skills_score = skills_results['skills_score']
    found_skills = skills_results['found_skills']
    matched_skills = skills_results['matched_skills']
    missing_skills = skills_results['missing_skills']
    
    # Calculate final weighted score
    final_score = (
        keyword_score * 0.50 +
        section_score * 0.20 +
        formatting_score * 0.15 +
        skills_score * 0.15
    )
    
    # Return comprehensive results
    return {
        'final_score': final_score,
        'keyword_score': keyword_score,
        'section_score': section_score,
        'formatting_score': formatting_score,
        'skills_score': skills_score,
        'resume_keywords': resume_keywords[:50],
        'job_keywords': job_keywords[:50],
        'matched_keywords': matched_keywords,
        'missing_keywords': missing_keywords,
        'present_sections': present_sections,
        'missing_sections': missing_sections,
        'formatting_issues': formatting_issues,
        'found_skills': found_skills,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'keyword_match_percentage': (len(matched_keywords) / len(job_keywords) * 100) if job_keywords else 0
    }