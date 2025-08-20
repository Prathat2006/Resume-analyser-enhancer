import streamlit as st
from backend.naukridotcomfetcher import scrape_job_selenium
from backend.jobdetailstructurer import structurer
from backend.resume_praserer import resume_extractor

st.title("File and Text Input")

# Text input
text_input = st.text_input("Enter job URL:")

# File input
uploaded_file = st.file_uploader("Upload a resume file")

# Check if both inputs are provided
both_provided = text_input and uploaded_file

# Submit button - only enabled if both inputs are provided
submit_button = st.button("Submit", disabled=not both_provided)

# Display status message
if not both_provided:
    if not text_input and not uploaded_file:
        st.warning("⚠️ Please provide both job URL and upload a resume file to proceed.")
    elif not text_input:
        st.warning("⚠️ Please enter a job URL.")
    elif not uploaded_file:
        st.warning("⚠️ Please upload a resume file.")

# Process only when submit button is clicked and both inputs are provided
if submit_button and both_provided:
    st.success("✅ Processing your inputs...")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Job Details")
        with st.spinner("Fetching job details..."):
            try:
                job_details = structurer(scrape_job_selenium(text_input)
                )                
                # Display job details with proper formatting
                if isinstance(job_details, dict):
                    for key, value in job_details.items():
                        # Format key as colored header
                        st.markdown(f"**:blue[{key.replace('_', ' ').title()}:]**")
                        # Display value in regular text
                        if isinstance(value, (list, dict)):
                            st.json(value)
                        else:
                            st.write(value)
                        st.write("")  # Add spacing
                elif isinstance(job_details, str):
                    try:
                        import json
                        parsed_data = json.loads(job_details)
                        for key, value in parsed_data.items():
                            st.markdown(f"**:blue[{key.replace('_', ' ').title()}:]**")
                            if isinstance(value, (list, dict)):
                                st.json(value)
                            else:
                                st.write(value)
                            st.write("")
                    except json.JSONDecodeError:
                        st.write(job_details)
                else:
                    st.json(job_details)
                    
            except Exception as e:
                st.error(f"Error fetching job details: {str(e)}")
    
    with col2:
        st.subheader("📄 Resume Data")
        with st.spinner("Processing resume..."):
            try:
                # Option 1: Save the uploaded file temporarily and pass the path
                import tempfile
                import os
                
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_file_path = tmp_file.name
                
                # Process the temporary file
                resume_data = resume_extractor(tmp_file_path)
                
                # Display resume data with proper formatting
                if isinstance(resume_data, dict):
                    for key, value in resume_data.items():
                        # Format key as colored header
                        st.markdown(f"**:green[{key.replace('_', ' ').title()}:]**")
                        # Display value in regular text
                        if isinstance(value, (list, dict)):
                            st.json(value)
                        elif isinstance(value, str) and len(value) > 100:
                            # For long text, use expander
                            with st.expander(f"View {key.replace('_', ' ').title()}"):
                                st.write(value)
                        else:
                            st.write(value)
                        st.write("")  # Add spacing
                elif isinstance(resume_data, str):
                    try:
                        import json
                        parsed_data = json.loads(resume_data)
                        for key, value in parsed_data.items():
                            st.markdown(f"**:green[{key.replace('_', ' ').title()}:]**")
                            if isinstance(value, (list, dict)):
                                st.json(value)
                            elif isinstance(value, str) and len(value) > 100:
                                with st.expander(f"View {key.replace('_', ' ').title()}"):
                                    st.write(value)
                            else:
                                st.write(value)
                            st.write("")
                    except json.JSONDecodeError:
                        # If it's just plain text, display it nicely
                        st.markdown("**:green[Extracted Content:]**")
                        st.write(resume_data)
                else:
                    st.json(resume_data)
                
                # Clean up the temporary file
                os.unlink(tmp_file_path)
                
            except Exception as e:
                st.error(f"Error processing resume: {str(e)}")