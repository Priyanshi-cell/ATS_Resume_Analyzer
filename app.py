import streamlit as st
import google.generativeai as genai
import os
import fitz  # PyMuPDF
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#core functions

@st.cache_data(show_spinner=False)
def get_gemini_response(resume_text, job_description, prompt):
    """Caches Gemini API responses to improve performance."""
    try:
        model = genai.GenerativeModel('gemini-flash-latest') 
        response = model.generate_content([resume_text, job_description, prompt])
        return response.text
    except Exception as e:
        st.error(f"An error occurred with the API call: {e}")
        return None

@st.cache_data(show_spinner=False)
def get_pdf_text(uploaded_file):
    """Uses the fast PyMuPDF library to extract text from a PDF."""
    if uploaded_file is not None:
        try:
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = "".join(page.get_text() for page in pdf_document)
            return text
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
            return None
    return None

def load_css(file_name):
    """Loads a CSS file into the Streamlit app."""
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}")

#prompts
input_prompt1 = "You are an experienced Technical HR Manager. Review the resume against the job description. Highlight strengths and weaknesses in separate, clearly marked markdown sections."
input_prompt2 = "You are an expert career coach. Based on the resume and job description, identify missing skills and suggest a clear, actionable plan (online courses, projects, certifications) using markdown formatting."
input_prompt3 = """
You are an expert ATS scanner and professional resume reviewer. 
Evaluate the provided resume against the job description and return ONLY a JSON object with the following six keys:
1. "percentage_match": An integer representing the match score (e.g., 85).
2. "matching_keywords": A list of important keywords from the job description found in the resume.
3. "missing_keywords": A list of the most critical keywords from the job description NOT found in the resume.
4. "strengths": A list of 2-3 short, impactful bullet points highlighting the candidate's key strengths for this role.
5. "weaknesses": A list of 2-3 short, constructive bullet points on areas for improvement.
6. "final_thoughts": A concise, final summary statement.
"""

#UI
st.set_page_config(page_title="ATS Resume Analyzer", layout="wide")
load_css("style.css")

#Icons
logo_svg = """
<svg class="logo-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path class="cyan" d="M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2Z"/>
  <path class="magenta" d="M11.41 15.12L12.82 16.53L15.65 13.7L17.06 15.11L12.82 19.35L9.99 16.52L11.41 15.12Z"/>
</svg>
"""
analysis_icon = """<svg class="tab-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>"""
rewrite_icon = """<svg class="tab-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>"""
how_it_works_icon = """<svg class="tab-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>"""
strength_icon = """<svg class="icon-strength" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>"""
weakness_icon = """<svg class="icon-weakness" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>"""
missing_icon = """<svg class="icon-missing" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>"""

#app layout
title_html = f'<div class="title-container">{logo_svg}<h1>ATS Resume Analyzer</h1></div>'
st.markdown(title_html, unsafe_allow_html=True)
st.markdown("Analyze your resume against a job description and polish yourself.")

tab1, tab2, tab3 = st.tabs(["Resume Analysis", "Bullet Point Rewriter", "How It Works"])

