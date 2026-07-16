import re

def get_bot_response(user_question, analysis_results):
    """
    Generate bot response based on analysis results.
    
    Args:
        user_question (str): User's question
        analysis_results (dict): Analysis results from scorer
        
    Returns:
        str: Bot response
    """
    if not analysis_results:
        return "Please analyze your resume first by uploading it and providing a job description."
    
    question_lower = user_question.lower()
    
    # Score-related questions
    if any(word in question_lower for word in ['score', 'low', 'bad', 'poor']):
        return get_score_response(analysis_results)
    
    # Keywords-related questions
    elif any(word in question_lower for word in ['keyword', 'missing', 'match']):
        return get_keyword_response(analysis_results)
    
    # Improvement suggestions
    elif any(word in question_lower for word in ['improve', 'better', 'enhance', 'fix']):
        return get_improvement_response(analysis_results)
    
    # Section-related questions
    elif any(word in question_lower for word in ['section', 'add', 'include']):
        return get_section_response(analysis_results)
    
    # General greeting
    elif any(word in question_lower for word in ['hello', 'hi', 'hey', 'greeting']):
        return "Hello! I'm your ATS analysis bot. I can help you understand your resume's ATS score and suggest improvements. What would you like to know?"
    
    # Default response
    else:
        return get_general_response(analysis_results)

def get_score_response(results):
    """Response for score-related questions."""
    score = results['final_score']
    
    if score >= 80:
        return f"Your ATS score is {score:.1f}%, which is excellent! Your resume is well-optimized. To maintain this, ensure you keep updating keywords and sections as you apply to different roles."
    elif score >= 60:
        return f"Your ATS score is {score:.1f}%. This is good, but there's room for improvement. Focus on adding missing keywords from the job description and ensuring all required sections are present. I'd suggest working on your keyword match specifically."
    elif score >= 40:
        return f"Your ATS score is {score:.1f}%. This is below average. I recommend: 1) Adding more keywords from the job description, 2) Including all standard sections, 3) Fixing formatting issues. Let me know if you want specific suggestions for any area."
    else:
        return f"Your ATS score is {score:.1f}%. This indicates significant optimization needed. Start by: 1) Extracting all keywords from the job description and incorporating them, 2) Adding missing sections like summary, experience, and skills, 3) Improving the formatting. I can provide detailed suggestions for each area."

def get_keyword_response(results):
    """Response for keyword-related questions."""
    missing = results['missing_keywords']
    matched = results['matched_keywords']
    
    if not missing:
        return "Great news! You haven't missed any keywords from the job description. Your resume is well-aligned with the required keywords."
    elif len(missing) <= 5:
        return f"You're missing {len(missing)} keywords: {', '.join(missing[:5])}. These are specific terms the employer is looking for. Try to naturally incorporate them into your experience descriptions, skills section, and summary. Your current keyword match rate is {results['keyword_match_percentage']:.1f}%."
    else:
        return f"You're missing {len(missing)} keywords from the job description. The most important ones to add are: {', '.join(missing[:10])}. I'd recommend: 1) Adding these keywords to your skills section, 2) Incorporating them into your experience bullet points, 3) Including them in your summary/profile. Your current keyword match rate is {results['keyword_match_percentage']:.1f}%."

def get_improvement_response(results):
    """Response for improvement suggestions."""
    improvements = []
    score = results['final_score']
    
    if results['missing_keywords']:
        improvements.append(f"Add missing keywords: {', '.join(results['missing_keywords'][:5])}")
    
    if results['missing_sections']:
        improvements.append(f"Add these sections: {', '.join(results['missing_sections'])}")
    
    if results['formatting_issues']:
        improvements.append(f"Fix formatting issues: {', '.join(results['formatting_issues'][:3])}")
    
    if results['missing_skills']:
        improvements.append(f"Add these skills: {', '.join(results['missing_skills'][:5])}")
    
    if not improvements:
        return "Your resume looks excellent! To maintain this quality: 1) Keep updating keywords for each application, 2) Ensure consistent formatting, 3) Quantify your achievements, 4) Add relevant projects to showcase your skills."
    
    improvement_text = "Based on my analysis, here are specific improvements you can make:\n\n"
    for i, imp in enumerate(improvements, 1):
        improvement_text += f"{i}. {imp}\n"
    
    improvement_text += f"\nYour overall ATS score is {score:.1f}%. Implementing these changes could significantly improve your score."
    
    return improvement_text

def get_section_response(results):
    """Response for section-related questions."""
    present = results['present_sections']
    missing = results['missing_sections']
    
    if not missing:
        return f"Your resume includes all standard sections: {', '.join(present)}. This is great for ATS compatibility. For each section, ensure you're using relevant keywords and quantifying your achievements where possible."
    else:
        sections_advice = {
            'summary': "Add a professional summary at the top of your resume. Include 3-4 sentences highlighting your experience, key skills, and career goals.",
            'experience': "Create a detailed work experience section. List your previous positions with bullet points describing responsibilities and achievements. Use action verbs and quantify results.",
            'education': "Add your educational background including degree, institution, and graduation year. Include relevant coursework if you're a recent graduate.",
            'skills': "Create a skills section listing technical and soft skills. Organize them into categories for better readability.",
            'projects': "Add a projects section to showcase practical applications of your skills. Include project descriptions, technologies used, and outcomes."
        }
        
        response = f"Your resume is missing these sections: {', '.join(missing)}.\n\n"
        for section in missing:
            if section in sections_advice:
                response += f"To add a {section} section:\n{sections_advice[section]}\n\n"
        
        return response

def get_general_response(results):
    """General response for other questions."""
    return "I can help you with questions about:\n- Your ATS score\n- Missing keywords\n- How to improve your resume\n- Adding sections\n- Skills matching\n\nWhat would you like to know specifically about your resume analysis?"