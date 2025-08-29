import streamlit as st
import requests
import json
import time
from io import BytesIO
import base64

# Configure page
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .step-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .score-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 1rem 0;
    }
    
    .score-bad {
        background: linear-gradient(135deg, #ff416c 0%, #ff4757 100%) !important;
    }
    
    .score-average {
        background: linear-gradient(135deg, #ffa726 0%, #ffcc02 100%) !important;
        color: black !important;
    }
    
    .feature-card {
        background: #f8f9ff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e1e5e9;
        margin: 0.5rem 0;
    }
    
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8f9ff;
        margin: 1rem 0;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    
    .metric-item {
        text-align: center;
        padding: 1rem;
    }
    
    .stProgress .stProgress-bar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .p{
            color : grey;
            }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'evaluation_result' not in st.session_state:
    st.session_state.evaluation_result = None
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'enhanced_resume_data' not in st.session_state:
    st.session_state.enhanced_resume_data = None


# API Configuration
API_BASE_URL = "http://localhost:8000"  # Change this to your FastAPI server URL
def display_pdf(pdf_data):
    """Display PDF in the browser using base64 encoding"""
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    pdf_display = f'''
    <div class="pdf-viewer-container">
        <h3>📄 Your Enhanced Resume Preview</h3>
        <iframe 
            src="data:application/pdf;base64,{base64_pdf}" 
            width="100%" 
            height="800" 
            type="application/pdf"
            style="border: none; border-radius: 5px;">
        </iframe>
    </div>
    '''
    st.markdown(pdf_display, unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🚀 AI Resume Analyzer</h1>
    <p>Transform your resume with AI-powered analysis and enhancement</p>
</div>
""", unsafe_allow_html=True)

# Progress indicator
progress_steps = ["Upload & Analyze", "View Results", "Enhance Resume"]
current_step = st.session_state.step

col1, col2, col3 = st.columns(3)
for i, (col, step_name) in enumerate(zip([col1, col2, col3], progress_steps), 1):
    with col:
        if i <= current_step:
            st.markdown(f"**✅ {step_name}**")
        elif i == current_step + 1:
            st.markdown(f"**🔄 {step_name}**")
        else:
            st.markdown(f"⏳ {step_name}")

st.markdown("---")

# Step 1: Upload and Analyze
if st.session_state.step == 1:
    # st.markdown("""
    # <div class="step-container">
    #     <h2>📄 Step 1: Upload Resume & Job URL</h2>
    #     <p>Upload your resume and provide the job posting URL for AI-powered analysis</p>
    # </div>
    # """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📎 Upload Your Resume")
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'doc', 'docx'],
            help="Supported formats: PDF, DOC, DOCX"
        )
        
        if uploaded_file:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            file_size = len(uploaded_file.getbuffer()) / 1024  # KB
            st.info(f"File size: {file_size:.1f} KB")
    
    with col2:
        st.markdown("### 🔗 Job Posting URL")
        job_url = st.text_input(
            "Enter the job posting URL",
            placeholder="https://www.naukri.com/job-listings/...",
            help="Paste the complete URL of the job posting you're applying for"
        )
        
        if job_url:
            st.success("✅ Job URL provided")
    
    # Analysis button
    if uploaded_file and job_url:
        st.markdown("### 🎯 Ready to Analyze!")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Analyze My Resume", key="analyze_btn"):
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("📤 Uploading files...")
                    progress_bar.progress(25)
                    time.sleep(0.5)
                    
                    # Prepare files for API call
                    files = {"resume": (uploaded_file.name, uploaded_file.getbuffer(), uploaded_file.type)}
                    data = {"job_url": job_url}
                    
                    status_text.text("🤖 AI is analyzing your resume...")
                    progress_bar.progress(50)
                    
                    # Make API call
                    response = requests.post(f"{API_BASE_URL}/evaluate", files=files, data=data)
                    
                    progress_bar.progress(75)
                    status_text.text("📊 Generating insights...")
                    time.sleep(0.5)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.evaluation_result = result
                        st.session_state.session_id = result.get('session_id')
                        st.session_state.step = 2
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
                    st.info("💡 Make sure your FastAPI server is running on http://localhost:8000")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

# Step 2: View Results
elif st.session_state.step == 2:
    if st.session_state.evaluation_result:
        score_data = st.session_state.evaluation_result['score']
        
        # st.markdown("""
        # <div class="step-container">
        #     <h2>📊 Step 2: Analysis Results</h2>
        #     <p>Here's your detailed resume analysis and compatibility score</p>
        # </div>
        # """, unsafe_allow_html=True)
        
        # Overall Score Display
        overall_score = score_data.get('final_score', 0)
        score_class = "score-card"
        if overall_score < 40:
            score_class += " score-bad"
        elif overall_score < 70:
            score_class += " score-average"
        
        st.markdown(f"""
        <div class="{score_class}">
            <h2>Overall Compatibility Score</h2>
            <h1>{overall_score}%</h1>
            <p>Your resume matches {overall_score}% with the job requirements</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed Breakdown
        col1, col2 = st.columns(2)
        
        # with col1:
        #     st.markdown("### 🎯 Detailed Scores")
            
        #     # Skills Score
        #     skills_score = score_data.get('skills_score', 0)
        #     st.metric("Skills Match", f"{skills_score}%", 
        #              delta=f"{skills_score - 50}% from average" if skills_score != 0 else None)
        #     st.progress(skills_score / 100)
            
        #     # Experience Score
        #     exp_score = score_data.get('experience_score', 0)
        #     st.metric("Experience Match", f"{exp_score}%",
        #              delta=f"{exp_score - 50}% from average" if exp_score != 0 else None)
        #     st.progress(exp_score / 100)
            
        #     # Education Score
        #     edu_score = score_data.get('education_score', 0)
        #     st.metric("Education Match", f"{edu_score}%",
        #              delta=f"{edu_score - 50}% from average" if edu_score != 0 else None)
        #     st.progress(edu_score / 100)
        
        # with col2:
        #     st.markdown("### 📈 Recommendations")
            
        #     # Missing Skills
        #     if 'missing_skills' in score_data:
        #         with st.expander("🔍 Missing Skills", expanded=True):
        #             missing_skills = score_data['missing_skills']
        #             if missing_skills:
        #                 for skill in missing_skills[:5]:  # Show top 5
        #                     st.markdown(f"• **{skill}**")
        #             else:
        #                 st.success("Great! No critical skills missing.")
            
        #     # Improvement Areas
        #     if 'improvement_areas' in score_data:
        #         with st.expander("💡 Improvement Areas", expanded=True):
        #             areas = score_data['improvement_areas']
        #             if areas:
        #                 for area in areas[:3]:  # Show top 3
        #                     st.markdown(f"• {area}")
        #             else:
        #                 st.success("Your resume looks comprehensive!")
            
        #     # Strengths
        #     if 'strengths' in score_data:
        #         with st.expander("✨ Your Strengths", expanded=True):
        #             strengths = score_data['strengths']
        #             if strengths:
        #                 for strength in strengths[:3]:
        #                     st.markdown(f"• {strength}")
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔄 Analyze Another Resume"):
                st.session_state.step = 1
                st.session_state.evaluation_result = None
                st.session_state.session_id = None
                st.rerun()
        
        with col2:
            if overall_score < 80:  # Show enhance option if score is not great
                if st.button("✨ Enhance My Resume"):
                    st.session_state.step = 3
                    st.rerun()
            else:
                st.success("🎉 Great score! Your resume is well-optimized.")
        
        with col3:
            # Download current analysis as JSON
            if st.button("📄 Download Report"):
                json_str = json.dumps(score_data, indent=2)
                st.download_button(
                    label="💾 Download Analysis Report",
                    data=json_str,
                    file_name="resume_analysis_report.json",
                    mime="application/json"
                )

# Step 3: Enhance Resume
elif st.session_state.step == 3:
    if st.session_state.session_id:
        
        # Check if we already have enhanced resume data
        if st.session_state.enhanced_resume_data is None:
            # Enhancement button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Enhance My Resume Now", key="enhance_btn"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        status_text.text("🤖 AI is enhancing your resume...")
                        progress_bar.progress(25)
                        time.sleep(1)
                        
                        # Make API call for enhancement
                        data = {"session_id": st.session_state.session_id}
                        response = requests.post(f"{API_BASE_URL}/enhance", data=data)
                        
                        progress_bar.progress(50)
                        status_text.text("📝 Optimizing content and format...")
                        time.sleep(1)
                        
                        progress_bar.progress(75)
                        status_text.text("🎨 Applying professional formatting...")
                        time.sleep(1)
                        
                        if response.status_code == 200:
                            progress_bar.progress(100)
                            status_text.text("✅ Enhancement complete!")
                            
                            # Store enhanced resume data
                            st.session_state.enhanced_resume_data = response.content
                            st.success("🎉 Your resume has been successfully enhanced!")
                            time.sleep(1)
                            st.rerun()  # Refresh to show the PDF viewer
                            
                        else:
                            st.error(f"❌ Enhancement failed: {response.status_code} - {response.text}")
                            
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Connection error: {str(e)}")
                        st.info("💡 Make sure your FastAPI server is running on http://localhost:8000")
                    except Exception as e:
                        st.error(f"❌ Unexpected error: {str(e)}")
        
        else:
            # Display the enhanced resume with PDF viewer
            st.markdown("### 🎉 Your Enhanced Resume is Ready!")
            
            # Display PDF viewer
            try:
                display_pdf(st.session_state.enhanced_resume_data)
            except Exception as e:
                st.error(f"❌ Error displaying PDF: {str(e)}")
                st.info("💡 Your browser might not support PDF viewing. You can still download the file below.")
            
            # Download section
            st.markdown("""
            <div class="download-section">
                <h2>📥 Download Your Enhanced Resume</h2>
                <p>Your resume has been optimized for better ATS compatibility and enhanced readability</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📥 Download Enhanced Resume",
                    data=st.session_state.enhanced_resume_data,
                    file_name=f"enhanced_resume_{int(time.time())}.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            
            # Additional actions
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Enhance Another Resume"):
                    st.session_state.step = 1
                    st.session_state.evaluation_result = None
                    st.session_state.session_id = None
                    st.session_state.enhanced_resume_data = None
                    st.rerun()
            
            with col2:
                if st.button("← Back to Analysis Results"):
                    st.session_state.step = 2
                    st.rerun()
            
            with col3:
                if st.button("🔄 Re-enhance Resume"):
                    st.session_state.enhanced_resume_data = None
                    st.rerun()
        
        # Back button (only show when not enhanced yet)
        if st.session_state.enhanced_resume_data is None:
            st.markdown("---")
            if st.button("← Back to Results"):
                st.session_state.step = 2
                st.rerun()

# Sidebar with additional info
with st.sidebar:
    st.markdown("### 🎯 How It Works")
    st.markdown("""
    1. **Upload** your resume (PDF/DOC)
    2. **Provide** job posting URL
    3. **Get** AI analysis & score
    4. **Preview** enhanced resume
    5. **Download** optimized version
    """)
    
    st.markdown("### 📊 Features")
    st.markdown("""
    - ATS compatibility check
    - Skills gap analysis
    - Content optimization
    - Professional formatting
    - Keyword enhancement
    - PDF preview
    """)
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Use recent resume versions
    - Provide complete job URLs
    - Review enhanced resume
    - Keep original resume backup
    - Test PDF in different viewers
    """)
    
    st.markdown("---")
    st.markdown("**📧 Need Help?**")
    st.markdown("Contact support for assistance")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Made with ❤️ using Streamlit & FastAPI | AI Resume Analyzer v1.0
</div>
""", unsafe_allow_html=True)