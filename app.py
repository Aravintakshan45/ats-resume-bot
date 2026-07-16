import streamlit as st
import os
from src.parser import extract_text_from_pdf, extract_text_from_docx
from src.scorer import calculate_ats_score
from src.ollama_bot import get_ai_response
import tempfile

# Page configuration
st.set_page_config(
    page_title="ATS Resume Analyzer Bot",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""

# Title
st.title("📄 ATS Resume Analyzer Bot")
st.markdown("Analyze your resume against job descriptions with AI-powered insights")

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Resume")
    
    uploaded_file = st.file_uploader(
        "Choose your resume (PDF or DOCX)",
        type=['pdf', 'docx'],
        help="Upload your resume in PDF or DOCX format"
    )
    
    if uploaded_file is not None:
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # Extract text based on file type
            if uploaded_file.type == "application/pdf" or uploaded_file.name.endswith('.pdf'):
                resume_text = extract_text_from_pdf(tmp_path)
            else:
                resume_text = extract_text_from_docx(tmp_path)
            
            st.session_state.resume_text = resume_text
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            st.success(f"✅ Resume uploaded successfully! ({len(resume_text)} characters)")
            
            # Show preview
            with st.expander("Preview Resume Text"):
                st.text(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

with col2:
    st.subheader("📋 Job Description")
    
    # Option to use sample or paste custom
    use_sample = st.checkbox("Use sample job description (Data Analyst)")
    
    if use_sample:
        sample_path = os.path.join("data", "sample_job_description.txt")
        if os.path.exists(sample_path):
            with open(sample_path, 'r') as f:
                sample_jd = f.read()
            job_description = st.text_area(
                "Sample Job Description",
                value=sample_jd,
                height=300,
                disabled=True
            )
            st.session_state.job_description = sample_jd
        else:
            st.warning("Sample job description not found. Please paste your own.")
            job_description = st.text_area(
                "Paste Job Description",
                height=300,
                placeholder="Paste the job description here..."
            )
            st.session_state.job_description = job_description
    else:
        job_description = st.text_area(
            "Paste Job Description",
            height=300,
            placeholder="Paste the job description here...",
            value=st.session_state.job_description if st.session_state.job_description else ""
        )
        st.session_state.job_description = job_description

# Analyze button
if st.button("🔍 Analyze Resume", type="primary"):
    if not st.session_state.resume_text:
        st.warning("Please upload a resume first!")
    elif not st.session_state.job_description:
        st.warning("Please provide a job description!")
    else:
        with st.spinner("Analyzing your resume..."):
            # Calculate ATS score
            results = calculate_ats_score(
                st.session_state.resume_text,
                st.session_state.job_description
            )
            st.session_state.analysis_results = results
            
            # Add initial bot message
            st.session_state.chat_history = [
                {"role": "assistant", "content": f"Hello! I've analyzed your resume against the job description. Your overall ATS score is {results['final_score']:.1f}%. Ask me anything about improving your resume!"}
            ]

# Display results if available
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    st.markdown("---")
    st.subheader("📊 ATS Analysis Results")
    
    # Score display with metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Overall Score",
            f"{results['final_score']:.1f}%",
            delta=None
        )
    
    with col2:
        st.metric(
            "Keyword Match",
            f"{results['keyword_score']:.1f}%",
            delta=None
        )
    
    with col3:
        st.metric(
            "Section Score",
            f"{results['section_score']:.1f}%",
            delta=None
        )
    
    with col4:
        st.metric(
            "Formatting Score",
            f"{results['formatting_score']:.1f}%",
            delta=None
        )
    
    with col5:
        st.metric(
            "Skills Score",
            f"{results['skills_score']:.1f}%",
            delta=None
        )
    
    # Detailed breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ What's Working")
        if results['present_sections']:
            st.write("**Present Sections:**")
            for section in results['present_sections']:
                st.success(f"✓ {section}")
        else:
            st.warning("No standard sections detected")
    
    with col2:
        st.subheader("⚠️ Areas for Improvement")
        
        if results['missing_keywords']:
            st.write("**Missing Keywords:**")
            for keyword in results['missing_keywords'][:10]:
                st.error(f"✗ {keyword}")
            if len(results['missing_keywords']) > 10:
                st.info(f"... and {len(results['missing_keywords']) - 10} more")
        
        if results['missing_sections']:
            st.write("**Missing Sections:**")
            for section in results['missing_sections']:
                st.warning(f"⚠ {section}")
        
        if results['formatting_issues']:
            st.write("**Formatting Issues:**")
            for issue in results['formatting_issues']:
                st.warning(f"⚠ {issue}")
        
        if not results['missing_keywords'] and not results['missing_sections'] and not results['formatting_issues']:
            st.success("✅ Your resume looks great! No major issues found.")
    
    # Keyword Analysis
    with st.expander("🔍 Detailed Keyword Analysis"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Resume Keywords Found**")
            if results['resume_keywords']:
                for kw in results['resume_keywords'][:20]:
                    st.code(kw)
            else:
                st.write("No keywords extracted")
        
        with col2:
            st.write("**Job Description Keywords**")
            if results['job_keywords']:
                for kw in results['job_keywords'][:20]:
                    st.code(kw)
            else:
                st.write("No keywords extracted")

# Chatbot Interface
st.markdown("---")
st.subheader("🤖 Ask the AI ATS Bot")

# Chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your resume analysis..."):
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(prompt, st.session_state.analysis_results)
            st.write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")

# Updated footer to show Groq AI instead of Mistral
st.caption("⚡ Powered by Groq AI (Llama 3.3 70B) | Hosted on Streamlit Cloud 🚀")
