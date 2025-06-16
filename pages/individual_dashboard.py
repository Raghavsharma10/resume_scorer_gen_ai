# IndividualDashboard.py

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

st.set_page_config(page_title="Resume Score", layout="centered", initial_sidebar_state="collapsed")

# Ask user for Groq API key
groq_api_key = st.text_input("Enter your Groq API Key", type="password")

if not groq_api_key:
    st.warning("Please enter your Groq API Key to continue.")
    st.stop()

st.title("Resume Score & AI Suggestions")
st.markdown("Upload your resume and paste the job description below to receive tailored AI feedback.")

# Upload resume
resume = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

# Paste job description
job_desc = st.text_area("Paste the Job Description")

# Process button
if st.button("Get AI Feedback"):
    if resume and job_desc:
        st.success("Processing your resume with AI...")

        # Save uploaded file temporarily
        with open("temp_resume.pdf", "wb") as f:
            f.write(resume.read())

        try:
            loader = PyPDFLoader("temp_resume.pdf")
            docs = loader.load_and_split()
            resume_text = "\n".join([doc.page_content for doc in docs])

            llm = ChatGroq(api_key=groq_api_key, model_name="Llama3-8b-8192")

            prompt = PromptTemplate.from_template("""
You are an expert recruiter and resume evaluator. Given the job description and the candidate's resume, score the resume's suitability for the job from 0 to 100. Justify the score briefly and provide suggestions for improvement.

Job Description:
{job}

Resume:
{resume}

Respond in this format:
Score: <score>/100  
Feedback: <brief analysis and improvement tips>
""")

            chain = prompt | llm
            response = chain.invoke({"job": job_desc, "resume": resume_text})

            st.subheader("📊 Score and Feedback")
            st.write(response.content if hasattr(response, "content") else str(response))

        except Exception as e:
            st.error(f"❌ Failed to process resume: {e}")
    else:
        st.warning("Please upload a resume and provide a job description.")