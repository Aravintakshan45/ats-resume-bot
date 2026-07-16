import streamlit as st
import os
from src.parser import extract_text_from_pdf, extract_text_from_docx
from src.scorer import calculate_ats_score
from src.ollama_bot import get_ai_response
import tempfile

st.set_page_config(page_title="ATS Resume Analyzer Bot", page_icon="📄", layout="wide")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "job_description" not in st.session_state:
    st.session_state.job_description = ""

st.title("📄 ATS Resume Analyzer Bot")
st.markdown("Analyze your resume against job descriptions with AI-powered insights")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Resume")
    uploaded_file = st.file_uploader("Choose your resume (PDF or DOCX)", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            if uploaded_file.type == "application/pdf" or uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(tmp_path)
            else:
                resume_text = extract_text_from_docx(tmp_path)
            
            st.session_state.resume_text = resume_text
            os.unlink(tmp_path)
            st.success(f"✅ Resume uploaded! ({len(resume_text)} characters)")
            
            with st.expander("Preview Resume Text"):
                st.text(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)
        except Exception as e:
            st.error(f"Error: {str(e)}")

with col2:
    st.subheader("📋 Job Description")
    use_sample = st.checkbox("Use sample job description (Data Analyst)")
    
    if use_sample:
        sample_path = os.path.join("data", "sample_job_description.txt")
        if os.path.exists(sample_path):
            with open(sample_path, "r") as f:
                sample_jd = f.read()
            job_description = st.text_area("Sample Job Description", value=sample_jd, height=300, disabled=True)
            st.session_state.job_description = sample_jd
        else:
            st.warning("Sample not found. Please paste your own.")
            job_description = st.text_area("Paste Job Description", height=300)
            st.session_state.job_description = job_description
    else:
        job_description = st.text_area("Paste Job Description", height=300, value=st.session_state.job_description or "")
        st.session_state.job_description = job_description

if st.button("🔍 Analyze Resume", type="primary"):
    if not st.session_state.resume_text:
        st.warning("Please upload a resume first!")
    elif not st.session_state.job_description:
        st.warning("Please provide a job description!")
    else:
        with st.spinner("Analyzing your resume..."):
            results = calculate_ats_score(st.session_state.resume_text, st.session_state.job_description)
            st.session_state.analysis_results = results
            st.session_state.chat_history = [
                {"role": "assistant", "content": f"Hello! Your ATS score is {results['final_score']:.1f}%. Ask me anything about improving your resume or where to apply!"}
            ]

if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    st.markdown("---")
    st.subheader("📊 ATS Analysis Results")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.metric("Overall", f"{results['final_score']:.1f}%")
    with c2: st.metric("Keywords", f"{results['keyword_score']:.1f}%")
    with c3: st.metric("Sections", f"{results['section_score']:.1f}%")
    with c4: st.metric("Formatting", f"{results['formatting_score']:.1f}%")
    with c5: st.metric("Skills", f"{results['skills_score']:.1f}%")

st.markdown("---")
st.subheader("🤖 Ask Your AI Career Assistant")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask about your resume or job search..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(prompt, st.session_state.analysis_results)
            st.write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

st.markdown("---")
st.caption("ATS Resume Analyzer Bot - Powered by Mistral AI 🧠 | Runs 100% Locally")
