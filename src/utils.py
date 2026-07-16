import re
import string

def clean_text(text):
    """
    Clean and normalize text.
    
    Args:
        text (str): Input text
        
    Returns:
        str: Cleaned text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep words and numbers
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # Remove extra spaces
    text = ' '.join(text.split())
    
    return text

def extract_keywords(text, min_length=3):
    """
    Extract keywords from text.
    
    Args:
        text (str): Input text
        min_length (int): Minimum keyword length
        
    Returns:
        list: List of unique keywords
    """
    # Clean text
    cleaned = clean_text(text)
    
    # Split into words
    words = cleaned.split()
    
    # Remove stopwords (common words)
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
                 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 
                 'through', 'during', 'including', 'as', 'than', 'so', 'if', 
                 'then', 'else', 'when', 'where', 'which', 'who', 'whom', 
                 'whose', 'that', 'this', 'these', 'those', 'am', 'is', 'are', 
                 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
                 'do', 'does', 'did', 'will', 'would', 'could', 'should', 
                 'may', 'might', 'must', 'can'}
    
    # Filter and clean keywords
    keywords = []
    for word in words:
        word = word.strip()
        if len(word) >= min_length and word not in stopwords:
            keywords.append(word)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)
    
    return unique_keywords

def extract_sections(text):
    """
    Extract common sections from resume text.
    
    Args:
        text (str): Resume text
        
    Returns:
        dict: Dictionary of section names and their content
    """
    sections = {
        'summary': ['summary', 'profile', 'objective', 'about'],
        'experience': ['experience', 'work experience', 'employment', 'work history'],
        'education': ['education', 'academic', 'qualifications'],
        'skills': ['skills', 'technical skills', 'core competencies'],
        'projects': ['projects', 'project experience', 'portfolio']
    }
    
    found_sections = {}
    text_lower = text.lower()
    
    for section, keywords in sections.items():
        for keyword in keywords:
            if keyword in text_lower:
                # Find the section content
                start_idx = text_lower.find(keyword)
                end_idx = len(text)
                
                # Try to find next section
                for next_section in sections.values():
                    for next_keyword in next_section:
                        next_idx = text_lower