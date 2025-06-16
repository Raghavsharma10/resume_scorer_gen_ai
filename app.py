import streamlit as st
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

st.set_page_config(page_title="AI Resume Scorer", layout="centered")

# Load environment variables
load_dotenv()
user_api_key = st.text_input("🔑 Enter your Groq API Key", type="password")

if user_api_key:
    llm = ChatGroq(model_name="Llama3-8b-8192", api_key=user_api_key)

st.title("📄 AI Resume Scorer")

# Step 1: User inputs
job_description = st.text_area("📝 Paste the Job Description", height=200)
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])

# Step 2: Parse resume and score
if uploaded_file and job_description:
    with open("temp_resume.pdf", "wb") as f:
     f.write(uploaded_file.read())

    loader = PyPDFLoader("temp_resume.pdf")
    docs = loader.load()
    resume_text = "\n".join([doc.page_content for doc in docs])

    if st.button("Score My Resume"):
        with st.spinner("Scoring..."):
            try:
                llm = ChatGroq(model_name="Llama3-8b-8192")

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
                response = chain.invoke({"job": job_description, "resume": resume_text})

                st.subheader("📊 Score and Feedback")
                st.write(response)

            except Exception as e:
                st.error(f"❌ Failed to score resume: {e}")
else:
    st.info("ℹ️ Please upload your resume and enter a job description.")