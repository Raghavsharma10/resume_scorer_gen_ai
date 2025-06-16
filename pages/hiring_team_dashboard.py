# HiringTeamDashboard.py
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import pandas as pd

st.set_page_config(page_title="Resume Ranking", layout="wide", initial_sidebar_state="collapsed")

st.title("AI-Powered Resume Ranking")

# Enter Groq API key
groq_api_key = st.text_input("Enter your Groq API Key", type="password")

if not groq_api_key:
    st.warning("Please enter your Groq API Key to continue.")
    st.stop()

st.markdown("Upload multiple resumes and a job description to rank them by match quality.")

# Upload multiple resumes
resumes = st.file_uploader("Upload Resumes (PDFs)", type=["pdf"], accept_multiple_files=True)

# Paste job description
job_desc = st.text_area("Paste the Job Description")

# Process button
if st.button("Get AI Feedback"):
    if resumes and job_desc:
        st.success("Processing your resumes with AI...")

        results = []
        try:
            llm = ChatGroq(api_key=groq_api_key, model_name="Llama3-8b-8192")

            prompt = PromptTemplate.from_template("""
You are an expert recruiter and resume evaluator. Given the job description and the candidate's resume, score the resume's suitability for the job from 0 to 100. Justify the score and ranking briefly and provide suggestions for improvement.

Job Description:
{job}

Resume:
{resume}

Respond in this format:
Score: <score>/100  
Feedback: <brief analysis and improvement tips>
""")

            for i, resume_file in enumerate(resumes):
                filename = f"temp_resume_{i}.pdf"
                with open(filename, "wb") as f:
                    f.write(resume_file.read())

                loader = PyPDFLoader(filename)
                docs = loader.load_and_split()
                resume_text = "\n".join([doc.page_content for doc in docs])

                chain = prompt | llm
                response = chain.invoke({"job": job_desc, "resume": resume_text})
                content = response.content if hasattr(response, "content") else str(response)

                # Parse score and feedback from response
                score = None
                feedback_lines = []
                score_found = False

                for line in content.splitlines():
                    if "Score:" in line:
                        try:
                            score_part = line.split("Score:")[1].strip()
                            score = score_part.split("/")[0].strip()
                            score_found = True
                        except:
                            score = None
                    elif "Feedback:" in line:
                        feedback_lines.append(line.split("Feedback:")[1].strip())
                    elif score_found:
                        feedback_lines.append(line.strip())

                feedback = " ".join(feedback_lines).strip()
                if not feedback:
                    feedback = "⚠️ No detailed feedback was returned by the AI."

                results.append({
                    "Resume": resume_file.name,
                    "Score": score,
                    "Feedback": feedback
                })

            st.subheader("📊 Scores and Feedback")
            df = pd.DataFrame(results)
            st.dataframe(df)
            st.subheader("📄 Detailed Feedback")
            for row in results:
                with st.expander(f"{row['Resume']} (Score: {row['Score']})"):
                    st.write(row["Feedback"])

        except Exception as e:
            st.error(f"❌ Failed to process resumes: {e}")
    else:
        st.warning("Please upload at least one resume and provide a job description.")