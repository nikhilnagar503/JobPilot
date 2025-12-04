import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import logging
# from src.google_oauth import GoogleOAuth
import gspread



from src.job_scraper import JobScraper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()


# --- Streamlit UI Components ---
def main():
    st.set_page_config(
        page_title="AI Job Assistant",
        layout="wide",
        page_icon="💼"
    )
    # load_css()
    
    # Sidebar navigation
    st.sidebar.title("💼 AI Job Assistant")
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Dashboard", "🔍 Job Search"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    # st.sidebar.markdown("### Settings")
    # json_credentials_file = st.sidebar.text_input(
    #     "Google Sheets Credentials Path",
    #     "./Data/steam-bonbon-451912-d7-24cde95bb4e7.json",
    #     help="Path to your Google Sheets service account JSON file"
    # )
    # spreadsheet_id = st.sidebar.text_input(
    #     "Google Sheet ID",
    #     help="1Wcq6mmLmwWHHxtJN_B2RzZWSzRN-cfJkGjiLzDpm0ys"
    # )
    
    if page == "🏠 Dashboard":
        render_dashboard()
    elif page == "🔍 Job Search":
        render_job_search()
    # elif page == "📝 Cover Letter":
    #     render_cover_letter_generator()
    # elif page == "✉️ Email Application":
    #     render_email_application()
    # elif page == "📊 Application Tracker":
    #     render_application_tracker()
    #     # render_application_tracker(json_credentials_file, spreadsheet_id)
    # elif page == "⚙️ Settings":
    #     render_settings()  # Add this new condition



def render_dashboard():
    st.title("AI Job Assistant Dashboard")
    st.markdown("""
    Welcome to your AI-powered job application assistant! This tool helps you:
    
    - 🔍 Search for relevant job opportunities
    - 📝 Generate personalized cover letters
    - ✉️ Send professional application emails
    - 📊 Track your application progress
    
    Get started by selecting a page from the sidebar.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jobs Found", "25", "+5 from last week")
    with col2:
        st.metric("Applications Sent", "8", "3 pending")
    with col3:
        st.metric("Interview Rate", "25%", "2 of 8")
    
    st.markdown("---")
    st.subheader("Recent Activity")
    st.write("Your recent job application activity will appear here.")


def render_job_search():
    st.title("Job Search")
    st.markdown("Find your next career opportunity using our AI-powered job search.")
    
    with st.expander("🔍 Search Filters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            job_titles = st.text_input(
                "Job Titles (comma separated)",
                "Data Scientist, Machine Learning Engineer",
                help="Enter multiple job titles separated by commas"
            )
        with col2:
            location = st.text_input("Location", "London")
    
    if st.button("Search Jobs", key="search_jobs"):
        with st.spinner("🔍 Searching for jobs..."):
            job_list = [title.strip() for title in job_titles.split(",")]
            
            try:
                scraper = JobScraper(job_titles=job_list, location=location)
                scraper.scrape_jobs()
                jobs = scraper.get_saved_jobs()
                
                if not jobs.empty:
                    st.session_state.job_results = jobs
                    st.success(f"🎉 Found {len(jobs)} jobs!")
                    
                    # Display jobs in cards
                    for idx, job in jobs.iterrows():
                        with st.container():
                            st.markdown(f"""
                            <div class="job-card">
                                <h3>{job['job_title']}</h3>
                                <p><strong>Company:</strong> {job['company']}</p>
                                <p><strong>Location:</strong> {job['location']}</p>
                                <p><strong>Salary:</strong> £{job['salary_min']} - £{job['salary_max']}</p>
                                <a href="{job['apply_link']}" target="_blank">View Job</a>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("No jobs found. Try different search terms.")
            except Exception as e:
                st.error(f"Error searching for jobs: {str(e)}")
                

if __name__ == "__main__":
    main()
    
    