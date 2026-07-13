import streamlit as st
from src.helper import extract_text_from_pdf, ask_gemini
from src.job_api import (
    fetch_joinrise_jobs,
    fetch_jsearch_jobs,
    fetch_linkedin_jobs,
    fetch_naukri_jobs,
)
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="NextHire - AI-Powered Job Portal",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary: #2563EB;
        --primary-dark: #1D4ED8;
        --primary-light: #3B82F6;
        --secondary: #10B981;
        --secondary-dark: #059669;
        --accent: #F59E0B;
        --background: #F8FAFC;
        --surface: #FFFFFF;
        --text-primary: #1E293B;
        --text-secondary: #64748B;
        --text-muted: #94A3B8;
        --border: #E2E8F0;
        --border-light: #F1F5F9;
        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --radius-sm: 6px;
        --radius: 12px;
        --radius-lg: 16px;
        --radius-xl: 24px;
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .stApp {
        background: var(--background);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--border-light);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--text-muted);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    
    /* Navbar */
    .navbar {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        padding: 1rem 2rem;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        box-shadow: var(--shadow-lg);
        backdrop-filter: blur(10px);
    }
    
    .navbar-content {
        max-width: 1400px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .navbar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        text-decoration: none;
    }
    
    .navbar-nav {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-link {
        color: rgba(255, 255, 255, 0.9);
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        padding: 0.5rem 1rem;
        border-radius: var(--radius-sm);
    }
    
    .nav-link:hover {
        color: white;
        background: rgba(255, 255, 255, 0.1);
    }
    
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, var(--primary) 0%, #1E40AF 50%, #1E3A8A 100%);
        padding: 120px 2rem 80px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.5;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .hero h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        line-height: 1.1;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .hero p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.25rem;
        margin-bottom: 2.5rem;
        line-height: 1.6;
        font-weight: 400;
    }
    
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin-top: 3rem;
        flex-wrap: wrap;
    }
    
    .stat-item {
        color: white;
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.95rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Main Container */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Upload Section */
    .upload-section {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 2.5rem;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border);
        margin-bottom: 2rem;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .section-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        border-radius: var(--radius);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
    }
    
    .section-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }
    
    .section-subtitle {
        font-size: 0.95rem;
        color: var(--text-secondary);
        margin: 0;
    }
    
    /* Upload Area */
    .upload-area {
        border: 2px dashed var(--border);
        border-radius: var(--radius-lg);
        padding: 3rem;
        text-align: center;
        background: var(--background);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .upload-area:hover {
        border-color: var(--primary);
        background: rgba(37, 99, 235, 0.02);
    }
    
    .upload-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .upload-text {
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .upload-hint {
        color: var(--text-muted);
        font-size: 0.875rem;
    }
    
    /* Settings Card */
    .settings-card {
        background: var(--background);
        border-radius: var(--radius);
        padding: 1.5rem;
        border: 1px solid var(--border);
    }
    
    .settings-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Buttons */
    .btn-primary {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        padding: 14px 32px;
        border-radius: var(--radius);
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
        width: 100%;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .btn-primary:active {
        transform: translateY(0);
    }
    
    /* Custom File Uploader */
    .stFileUploader > div {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
    }
    
    .stFileUploader > div > div {
        border: 2px dashed var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 3rem 2rem !important;
        background: var(--background) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: var(--primary) !important;
        background: rgba(37, 99, 235, 0.02) !important;
    }
    
    /* Custom Selectbox */
    .stSelectbox > div > div {
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        background: var(--surface) !important;
        padding: 0.5rem !important;
    }
    
    /* Tabs */
    .stTabs {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        margin: 2rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        border-bottom: 2px solid var(--border);
        padding-bottom: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 1.5rem;
        font-weight: 600;
        color: var(--text-secondary);
        border-radius: var(--radius) var(--radius) 0 0;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom: 3px solid var(--primary) !important;
        background: rgba(37, 99, 235, 0.05) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--primary);
        background: rgba(37, 99, 235, 0.05);
    }
    
    /* Job Cards */
    .job-card {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 1.75rem;
        margin: 1rem 0;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .job-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--primary) 0%, var(--secondary) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .job-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-light);
    }
    
    .job-card:hover::before {
        opacity: 1;
    }
    
    .job-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    
    .job-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
    }
    
    .company-name {
        font-size: 1rem;
        font-weight: 600;
        color: var(--primary);
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .job-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .meta-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--text-secondary);
        font-size: 0.9rem;
        background: var(--background);
        padding: 0.5rem 1rem;
        border-radius: var(--radius-sm);
        border: 1px solid var(--border);
    }
    
    .meta-item span:first-child {
        font-size: 1rem;
    }
    
    .job-skills {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .skill-tag {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(37, 99, 235, 0.05) 100%);
        color: var(--primary);
        padding: 0.4rem 0.9rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(37, 99, 235, 0.2);
        transition: all 0.2s ease;
    }
    
    .skill-tag:hover {
        background: var(--primary);
        color: white;
    }
    
    .apply-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: var(--radius);
        text-decoration: none;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .apply-btn:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
    }
    
    /* Result Cards */
    .result-card {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .result-card h3 {
        color: var(--text-primary);
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* Success/Warning Boxes */
    .success-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: var(--secondary-dark);
        padding: 1.25rem 1.75rem;
        border-radius: var(--radius);
        text-align: center;
        font-weight: 600;
        font-size: 1.05rem;
        margin: 2rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #B45309;
        padding: 1.25rem 1.75rem;
        border-radius: var(--radius);
        text-align: center;
        font-weight: 600;
        font-size: 1.05rem;
    }
    
    /* Premium Sources */
    .premium-card {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.02) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: var(--radius-lg);
        padding: 1.75rem;
        margin: 1rem 0;
    }
    
    .premium-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(245, 158, 11, 0.2);
    }
    
    .premium-icon {
        font-size: 1.5rem;
    }
    
    .premium-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }
    
    .premium-badge {
        background: linear-gradient(135deg, var(--accent) 0%, #D97706 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: auto;
    }
    
    /* Footer */
    .footer {
        background: var(--text-primary);
        color: white;
        padding: 3rem 2rem 2rem;
        margin-top: 4rem;
    }
    
    .footer-content {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .footer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .footer-section h3 {
        color: white;
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }
    
    .footer-section p, .footer-section a {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.8;
        font-size: 0.95rem;
    }
    
    .footer-section a {
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    .footer-section a:hover {
        color: var(--primary-light);
    }
    
    .footer-bottom {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 2rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
    }
    
    /* Feature Cards */
    .feature-card {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 2rem;
        text-align: center;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-light);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.25rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
    }
    
    .feature-desc {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Loading Animation */
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.95);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 2000;
    }
    
    .spinner {
        width: 60px;
        height: 60px;
        border: 4px solid var(--border);
        border-top-color: var(--primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Skeleton Loading */
    .skeleton {
        background: linear-gradient(90deg, var(--border-light) 25%, var(--background) 50%, var(--border-light) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: var(--radius);
    }
    
    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Keyword Chip */
    .keyword-chip {
        display: inline-block;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1rem;
        margin: 1rem 0;
        box-shadow: var(--shadow);
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: var(--text-secondary);
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        opacity: 0.5;
    }
    
    .empty-state-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
    }
    
    .empty-state-desc {
        font-size: 1rem;
        line-height: 1.6;
        max-width: 400px;
        margin: 0 auto;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero h1 {
            font-size: 2.5rem;
        }
        
        .hero-stats {
            gap: 2rem;
        }
        
        .stat-number {
            font-size: 2rem;
        }
        
        .main-container {
            padding: 1rem;
        }
        
        .upload-section {
            padding: 1.5rem;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

# Navbar
st.markdown(
    """
<div class="navbar">
    <div class="navbar-content">
        <a href="#" class="navbar-brand">
            <span style="font-size: 2rem;">🎯</span>
            <span>NextHire</span>
        </a>
        <div class="navbar-nav">
            <a href="#upload" class="nav-link">Home</a>
            <a href="#features" class="nav-link">Features</a>
            <a href="#" class="nav-link">Jobs</a>
            <a href="#" class="nav-link">About</a>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Hero Section
st.markdown(
    """
<div class="hero">
    <div class="hero-content">
        <h1>🚀 AI-Powered Career Transformation</h1>
        <p>Upload your resume and let our intelligent system analyze your skills, identify gaps, and match you with the perfect job opportunities.</p>
        <div class="hero-stats">
            <div class="stat-item">
                <span class="stat-number">500+</span>
                <span class="stat-label">Jobs Available</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">95%</span>
                <span class="stat-label">Match Accuracy</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">10K+</span>
                <span class="stat-label">Career Growth</span>
            </div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Main Container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Upload Section
with st.container():
    st.markdown(
        """
    <div class="upload-section" id="upload">
        <div class="section-header">
            <div class="section-icon">📄</div>
            <div>
                <h2 class="section-title">Upload Your Resume</h2>
                <p class="section-subtitle">Get personalized job recommendations based on your skills and experience</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Drag & drop your PDF resume here or click to browse",
            type=["pdf"],
            label_visibility="collapsed",
        )

    with col2:
        st.markdown("### ⚙️ Job Preferences")
        location = st.selectbox(
            "Preferred Location",
            ["India", "USA", "UK", "Remote", "All"],
            index=0,
            label_visibility="collapsed",
        )
        st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    with st.spinner("🔄 Extracting text from resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("🔄 Analyzing resume with AI..."):
        summary = ask_gemini(
            f"Summarize the following resume highlighting the key skills, experiences, and education in a clear, concise format:\n\n{resume_text}",
            max_tokens=500,
        )

    with st.spinner("🔄 Identifying skill gaps..."):
        skillgaps = ask_gemini(
            f"Based on the following resume, identify skill gaps and areas for improvement. Format as bullet points:\n\n{resume_text}",
            max_tokens=400,
        )

    with st.spinner("🔄 Creating personalized roadmap..."):
        roadmap = ask_gemini(
            f"Based on the resume and skill gaps, create a learning roadmap with specific steps:\n\nResume:\n{resume_text}\n\nSkill Gaps:\n{skillgaps}",
            max_tokens=400,
        )

    # Results Section
    st.markdown("---")
    st.markdown(
        '<h2 style="text-align: center; color: var(--text-primary); margin: 2rem 0 1rem;">📊 Your Career Analysis Report</h2>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📝 Resume Summary",
            "🎯 Skill Gaps",
            "🗺️ Learning Roadmap",
            "💼 Job Opportunities",
        ]
    )

    with tab1:
        st.markdown(
            f"""
        <div class="result-card">
            <h3>📝 Professional Summary</h3>
            {summary}
        </div>
        """,
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            f"""
        <div class="result-card">
            <h3>🎯 Identified Skill Gaps</h3>
            {skillgaps}
        </div>
        """,
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown(
            f"""
        <div class="result-card">
            <h3>🗺️ Your Learning Journey</h3>
            {roadmap}
        </div>
        """,
            unsafe_allow_html=True,
        )

    with tab4:
        with st.spinner("🔄 Generating search keywords..."):
            keywords = ask_gemini(
                f"Based on this resume summary, suggest 3-5 job search keywords. Return only comma-separated keywords:\n\n{summary}",
                max_tokens=50,
            )
            search_query = keywords.replace("\n", "").strip()

        st.markdown(
            f"""
        <div style="text-align: center; margin: 2rem 0;">
            <p style="color: var(--text-secondary); font-size: 1rem; margin-bottom: 0.5rem;">AI-Suggested Search Keywords</p>
            <span class="keyword-chip">🔍 {search_query}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

        job_col1, job_col2 = st.columns([2, 1])

        with job_col1:
            st.markdown("### 💼 Matching Opportunities")
            st.markdown(
                "<p style='color: var(--text-secondary); font-size: 0.95rem;'>Based on your profile, we found these opportunities for you:</p>",
                unsafe_allow_html=True,
            )

            with st.spinner("Fetching relevant jobs..."):
                jobs = fetch_joinrise_jobs(search_query, location, row=15)

            if jobs:
                for job in jobs:
                    skills = (
                        ", ".join(job.get("skills", [])[:3])
                        if job.get("skills")
                        else ""
                    )
                    st.markdown(
                        f"""
                    <div class="job-card">
                        <div class="job-header">
                            <div>
                                <h3 class="job-title">{job.get("title", "N/A")}</h3>
                                <p class="company-name">🏢 {job.get("companyName", "N/A")}</p>
                            </div>
                        </div>
                        <div class="job-meta">
                            <div class="meta-item">
                                <span>📍</span>
                                <span>{job.get("location", "N/A")}</span>
                            </div>
                            <div class="meta-item">
                                <span>💼</span>
                                <span>{job.get("type", "N/A")}</span>
                            </div>
                            <div class="meta-item">
                                <span>📊</span>
                                <span>{job.get("seniority", "N/A")}</span>
                            </div>
                        </div>
                        {f'<div class="job-skills"><span class="skill-tag">🛠️ {skills}</span></div>' if skills else ""}
                        <a href="{job.get("link", "#")}" target="_blank" class="apply-btn">Apply Now →</a>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    """
                <div class="empty-state">
                    <div class="empty-state-icon">🔍</div>
                    <h3 class="empty-state-title">No Jobs Found</h3>
                    <p class="empty-state-desc">We couldn't find matching jobs. Try uploading a different resume or adjusting your preferences.</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        with job_col2:
            st.markdown("### 🔗 Premium Sources")
            st.markdown(
                "<p style='color: var(--text-muted); font-size: 0.875rem;'>Powered by LinkedIn & Naukri</p>",
                unsafe_allow_html=True,
            )

            st.markdown(
                """
            <div class="premium-card">
                <div class="premium-header">
                    <span class="premium-icon">💼</span>
                    <h4 class="premium-title">LinkedIn Jobs</h4>
                    <span class="premium-badge">PRO</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            linkedin_jobs = fetch_linkedin_jobs(search_query, location, row=3)
            if linkedin_jobs:
                for job in linkedin_jobs[:3]:
                    st.markdown(
                        f"- [{job.get('title', 'N/A')}]({job.get('link', '#')})"
                    )
            else:
                st.markdown("""
                <p style='color: var(--text-muted); font-size: 0.875rem; text-align: center;'>
                    ⚠️ Requires paid Apify subscription
                </p>
                """)

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(
                """
            <div class="premium-card">
                <div class="premium-header">
                    <span class="premium-icon">🌐</span>
                    <h4 class="premium-title">Naukri Jobs</h4>
                    <span class="premium-badge">PRO</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            naukri_jobs = fetch_naukri_jobs(search_query, location, row=3)
            if naukri_jobs:
                for job in naukri_jobs[:3]:
                    st.markdown(f"- [{job.get('title', 'N/A')}]({job.get('url', '#')})")
            else:
                st.markdown("""
                <p style='color: var(--text-muted); font-size: 0.875rem; text-align: center;'>
                    ⚠️ Requires paid Apify subscription
                </p>
                """)

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        """
    <div class="success-box">
        ✅ Resume Analysis Complete! Your personalized career roadmap is ready.
    </div>
    """,
        unsafe_allow_html=True,
    )

else:
    # Features Section
    st.markdown('<div id="features"></div>', unsafe_allow_html=True)
    st.markdown(
        '<h2 style="text-align: center; color: var(--text-primary); margin: 3rem 0 2rem;">✨ Key Features</h2>',
        unsafe_allow_html=True,
    )

    feat_col1, feat_col2, feat_col3 = st.columns(3)

    with feat_col1:
        st.markdown(
            """
        <div class="feature-card">
            <span class="feature-icon">📝</span>
            <h3 class="feature-title">Smart Resume Analysis</h3>
            <p class="feature-desc">AI-powered extraction of key skills, experiences, and qualifications from your resume</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with feat_col2:
        st.markdown(
            """
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <h3 class="feature-title">Skill Gap Detection</h3>
            <p class="feature-desc">Identify missing skills and get actionable recommendations for career growth</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with feat_col3:
        st.markdown(
            """
        <div class="feature-card">
            <span class="feature-icon">💼</span>
            <h3 class="feature-title">Job Matching</h3>
            <p class="feature-desc">Get personalized job recommendations based on your unique profile and preferences</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Empty State
    st.markdown(
        """
    <div class="empty-state" style="margin-top: 3rem;">
        <div class="empty-state-icon">👋</div>
        <h2 class="empty-state-title">Ready to Transform Your Career?</h2>
        <p class="empty-state-desc">Upload your resume above to get started with AI-powered job recommendations and personalized career insights.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Close main container
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
<div class="footer">
    <div class="footer-content">
        <div class="footer-grid">
            <div class="footer-section">
                <h3>🎯 NextHire</h3>
                <p>AI-Powered Job Recommendation System that helps you discover the perfect career opportunities.</p>
            </div>
            <div class="footer-section">
                <h3>Quick Links</h3>
                <p><a href="#">Home</a><br>
                <a href="#features">Features</a><br>
                <a href="#">About Us</a><br>
                <a href="#">Contact</a></p>
            </div>
            <div class="footer-section">
                <h3>Resources</h3>
                <p><a href="#">Help Center</a><br>
                <a href="#">Privacy Policy</a><br>
                <a href="#">Terms of Service</a><br>
                <a href="#">API Documentation</a></p>
            </div>
            <div class="footer-section">
                <h3>Connect</h3>
                <p><a href="#">LinkedIn</a><br>
                <a href="#">Twitter</a><br>
                <a href="#">GitHub</a><br>
                <a href="#">Newsletter</a></p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2024 NextHire. All rights reserved. Built with ❤️ for job seekers everywhere.</p>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)
