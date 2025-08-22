import streamlit as st
from backend.naukridotcomfetcher import scrape_job_selenium
from backend.jobdetailstructurer import structurer
from backend.resume_praserer import resume_extractor
from backend.scorer import score_resume  # Import the new scorer function
import tempfile
import os
import json

st.set_page_config(layout="wide")
st.title("📄 Resume and Job Description Analyzer")

# Text input for job URL
text_input = st.text_input("Enter the Job Posting URL:")

# File uploader for resume
uploaded_file = st.file_uploader("Upload your resume (PDF):")

# Check if both inputs are provided
both_provided = text_input and uploaded_file

# Submit button - enabled only if both inputs are provided
submit_button = st.button("Analyze", disabled=not both_provided)

# Display status messages
if not both_provided:
    if not text_input and not uploaded_file:
        st.info("Please provide a job URL and upload a resume to begin.")
    elif not text_input:
        st.warning("Please enter a job URL.")
    elif not uploaded_file:
        st.warning("Please upload a resume file.")

# Process when the submit button is clicked
if submit_button and both_provided:
    st.success("Processing your request...")
    
    col1, col2 = st.columns(2)
    
    job_details = None
    resume_data = None
    
    with col1:
        st.subheader("🔍 Job Details")
        with st.spinner("Fetching and structuring job details..."):
            try:
                scraped_data = scrape_job_selenium(text_input)
                job_details = structurer(scraped_data)
                
                if isinstance(job_details, str):
                    try:
                        job_details = json.loads(job_details)
                    except json.JSONDecodeError:
                        st.error("Failed to parse job details as JSON.")
                        st.stop()

                if isinstance(job_details, dict):
                    for key, value in job_details.items():
                        st.markdown(f"**{key.replace('_', ' ').title()}:**")
                        if isinstance(value, (list, dict)):
                            st.json(value)
                        else:
                            st.write(str(value))
                else:
                    st.write(job_details)
            except Exception as e:
                st.error(f"Error fetching job details: {e}")
                st.stop()

    with col2:
        st.subheader("📄 Resume Data")
        with st.spinner("Extracting information from your resume..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_file_path = tmp_file.name

                resume_data = resume_extractor(tmp_file_path)
                os.unlink(tmp_file_path)

                if isinstance(resume_data, str):
                    try:
                        resume_data = json.loads(resume_data)
                    except json.JSONDecodeError:
                        st.error("Failed to parse resume data as JSON.")
                        st.stop()

                if isinstance(resume_data, dict):
                    for key, value in resume_data.items():
                        st.markdown(f"**{key.replace('_', ' ').title()}:**")
                        if isinstance(value, (list, dict)):
                            st.json(value)
                        else:
                            st.write(str(value))
                else:
                    st.write(resume_data)
            except Exception as e:
                st.error(f"Error processing resume: {e}")
                st.stop()
    
    st.divider()

    if job_details and resume_data:
        st.subheader("📊 Resume Score and Analysis")
        with st.spinner("Comparing resume to job description and calculating score..."):
            analysis = score_resume(resume_data, job_details)

            if analysis and analysis["score"] > 0:
                st.metric(label="Compatibility Score", value=f"{analysis['score']}/100")
                
                st.markdown("### Summary")
                st.write(analysis["summary"])

                st.markdown("### ✅ Strengths")
                for strength in analysis["strengths"]:
                    st.write(f"- {strength}")

                st.markdown("### ⚠️ Areas for Improvement")
                for weakness in analysis["weaknesses"]:
                    st.write(f"- {weakness}")
            else:
                st.error("Could not generate the resume analysis. Please try again.")