with tab1:
    st.markdown(f'<div class="tab-header">{analysis_icon}<h3>Analyze Your Resume</h3></div>', unsafe_allow_html=True)
    input_text = st.text_area("📋 Paste the Job Description here:", key="input", height=250)
    uploaded_file = st.file_uploader("📂 Upload your Resume (PDF)", type=["pdf"])

    if uploaded_file: st.success("PDF Uploaded Successfully!")

    col1, col2, col3 = st.columns(3)
    with col1: submit1 = st.button("Evaluate Resume", use_container_width=True)
    with col2: submit2 = st.button("Suggest Improvements", use_container_width=True)
    with col3: submit3 = st.button("Customized ATS Report", use_container_width=True, key="ats_report")

    if submit1 or submit2 or submit3:
        if not uploaded_file or not input_text:
            st.warning("⚠️ Please upload a resume and paste a job description.")
        else:
            pdf_text = get_pdf_text(uploaded_file)
            if pdf_text:
                if submit1:
                    with st.spinner("Evaluating your resume..."):
                        response = get_gemini_response(pdf_text, input_text, input_prompt1)
                        st.subheader("Resume Evaluation Report")
                        st.markdown(response)
                elif submit2:
                    with st.spinner("Generating suggestions for improvement..."):
                        response = get_gemini_response(pdf_text, input_text, input_prompt2)
                        st.subheader("Personalized Improvement Plan")
                        st.markdown(response)
                elif submit3:
                    with st.spinner("Generating Comprehensive ATS Report..."):
                        response = get_gemini_response(pdf_text, input_text, input_prompt3)
                        if response:
                            cleaned_response = response.replace("```json", "").replace("```", "").strip()
                            try:
                                data = json.loads(cleaned_response)
                                
                                score_html = f"""
                                <div class="score-ring" style="--score-percent: {data.get('percentage_match', 0)};">
                                    <div class="score-center">
                                        <span>{data.get('percentage_match', 0)}%</span>
                                        <p>Match</p>
                                    </div>
                                </div>
                                """
                                
                                strengths_html = "".join([f"<li>{s}</li>" for s in data.get('strengths', [])])
                                weaknesses_html = "".join([f"<li>{w}</li>" for w in data.get('weaknesses', [])])
                                missing_kw_html = "".join([f"<li>{kw}</li>" for kw in data.get('missing_keywords', [])])
                                
                                details_html = f"""
                                <div class="dashboard-list">
                                    <h4>{strength_icon} Strengths</h4>
                                    <ul>{strengths_html if strengths_html else "<li>Not specified</li>"}</ul>
                                </div>
                                <div class="dashboard-list">
                                    <h4>{weakness_icon} Areas for Improvement</h4>
                                    <ul>{weaknesses_html if weaknesses_html else "<li>Not specified</li>"}</ul>
                                </div>
                                <div class="dashboard-list">
                                    <h4>{missing_icon} Missing Keywords</h4>
                                    <ul>{missing_kw_html if missing_kw_html else "<li>None found!</li>"}</ul>
                                </div>
                                """

                                st.subheader("Comprehensive ATS Dashboard")
                                st.markdown(f"""
                                <div class="ats-dashboard">
                                    <div class="score-column">{score_html}</div>
                                    <div class="details-column">{details_html}</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                with st.expander("Show AI's Final Thoughts"):
                                    st.info(data.get("final_thoughts", "Not provided."))

                            except (json.JSONDecodeError, TypeError) as e:
                                st.error(f"Error parsing the AI's detailed report: {e}")
                                st.markdown(response)

with tab2:
    st.markdown(f'<div class="tab-header">{rewrite_icon}<h3>Interactive Bullet Point Rewriter</h3></div>', unsafe_allow_html=True)
    st.markdown("Paste a bullet point from your resume and the job description (from the first tab) to get an improved version.")
    bullet_point = st.text_input("Paste your bullet point here:", key="bullet_point", placeholder="e.g., Managed social media accounts.")
    rewrite_button = st.button("Rewrite Bullet Point", use_container_width=True)

    rewrite_prompt = """You are an expert resume writer specializing in the STAR method. Rewrite the following bullet point to be more impactful and quantifiable, incorporating keywords from the provided job description.
    **Job Description:** --- {job_description} ---
    **Original Bullet Point:** --- {bullet_point} ---
    Provide ONLY the single, rewritten bullet point as your response. Do not add any extra explanations."""

    if rewrite_button:
        if not bullet_point or not input_text:
            st.warning("Please provide a bullet point and a job description in the first tab.")
        else:
            with st.spinner("Rewriting..."):
                formatted_prompt = rewrite_prompt.format(job_description=input_text, bullet_point=bullet_point)
                try:
                    model = genai.GenerativeModel('gemini-flash-latest')
                    response = model.generate_content(formatted_prompt)
                    st.markdown("### ✨ Suggested Improvement:")
                    st.success(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

with tab3:
    st.markdown(f'<div class="tab-header">{how_it_works_icon}<h3>How It Works</h3></div>', unsafe_allow_html=True)
    st.markdown("""
    This tool leverages Google's advanced Gemini AI to help you optimize your resume.
    
    - **Resume Analysis:** Get a detailed analysis from an HR perspective, a skill improvement plan, and a comprehensive ATS report.
    - **Bullet Point Rewriter:** Rewrite your resume bullet points for greater impact using the STAR method.
    - **Technology:** Built with Streamlit, PyMuPDF for fast PDF processing, and powered by Google Gemini.
    """)

