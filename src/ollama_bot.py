
import streamlit as st
import groq

# Current Groq models (as of 2026)
GROQ_MODEL = "llama-3.3-70b-versatile"  # Latest, most capable

def get_ai_response(user_question, analysis_results):
    """
    Get AI response using Groq API (Latest Models)
    """
    if not analysis_results:
        return "Please analyze your resume first by uploading it and providing a job description."
    
    # Build context from analysis results
    context_lines = []
    context_lines.append(f"Overall Score: {analysis_results['final_score']:.1f}%")
    context_lines.append(f"Keyword Score: {analysis_results['keyword_score']:.1f}%")
    context_lines.append(f"Section Score: {analysis_results['section_score']:.1f}%")
    context_lines.append(f"Formatting Score: {analysis_results['formatting_score']:.1f}%")
    context_lines.append(f"Skills Score: {analysis_results['skills_score']:.1f}%")
    context_lines.append("")
    
    missing_keywords = analysis_results.get('missing_keywords', [])
    if missing_keywords:
        context_lines.append(f"Missing Keywords: {', '.join(missing_keywords[:10])}")
    
    missing_sections = analysis_results.get('missing_sections', [])
    if missing_sections:
        context_lines.append(f"Missing Sections: {', '.join(missing_sections)}")
    
    formatting_issues = analysis_results.get('formatting_issues', [])
    if formatting_issues:
        context_lines.append(f"Formatting Issues: {', '.join(formatting_issues[:3])}")
    
    found_skills = analysis_results.get('found_skills', [])
    if found_skills:
        context_lines.append(f"Skills Found: {', '.join(found_skills[:10])}")
    
    context = "\n".join(context_lines)
    
    # Check if question is about job search
    job_keywords = ['where', 'apply', 'job', 'company', 'hire', 'position', 
                    'openings', 'career', 'portal', 'site', 'website', 
                    'indeed', 'linkedin', 'naukri', 'monster']
    is_job_search = any(word in user_question.lower() for word in job_keywords)
    
    # Add job search advice if relevant
    if is_job_search and analysis_results:
        skills = analysis_results.get('found_skills', [])
        advice_lines = []
        
        if any(s in ['python', 'sql', 'tableau', 'power bi', 'data', 'analytics'] for s in skills):
            advice_lines.append("✅ For Data/Analytics roles, focus on:")
            advice_lines.append("  • LinkedIn for professional networking")
            advice_lines.append("  • Indeed for data roles")
            advice_lines.append("  • Glassdoor for company reviews")
            advice_lines.append("  • AngelList for startup roles")
        
        if any(s in ['java', 'javascript', 'react', 'angular', 'node'] for s in skills):
            advice_lines.append("✅ For Developer roles, focus on:")
            advice_lines.append("  • GitHub Jobs for tech roles")
            advice_lines.append("  • Stack Overflow Jobs")
            advice_lines.append("  • Hacker News Who's Hiring")
        
        if not advice_lines:
            advice_lines.append("📌 General Job Search Tips:")
            advice_lines.append("  • Customize your resume for each application")
            advice_lines.append("  • Network with people in your industry")
            advice_lines.append("  • Use company websites directly")
            advice_lines.append("  • Set up job alerts on multiple platforms")
        
        context += "\n\nJob Search Advice:\n" + "\n".join(advice_lines)
    
    # Create prompt
    prompt = f"""
You are an expert career advisor and ATS resume specialist.

Here is the resume analysis:
{context}

User Question: {user_question}

Please provide a helpful, specific, and actionable response.
"""
api_key = st.secrets["GROQ_API_KEY"]
    
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        
        client = groq.Groq(api_key=api_key)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert career advisor and ATS resume specialist. Give specific, actionable, and encouraging advice."},
                {"role": "user", "content": prompt}
            ],
            model=GROQ_MODEL,
            temperature=0.7,
            max_tokens=500
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        # Fallback to Ollama
        try:
            import ollama
            response = ollama.chat(
                model="mistral",
                messages=[
                    {'role': 'system', 'content': 'You are an expert career advisor and ATS resume specialist.'},
                    {'role': 'user', 'content': prompt}
                ]
            )
            return response['message']['content']
        except:
            return f"Error connecting to AI. Please check your internet connection. Error: {str(e)}"


# Check if backup file exists
ls -la src/ollama_bot.py.save

# If it exists, remove it
rm -f src/ollama_bot.py.saveexit()

