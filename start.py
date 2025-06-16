import streamlit as st

# Page configuration
st.set_page_config(page_title="AI Resume Scorer", layout="centered")

st.title("Welcome to AI Resume Scorer")

st.markdown("""
This app helps:
- **Job Seekers** improve their resume with AI assistance
- **Hiring Teams** rank resumes based on job descriptions

Select your role to get started:
""")

# Role selection
user_type = st.radio("Who are you?", ["Individual (Job Seeker)", "Hiring Team / Recruiter"])

# Store in session state for navigation
st.session_state["user_type"] = user_type

# Navigation buttons
if user_type == "Individual (Job Seeker)":
    if st.button(" Continue as Individual"):
        st.switch_page("IndividualDashboard.py")

elif user_type == "Hiring Team / Recruiter":
    if st.button(" Continue as Hiring Team"):
        st.switch_page("HiringTeamDashboard.py")