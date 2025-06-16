import streamlit as st

# Page configuration
st.set_page_config(page_title="AI Resume Scorer", layout="centered", initial_sidebar_state="collapsed")



# Hide sidebar navigation
# st.markdown("""
#     <style>
#         [data-testid="stSidebarNav"] {
#             display: none;
#         }
#     </style>
# """, unsafe_allow_html=True)

# Handle redirection based on query param
st.title("Welcome to AI Resume Scorer")

st.markdown("""
This application is designed to assist two types of users:

- **Individuals (Job Seekers):** Upload your resume and receive AI-powered insights, feedback, and suggestions to improve it based on best practices and job descriptions.
- **Hiring Teams / Recruiters:** Upload multiple resumes along with a job description to automatically rank and evaluate how well each candidate matches the role.

This app helps:
- **Job Seekers** improve their resume with AI assistance
- **Hiring Teams** rank resumes based on job descriptions

Select your role from the sidebar to get started:
""")