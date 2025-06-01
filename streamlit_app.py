# streamlit_app.py
import streamlit as st
import pandas as pd
import json
import plotly.express as px
from collections import Counter
from typing import List, Dict, Any, Optional, Union
import numpy as np
import tempfile
import os
import datetime
from pathlib import Path
from cv_analyser import CVAnalyzer
from groq_search import AICandidateSearch
from ai_matching import AdvancedCandidateMatcher, CandidateRanker, BackgroundChecker
import time
import asyncio
from dataclasses import asdict

# Load the dataset
@st.cache_data
def load_data():
    with open('dataset.json', 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

def get_top_skills(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Extract top N skills from the dataset"""
    all_skills = [skill for sublist in df['skills'].dropna() for skill in sublist]
    skill_counts = Counter(all_skills)
    return pd.DataFrame(skill_counts.most_common(top_n), columns=['Skill', 'Count'])

def get_seniority_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Get distribution of seniority levels"""
    return df['seniority'].value_counts().reset_index().rename(columns={'count': 'count', 'index': 'seniority'})

def get_experience_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Get distribution of experience years"""
    return df['experience_years'].value_counts().reset_index().rename(columns={'experience_years': 'experience', 'count': 'count'})

def get_employment_type_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Get distribution of employment types"""
    return df['employment_type'].value_counts().reset_index()

def get_skills_by_seniority(df: pd.DataFrame, seniority: str) -> pd.DataFrame:
    """Get top skills for a specific seniority level"""
    filtered_df = df[df['seniority'] == seniority]
    all_skills = [skill for sublist in filtered_df['skills'].dropna() for skill in sublist]
    skill_counts = Counter(all_skills)
    return pd.DataFrame(skill_counts.most_common(10), columns=['Skill', 'Count'])

# Function to load local CSS

# Function to load local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def setup_page():
    # Page Configuration (must be the first Streamlit command)
    st.set_page_config(
        page_title="NaukriAI Dashboard",
        page_icon="🚀", # You can use an emoji or a path to an .ico file
        layout="wide", # Can be "centered" or "wide"
        initial_sidebar_state="expanded" # Can be "auto", "expanded", "collapsed"
    )

def load_env():
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

def main():
    # Load data
    df = load_data()
    
    # Get app_mode from session state
    app_mode = st.session_state.get('app_mode', 'Home')
    
    # --- Main Page Content ---
    if app_mode == "Home" or app_mode is None:
        st.title("Welcome to NaukriAI Dashboard 🚀")
        st.markdown("### Your AI-Powered Hiring Co-Pilot")

        st.markdown("---")
        st.subheader("Key Metrics")
        
        # Calculate metrics
        total_candidates = len(df)
        seniority_dist = get_seniority_distribution(df)
        top_skills = get_top_skills(df)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f"""
                <div class="custom-card">
                    <h3>Total Candidates</h3>
                    <p style="font-size: 2em; color: #4a4aff; font-weight: bold;">{total_candidates:,}</p>
                </div>
                """, unsafe_allow_html=True
            )
        with col2:
            # Get senior count safely
            senior_count = seniority_dist[seniority_dist['seniority'] == 'senior']['count'].iloc[0] if not seniority_dist[seniority_dist['seniority'] == 'senior'].empty else 0
            st.markdown(
                f"""
                <div class="custom-card">
                    <h3>Senior Candidates</h3>
                    <p style="font-size: 2em; color: #4a4aff; font-weight: bold;">{senior_count}</p>
                </div>
                """, unsafe_allow_html=True
            )
        with col3:
            top_skill = top_skills.iloc[0]['Skill'] if not top_skills.empty else "N/A"
            top_skill_count = top_skills.iloc[0]['Count'] if not top_skills.empty else 0
            st.markdown(
                f"""
                <div class="custom-card">
                    <h3>Top Skill</h3>
                    <p style="font-size: 1.5em; color: #4a4aff; font-weight: bold; margin: 0;">{top_skill}</p>
                    <p style="font-size: 1em; color: #b0b0ff; margin: 0;">{top_skill_count} candidates</p>
                </div>
                """, unsafe_allow_html=True
            )
        
        # Add some space
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # First row of charts
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Top 10 Skills in Demand")
            fig = px.bar(
                top_skills.head(10), 
                x='Count', 
                y='Skill',
                orientation='h',
                color='Count',
                color_continuous_scale='blues',
                labels={'Count': 'Number of Candidates', 'Skill': 'Skill'}
            )
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Seniority Distribution")
            fig = px.pie(
                seniority_dist, 
                values='count', 
                names='seniority',
                hole=0.4,
                color='seniority',
                color_discrete_map={
                    'junior': '#4a4aff',
                    'midlevel': '#6c6cff',
                    'senior': '#8e8eff'
                }
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
        
        # Second row of charts
        st.subheader("Experience Level Distribution")
        exp_dist = get_experience_distribution(df)
        if not exp_dist.empty:
            fig = px.bar(
                exp_dist, 
                x='experience', 
                y='count',
                color='experience',
                color_discrete_sequence=px.colors.sequential.Blues_r,
                labels={'experience': 'Experience Level', 'count': 'Number of Candidates'},
                category_orders={"experience": sorted(exp_dist['experience'].unique())}
            )
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        # Third row - skills by seniority
        st.subheader("Top Skills by Seniority Level")
        seniority_levels = df['seniority'].unique()
        cols = st.columns(len(seniority_levels))
        
        for idx, level in enumerate(seniority_levels):
            with cols[idx]:
                st.markdown(f"**{level.capitalize()}**")
                skills_df = get_skills_by_seniority(df, level)
                if not skills_df.empty:
                    fig = px.bar(
                        skills_df, 
                        x='Count', 
                        y='Skill',
                        orientation='h',
                        color='Count',
                        color_continuous_scale='blues',
                        height=300
                    )
                    fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
                    st.plotly_chart(fig, use_container_width=True)

    elif app_mode == "CV Analyser":
        st.header("CV Analyser")
        st.markdown("Upload your CV (PDF or DOCX) to get detailed analysis.")
        
        uploaded_file = st.file_uploader("Choose a CV file", type=["pdf", "docx", "txt"])
        
        if uploaded_file is not None:
            # Display file details
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": f"{uploaded_file.size / 1024:.2f} KB"}
            st.write("File uploaded successfully!")
            st.write(file_details)
            
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                # Initialize the CV Analyzer
                analyzer = CVAnalyzer()
                
                # Show a loading spinner while analyzing
                with st.spinner('Analyzing your CV...'):
                    # Analyze the CV
                    result = analyzer.analyze_cv(tmp_file_path)
                
                if result['status'] == 'success':
                    analysis = result['analysis']
                    
                    # Display the analysis results with enhanced recruiter-focused sections
                    st.subheader("📊 CV Analysis Report")
                    
                    # Overall Assessment
                    if 'overall_score' in analysis:
                        score = analysis['overall_score']
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.metric(label="Overall Fit Score", value=f"{score}%")
                        with col2:
                            if score >= 80:
                                st.success("🔥 Strong match for technical roles")
                            elif score >= 60:
                                st.warning("🔄 Potential match with some upskilling")
                            else:
                                st.info("📉 May require significant experience or skill development")
                    
                    st.markdown("---")
                    
                    # Candidate Snapshot
                    st.subheader("👤 Candidate Snapshot")
                    if 'candidate_summary' in analysis:
                        summary = analysis['candidate_summary']
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("##### 🔍 Basic Info")
                            st.markdown(f"**Name:** {summary.get('name', 'N/A')}")
                            st.markdown(f"**Current Position:** {summary.get('current_position', 'N/A')}")
                            st.markdown(f"**Experience:** {summary.get('total_experience', 'N/A')}")
                        with col2:
                            st.markdown("##### 📍 Location & Availability")
                            st.markdown(f"**Location:** {summary.get('location', 'N/A')}")
                            st.markdown(f"**Notice Period:** {summary.get('notice_period', 'Not specified')}")
                            st.markdown(f"**Employment Type:** {summary.get('employment_type', 'Not specified')}")
                        with col3:
                            st.markdown("##### 🎓 Education")
                            if 'education' in summary and summary['education']:
                                for edu in summary['education'][:2]:  # Show top 2 education entries
                                    st.markdown(f"- {edu}")
                            else:
                                st.markdown("No education information provided")
                    
                    # Core Competencies
                    st.markdown("---")
                    st.subheader("💼 Core Competencies")
                    
                    if 'skills' in analysis and analysis['skills']:
                        skills = analysis['skills']
                        
                        # Categorize skills
                        tech_skills = [s for s in skills if any(tech in s.lower() for tech in ['python', 'java', 'c++', 'javascript', 'sql', 'cloud', 'aws', 'azure', 'docker', 'kubernetes', 'ml', 'ai', 'data'])]
                        soft_skills = [s for s in skills if s.lower() in ['leadership', 'communication', 'teamwork', 'problem solving', 'time management', 'adaptability']]
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("##### 🛠️ Technical Skills")
                            for skill in tech_skills[:8]:  # Show top 8 technical skills
                                st.markdown(f"- {skill}")
                        with col2:
                            st.markdown("##### 🤝 Soft Skills")
                            for skill in soft_skills or ["Not explicitly mentioned"]:
                                st.markdown(f"- {skill}")
                    
                    # Work Experience Analysis
                    st.markdown("---")
                    st.subheader("📈 Work Experience Analysis")
                    
                    # Try to extract experience from different possible fields
                    experience_data = []
                    
                    # Check standard experience field first
                    if 'experience' in analysis and analysis['experience']:
                        experience_data = analysis['experience']
                    # Check if experience is in candidate_summary
                    elif 'candidate_summary' in analysis and 'experience' in analysis['candidate_summary']:
                        experience_data = analysis['candidate_summary']['experience']
                    # Check if experience is embedded in the text
                    elif 'text' in analysis:
                        # Try to extract experience from raw text (simplified example)
                        import re
                        text = analysis.get('text', '')
                        # Look for common work experience patterns
                        experience_matches = re.finditer(r'([A-Za-z]+\s+\d{4})\s*-\s*([A-Za-z]+\s+\d{4}|Present).*?\n(.*?)(?=\n\w|$)', 
                                                    text, re.DOTALL)
                        for match in experience_matches:
                            start_date, end_date, details = match.groups()
                            experience_data.append({
                                'duration': f"{start_date} - {end_date}",
                                'details': details.strip()
                            })
                    
                    if experience_data:
                        for idx, job in enumerate(experience_data[:3]):  # Show top 3 experiences
                            with st.expander(f"{job.get('title', 'Role')} at {job.get('company', 'Company')} ({job.get('duration', 'N/A')})"):
                                # Display role and company if available
                                if 'title' in job or 'company' in job:
                                    st.markdown(f"**Role:** {job.get('title', 'Not specified')}")
                                    st.markdown(f"**Company:** {job.get('company', 'Not specified')}")
                                
                                # Display duration if available
                                if 'duration' in job:
                                    st.markdown(f"**Duration:** {job['duration']}")
                                
                                # Display responsibilities
                                st.markdown("**Key Responsibilities:**")
                                if 'responsibilities' in job and job['responsibilities']:
                                    for resp in job['responsibilities'][:5]:  # Show top 5 responsibilities
                                        st.markdown(f"- {resp}")
                                elif 'details' in job:
                                    # Try to extract bullet points from details
                                    details = job['details'].split('\n')
                                    for detail in details[:5]:  # Show top 5 details
                                        if detail.strip():
                                            st.markdown(f"- {detail.strip()}")
                                else:
                                    st.markdown("- No specific responsibilities mentioned")
                                
                                # Display achievements if available
                                if 'achievements' in job and job['achievements']:
                                    st.markdown("**Key Achievements:**")
                                    for ach in job['achievements'][:3]:  # Show top 3 achievements
                                        st.markdown(f"- ✅ {ach}")
                    else:
                        st.warning("No detailed work experience found in the CV. Here's what we found in the text:")
                        # Show raw text analysis as fallback
                        if 'text' in analysis:
                            text = analysis['text']
                            # Look for any company names or roles that might indicate experience
                            import re
                            # Look for common work-related terms
                            work_terms = ['worked at', 'experience at', 'intern at', 'role at', 'position at', 'bladexlab']
                            found_terms = [term for term in work_terms if term.lower() in text.lower()]
                            if found_terms:
                                st.info(f"Found potential work experience mentions: {', '.join(found_terms)}")
                                # Show context around these terms
                                for term in found_terms:
                                    idx = text.lower().find(term.lower())
                                    if idx > 0:
                                        context = text[max(0, idx-50):min(len(text), idx+100)]
                                        st.text(f"...{context}...")
                                        st.markdown("---")
                    
                    # Strengths & Development Areas
                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🌟 Key Strengths")
                        if 'strengths' in analysis and analysis['strengths']:
                            for strength in analysis['strengths'][:5]:
                                st.markdown(f"- ✅ {strength}")
                        else:
                            st.info("No specific strengths identified")
                    
                    with col2:
                        st.subheader("📈 Development Areas")
                        if 'areas_for_improvement' in analysis and analysis['areas_for_improvement']:
                            for area in analysis['areas_for_improvement'][:5]:
                                st.markdown(f"- 🔄 {area}")
                        else:
                            st.info("No specific development areas identified")
                    
                    # Recruiter's Notes
                    st.markdown("---")
                    st.subheader("📝 Recruiter's Notes")
                    
                    if 'recommendation' in analysis:
                        rec = analysis['recommendation']
                        
                        st.markdown("##### 🎯 Recommended Roles")
                        roles = rec.get('suggested_roles', [])
                        if roles:
                            st.write(", ".join([f"`{role}`" for role in roles]))
                        else:
                            st.info("No specific role recommendations available")
                        
                        st.markdown("##### 💰 Salary Benchmark")
                        if 'suggested_compensation_range' in rec:
                            comp = rec['suggested_compensation_range']
                            st.markdown(f"**Range:** {comp.get('currency', '$')}{comp.get('min', 'N/A')} - {comp.get('currency', '$')}{comp.get('max', 'N/A')} per year")
                        else:
                            st.info("Salary benchmark not available")
                        
                        st.markdown("##### 📋 Interview Focus Areas")
                        if 'interview_focus_areas' in rec and rec['interview_focus_areas']:
                            for area in rec['interview_focus_areas']:
                                st.markdown(f"- {area}")
                        else:
                            st.markdown("1. Technical skills verification")
                            st.markdown("2. Problem-solving approach")
                            st.markdown("3. Cultural fit assessment")
                        
                        if 'reasoning' in rec:
                            st.markdown("##### 📝 Additional Notes")
                            st.info(rec['reasoning'])
                
                else:
                    st.error(f"Error analyzing CV: {result.get('message', 'Unknown error')}")
                
            except Exception as e:
                st.error(f"An error occurred while analyzing the CV: {str(e)}")
            finally:
                # Clean up the temporary file
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass
            # To read file as bytes:
            # bytes_data = uploaded_file.getvalue()
            # st.write(bytes_data)

            # To convert to a string based IO:
            # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            # st.write(stringio)

            # To read file as string:
            # string_data = stringio.read()
            # st.write(string_data)

            # Can be used wherever a "file-like" object is accepted:
            # dataframe = pd.read_csv(uploaded_file)
            # st.write(dataframe)
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            # Placeholder for actual CV analysis logic
            if st.button("Analyse CV"):
                with st.spinner("Analysing your CV..."):
                    # Simulate analysis
                    import time
                    time.sleep(3)
                    st.subheader("Analysis Results (Example)")
                    st.markdown(
                        """
                        <div class="custom-card">
                            <h4>Overall Score: 85%</h4>
                            <p><strong>Strengths:</strong> Strong technical skills, good project experience.</p>
                            <p><strong>Areas for Improvement:</strong> Keywords for 'Data Science' could be enhanced.</p>
                        </div>
                        """, unsafe_allow_html=True
                    )


    elif app_mode == "Market Insights":
        st.header("Market Insights")
        
        # Load data
        df = load_data()
        
        # Top Skills Analysis
        st.subheader("Top Skills Analysis")
        top_n = st.slider("Number of top skills to show:", 5, 20, 10, 1)
        
        # Get top skills
        top_skills = get_top_skills(df, top_n)
        
        # Create two columns for the chart and data
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Horizontal bar chart for top skills
            fig = px.bar(
                top_skills, 
                x='Count', 
                y='Skill',
                orientation='h',
                color='Count',
                color_continuous_scale='blues',
                labels={'Count': 'Number of Candidates', 'Skill': 'Skill'},
                title=f'Top {top_n} Most Common Skills'
            )
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Display the raw data
            st.markdown("### Skill Counts")
            st.dataframe(
                top_skills,
                column_config={
                    "Skill": "Skill",
                    "Count": st.column_config.NumberColumn("Count", format="%d")
                },
                hide_index=True,
                use_container_width=True
            )
        
        # Seniority Analysis
        st.subheader("Seniority Level Analysis")
        seniority_dist = get_seniority_distribution(df)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Pie chart for seniority distribution
            fig = px.pie(
                seniority_dist, 
                values='count', 
                names='seniority',
                title='Seniority Distribution',
                hole=0.4,
                color='seniority',
                color_discrete_map={
                    'junior': '#4a4aff',
                    'midlevel': '#6c6cff',
                    'senior': '#8e8eff'
                }
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Bar chart for experience years
            exp_dist = get_experience_distribution(df)
            if not exp_dist.empty:
                fig = px.bar(
                    exp_dist, 
                    x='experience', 
                    y='count',
                    title='Experience Level Distribution',
                    color='experience',
                    color_discrete_sequence=px.colors.sequential.Blues_r,
                    labels={'experience': 'Experience Level', 'count': 'Number of Candidates'},
                    category_orders={"experience": sorted(exp_dist['experience'].unique())}
                )
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title=None)
                st.plotly_chart(fig, use_container_width=True)
        
        # Create tabs for each seniority level
        seniority_levels = df['seniority'].unique()
        tabs = st.tabs([f"{level.capitalize()}" for level in seniority_levels])
        
        for idx, level in enumerate(seniority_levels):
            with tabs[idx]:
                skills_df = get_skills_by_seniority(df, level)
                if not skills_df.empty:
                    fig = px.bar(
                        skills_df, 
                        x='Count', 
                        y='Skill',
                        orientation='h',
                        color='Count',
                        color_continuous_scale='blues',
                        title=f'Top Skills for {level.capitalize()} Candidates',
                        labels={'Count': 'Number of Candidates', 'Skill': 'Skill'}
                    )
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
        
        # Employment Type Analysis
        st.subheader("Employment Type Analysis")
        emp_type_dist = get_employment_type_distribution(df)
        
        if not emp_type_dist.empty:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.pie(
                    emp_type_dist, 
                    values='count', 
                    names='employment_type',
                    title='Employment Type Distribution',
                    hole=0.4,
                    color='employment_type',
                    color_discrete_sequence=px.colors.sequential.Blues
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### Employment Type Counts")
                st.dataframe(
                    emp_type_dist.rename(columns={'index': 'Employment Type', 'count': 'Count'}),
                    column_config={
                        "Employment Type": "Employment Type",
                        "Count": st.column_config.NumberColumn("Count", format="%d")
                    },
                    hide_index=True,
                    use_container_width=True
                )

def display_ai_candidate_search():
    st.header("🔍 AI-Powered Candidate Search")
    st.markdown("""
    Search for candidates using natural language queries. The AI will understand your requirements 
    and find the best matching candidates from the database.
    """)
    
    # Load the full dataset
    try:
        with open('dataset.json', 'r') as f:
            full_dataset = json.load(f)
    except Exception as e:
        st.error(f"Failed to load candidate database: {str(e)}")
        return
    
    # Initialize the search
    if 'searcher' not in st.session_state:
        st.session_state.searcher = AICandidateSearch()
    
    # Search input
    query = st.text_area("Describe your ideal candidate:", 
                        placeholder="e.g., 'Senior Python developer with 5+ years of experience in machine learning and cloud technologies")
    
    if st.button("Search Candidates") and query:
        with st.spinner('Searching for the best candidates...'):
            try:
                # Search for candidates
                results = st.session_state.searcher.search_candidates(query)
                
                if not results:
                    st.warning("No matching candidates found. Try broadening your search criteria.")
                    return
                
                # Find complete profiles from the full dataset
                matched_profiles = []
                for result in results:
                    # The result might be the candidate directly or have a 'candidates' key
                    candidate_data = result if isinstance(result, dict) else {}
                    if 'candidates' in result and isinstance(result['candidates'], list):
                        candidate_data = result['candidates'][0] if result['candidates'] else {}
                    
                    # Find the full profile by name
                    full_profile = next((p for p in full_dataset if p.get('name') == candidate_data.get('name')), None)
                    if full_profile:
                        # Add the reason from the search result
                        full_profile['_match_reason'] = candidate_data.get('reason', 'No reason provided')
                        matched_profiles.append(full_profile)
                
                st.session_state.search_results = matched_profiles
                
            except Exception as e:
                st.error(f"An error occurred during the search: {str(e)}")
    
    # Display search results if available
    if 'search_results' in st.session_state and st.session_state.search_results:
        results = st.session_state.search_results
        
        # Display each candidate in a card format
        for i, candidate in enumerate(results):
            with st.container(border=True):
                # Header with name and basic info
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    # Profile picture placeholder with first letter of name
                    name = candidate.get('name', 'U')
                    first_letter = name[0].upper()
                    st.markdown(f"""
                        <div style='width: 60px; height: 60px; border-radius: 50%; 
                        background-color: #4a4aff; color: white; display: flex; 
                        align-items: center; justify-content: center; 
                        margin: 0 auto; font-size: 1.5em; font-weight: bold;'>
                            {first_letter}
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"### {name}")
                    st.markdown(f"**{candidate.get('seniority', '').title()}** • {candidate.get('experience_years', 'N/A')} experience")
                    
                    # Location and Employment Type
                    loc = ', '.join(candidate.get('location', ['Not specified']))
                    emp_type = candidate.get('employment_type', 'Not specified').replace('-', ' ').title()
                    st.markdown(f"📍 {loc} • 💼 {emp_type}")
                    
                    # Skills
                    skills = candidate.get('skills', [])
                    if skills:
                        st.markdown("**Skills:** " + " • ".join([f"`{s}`" for s in skills[:5]]))
                
                # Match Reason - Always visible
                st.markdown("---")
                st.markdown("**Match Reason:**")
                st.info(candidate.get('_match_reason', 'No reason provided'))
                
                st.markdown("---")
        
        # Show detailed view if a candidate is selected
        if 'selected_candidate' in st.session_state and st.session_state.selected_candidate:
            st.markdown("---")
            st.markdown("## 👤 Full Candidate Profile")
            
            candidate = st.session_state.selected_candidate
            
            # Main profile header
            col1, col2 = st.columns([1, 3])
            with col1:
                # Placeholder for profile picture or avatar
                st.markdown("""
                    <div style='width: 150px; height: 150px; border-radius: 50%; 
                    background-color: #f0f2f6; display: flex; align-items: center; 
                    justify-content: center; margin: 0 auto; font-size: 3em;'>
                        👤
                    </div>
                """, unsafe_allow_html=True)
                
                # Basic info
                st.markdown(f"### {candidate.get('name', 'Unnamed Candidate')}")
                st.markdown(f"**{candidate.get('title', '')}**")
                
                # Contact info (if available)
                if 'email' in candidate:
                    st.markdown(f"✉️ {candidate['email']}")
                if 'phone' in candidate:
                    st.markdown(f"📱 {candidate['phone']}")
                
                # Social links (if available)
                if 'linkedin' in candidate or 'github' in candidate:
                    st.markdown("### Connect")
                    if 'linkedin' in candidate:
                        st.markdown(f"🔗 [LinkedIn]({candidate['linkedin']})")
                    if 'github' in candidate:
                        st.markdown(f"💻 [GitHub]({candidate['github']})")
                
                # Action buttons
                if st.button("← Back to Results", use_container_width=True):
                    st.session_state.selected_candidate = None
                    st.rerun()
                
                if st.button("📥 Download Full CV", use_container_width=True):
                    st.info("CV download functionality coming soon!")
            
            with col2:
                # Professional Summary
                if 'summary' in candidate:
                    st.markdown("### Professional Summary")
                    st.markdown(candidate['summary'])
                
                # Work Experience
                if 'experience' in candidate and candidate['experience']:
                    st.markdown("### 🏢 Work Experience")
                    for exp in candidate['experience']:
                        with st.expander(f"{exp.get('position', 'Role')} at {exp.get('company', 'Company')} ({exp.get('duration', 'N/A')})"):
                            if 'description' in exp:
                                st.markdown(exp['description'])
                            if 'achievements' in exp and exp['achievements']:
                                st.markdown("**Key Achievements:**")
                                for ach in exp['achievements']:
                                    st.markdown(f"- {ach}")
                
                # Education
                if 'education' in candidate and candidate['education']:
                    st.markdown("### 🎓 Education")
                    for edu in candidate['education']:
                        st.markdown(f"**{edu.get('degree', 'Degree')}**")
                        st.markdown(f"{edu.get('institution', 'Institution')} | {edu.get('year', 'Year')}")
                        if 'details' in edu:
                            st.markdown(edu['details'])
                
                # Skills
                if 'skills' in candidate and candidate['skills']:
                    st.markdown("### 🛠️ Skills & Expertise")
                    skills = candidate['skills']
                    
                    # Group skills by category if available
                    if any(isinstance(skill, dict) for skill in skills):
                        skill_categories = {}
                        for skill in skills:
                            if isinstance(skill, dict):
                                category = skill.get('category', 'Other')
                                if category not in skill_categories:
                                    skill_categories[category] = []
                                skill_categories[category].append(skill.get('name', ''))
                        
                        for category, skill_list in skill_categories.items():
                            st.markdown(f"**{category}**")
                            st.markdown(" • ".join([f"`{s}`" for s in skill_list if s]))
                    else:
                        # Simple list of skills
                        st.markdown(" • ".join([f"`{s}`" for s in skills if s]))
                
                # Additional sections (certifications, projects, etc.)
                if 'certifications' in candidate and candidate['certifications']:
                    st.markdown("### 📜 Certifications")
                    for cert in candidate['certifications']:
                        st.markdown(f"- {cert}")
                
                if 'projects' in candidate and candidate['projects']:
                    st.markdown("### 🚀 Projects")
                    for proj in candidate['projects']:
                        with st.expander(proj.get('name', 'Project')):
                            st.markdown(f"**Technologies:** {', '.join(proj.get('technologies', []))}")
                            if 'description' in proj:
                                st.markdown(proj['description'])
                
                # Raw JSON view (for debugging)
                with st.expander("View Raw Profile Data"):
                    st.json(candidate)
                
                # Action buttons at bottom
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("✉️ Contact Candidate", use_container_width=True):
                        st.info("Contact form will appear here")
                with c2:
                    if st.button("⭐ Shortlist", use_container_width=True):
                        st.success(f"{candidate.get('name', 'Candidate')} has been shortlisted!")
                with c3:
                    if st.button("📅 Schedule Interview", use_container_width=True):
                        st.info("Interview scheduling coming soon!")

def main_app():
    setup_page()
    load_env()
    
    # Load custom CSS
    local_css("static/style.css")
    
    # Initialize session state for app mode if it doesn't exist
    if 'app_mode' not in st.session_state:
        st.session_state.app_mode = "Home"
    
    # --- Sidebar ---
    st.sidebar.title("NaukriAI Controls")
    st.sidebar.header("Navigation")
    
    # Update app mode based on user selection
    new_app_mode = st.sidebar.selectbox(
        "Choose a feature:",
        ["Home", "CV Analyser", "Market Insights", "AI Candidate Search", "AI Matching & Ranking", "Background Check"],
        index=["Home", "CV Analyser", "Market Insights", "AI Candidate Search", "AI Matching & Ranking", "Background Check"].index(st.session_state.app_mode)
    )
    
    if new_app_mode != st.session_state.app_mode:
        st.session_state.app_mode = new_app_mode
        st.rerun()
    
    # Route to the selected page
    if st.session_state.app_mode == "Home":
        show_home()
    elif st.session_state.app_mode == "CV Analyser":
        show_cv_analyser()
    elif st.session_state.app_mode == "AI Candidate Search":
        display_ai_candidate_search()
    elif st.session_state.app_mode == "AI Matching & Ranking":
        show_ai_matching_ranking()
    elif st.session_state.app_mode == "Background Check":
        show_background_check()
    else:
        show_home()

def show_home():
    df = load_data()
    st.title("Welcome to NaukriAI Dashboard 🚀")
    st.markdown("### Your AI-Powered Hiring Co-Pilot")
    
    st.markdown("---")
    st.subheader("Key Metrics")
    
    # Calculate metrics
    total_candidates = len(df)
    seniority_dist = get_seniority_distribution(df)
    top_skills = get_top_skills(df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="custom-card">
                <h3>Total Candidates</h3>
                <p style="font-size: 2em; color: #4a4aff; font-weight: bold;">{total_candidates:,}</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        # Get senior count safely
        senior_count = seniority_dist[seniority_dist['seniority'] == 'senior']['count'].iloc[0] if not seniority_dist[seniority_dist['seniority'] == 'senior'].empty else 0
        st.markdown(
            f"""
            <div class="custom-card">
                <h3>Senior Candidates</h3>
                <p style="font-size: 2em; color: #4a4aff; font-weight: bold;">{senior_count}</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col3:
        top_skill = top_skills.iloc[0]['Skill'] if not top_skills.empty else "N/A"
        top_skill_count = top_skills.iloc[0]['Count'] if not top_skills.empty else 0
        st.markdown(
            f"""
            <div class="custom-card">
                <h3>Top Skill</h3>
                <p style="font-size: 1.5em; color: #4a4aff; font-weight: bold; margin: 0;">{top_skill}</p>
                <p style="font-size: 1em; color: #b0b0ff; margin: 0;">{top_skill_count} candidates</p>
            </div>
            """, unsafe_allow_html=True
        )
    
    # Add some space
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # First row of charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Top 10 Skills in Demand")
        fig = px.bar(
            top_skills.head(10), 
            x='Count', 
            y='Skill',
            orientation='h',
            color='Count',
            color_continuous_scale='blues',
            labels={'Count': 'Number of Candidates', 'Skill': 'Skill'}
        )
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Seniority Distribution")
        fig = px.pie(
            seniority_dist, 
            values='count', 
            names='seniority',
            hole=0.4,
            color='seniority',
            color_discrete_map={
                'junior': '#4a4aff',
                'midlevel': '#6c6cff',
                'senior': '#8e8eff'
            }
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    
    # Second row of charts
    st.subheader("Experience Level Distribution")
    exp_dist = get_experience_distribution(df)
    if not exp_dist.empty:
        # Sort the experience levels for consistent ordering
        exp_dist = exp_dist.sort_values('experience')
        
        fig = px.bar(
            exp_dist, 
            x='experience', 
            y='count',
            color='experience',
            color_discrete_sequence=px.colors.sequential.Blues_r,
            labels={'experience': 'Experience Level', 'count': 'Number of Candidates'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis={'categoryorder': 'array', 'categoryarray': sorted(exp_dist['experience'].unique())}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Third row - skills by seniority
    st.subheader("Top Skills by Seniority Level")
    seniority_levels = df['seniority'].unique()
    cols = st.columns(len(seniority_levels))
    
    for idx, level in enumerate(seniority_levels):
        with cols[idx]:
            st.markdown(f"**{level.capitalize()}**")
            skills_df = get_skills_by_seniority(df, level)
            if not skills_df.empty:
                fig = px.bar(
                    skills_df, 
                    x='Count', 
                    y='Skill',
                    orientation='h',
                    color='Count',
                    color_continuous_scale='blues',
                    height=300
                )
                fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
                st.plotly_chart(fig, use_container_width=True)

def show_cv_analyser():
    st.header("CV Analyser")
    st.markdown("Upload your CV (PDF or DOCX) to get detailed analysis.")
    
    uploaded_file = st.file_uploader("Choose a CV file", type=["pdf", "docx", "txt"])
    
    if uploaded_file is not None:
        # Display file details
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": f"{uploaded_file.size / 1024:.2f} KB"}
        st.write("File uploaded successfully!")
        st.write(file_details)
        
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            # Initialize the CV Analyzer
            analyzer = CVAnalyzer()
            
            # Show a loading spinner while analyzing
            with st.spinner('Analyzing your CV...'):
                # Analyze the CV
                result = analyzer.analyze_cv(tmp_file_path)
            
            if result['status'] == 'success':
                analysis = result['analysis']
                
                # Display the analysis results with enhanced recruiter-focused sections
                st.subheader("📊 CV Analysis Report")
                
                # Overall Assessment
                if 'overall_score' in analysis:
                    score = analysis['overall_score']
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.metric(label="Overall Fit Score", value=f"{score}%")
                    with col2:
                        if score >= 80:
                            st.success("🔥 Strong match for technical roles")
                        elif score >= 60:
                            st.warning("🔄 Potential match with some upskilling")
                        else:
                            st.info("📉 May require significant experience or skill development")
                
                st.markdown("---")
                
                # Candidate Snapshot
                st.subheader("👤 Candidate Snapshot")
                if 'candidate_summary' in analysis:
                    summary = analysis['candidate_summary']
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown("##### 🔍 Basic Info")
                        st.markdown(f"**Name:** {summary.get('name', 'N/A')}")
                        st.markdown(f"**Current Position:** {summary.get('current_position', 'N/A')}")
                        st.markdown(f"**Experience:** {summary.get('total_experience', 'N/A')}")
                    with col2:
                        st.markdown("##### 📍 Location & Availability")
                        st.markdown(f"**Location:** {summary.get('location', 'N/A')}")
                        st.markdown(f"**Notice Period:** {summary.get('notice_period', 'Not specified')}")
                        st.markdown(f"**Employment Type:** {summary.get('employment_type', 'Not specified')}")
                    with col3:
                        st.markdown("##### 🎓 Education")
                        if 'education' in summary and summary['education']:
                            for edu in summary['education'][:2]:  # Show top 2 education entries
                                st.markdown(f"- {edu}")
                        else:
                            st.markdown("No education information provided")
                
                # Core Competencies
                st.markdown("---")
                st.subheader("💼 Core Competencies")
                
                if 'skills' in analysis and analysis['skills']:
                    skills = analysis['skills']
                    
                    # Categorize skills
                    tech_skills = [s for s in skills if any(tech in s.lower() for tech in ['python', 'java', 'c++', 'javascript', 'sql', 'cloud', 'aws', 'azure', 'docker', 'kubernetes', 'ml', 'ai', 'data'])]
                    soft_skills = [s for s in skills if s.lower() in ['leadership', 'communication', 'teamwork', 'problem solving', 'time management', 'adaptability']]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("##### 🛠️ Technical Skills")
                        for skill in tech_skills[:8]:  # Show top 8 technical skills
                            st.markdown(f"- {skill}")
                    with col2:
                        st.markdown("##### 🤝 Soft Skills")
                        for skill in soft_skills or ["Not explicitly mentioned"]:
                            st.markdown(f"- {skill}")
                
                # Work Experience Analysis
                st.markdown("---")
                st.subheader("📈 Work Experience Analysis")
                
                # Try to extract experience from different possible fields
                experience_data = []
                
                # Check standard experience field first
                if 'experience' in analysis:
                    experience_data = analysis['experience']
                # Check if experience is in candidate_summary
                elif 'candidate_summary' in analysis and 'experience' in analysis['candidate_summary']:
                    experience_data = analysis['candidate_summary']['experience']
                # Check if experience is embedded in the text
                elif 'text' in analysis:
                    # Try to extract experience from raw text (simplified example)
                    import re
                    text = analysis.get('text', '')
                    # Look for common work experience patterns
                    experience_matches = re.finditer(r'([A-Za-z]+\s+\d{4})\s*-\s*([A-Za-z]+\s+\d{4}|Present).*?\n(.*?)(?=\n\w|$)', 
                                                text, re.DOTALL)
                    for match in experience_matches:
                        start_date, end_date, details = match.groups()
                        experience_data.append({
                            'duration': f"{start_date} - {end_date}",
                            'details': details.strip()
                        })
                
                if experience_data:
                    for idx, job in enumerate(experience_data[:3]):  # Show top 3 experiences
                        with st.expander(f"{job.get('title', 'Role')} at {job.get('company', 'Company')} ({job.get('duration', 'N/A')})"):
                            # Display role and company if available
                            if 'title' in job or 'company' in job:
                                st.markdown(f"**Role:** {job.get('title', 'Not specified')}")
                                st.markdown(f"**Company:** {job.get('company', 'Not specified')}")
                            
                            # Display duration if available
                            if 'duration' in job:
                                st.markdown(f"**Duration:** {job['duration']}")
                            
                            # Display responsibilities
                            st.markdown("**Key Responsibilities:**")
                            if 'responsibilities' in job and job['responsibilities']:
                                for resp in job['responsibilities'][:5]:  # Show top 5 responsibilities
                                    st.markdown(f"- {resp}")
                            elif 'details' in job:
                                # Try to extract bullet points from details
                                details = job['details'].split('\n')
                                for detail in details[:5]:  # Show top 5 details
                                    if detail.strip():
                                        st.markdown(f"- {detail.strip()}")
                            else:
                                st.markdown("- No specific responsibilities mentioned")
                            
                            # Display achievements if available
                            if 'achievements' in job and job['achievements']:
                                st.markdown("**Key Achievements:**")
                                for ach in job['achievements'][:3]:  # Show top 3 achievements
                                    st.markdown(f"- ✅ {ach}")
                else:
                    st.warning("No detailed work experience found in the CV. Here's what we found in the text:")
                    # Show raw text analysis as fallback
                    if 'text' in analysis:
                        text = analysis['text']
                        # Look for any company names or roles that might indicate experience
                        import re
                        # Look for common work-related terms
                        work_terms = ['worked at', 'experience at', 'intern at', 'role at', 'position at', 'bladexlab']
                        found_terms = [term for term in work_terms if term.lower() in text.lower()]
                        if found_terms:
                            st.info(f"Found potential work experience mentions: {', '.join(found_terms)}")
                            # Show context around these terms
                            for term in found_terms:
                                idx = text.lower().find(term.lower())
                                if idx > 0:
                                    context = text[max(0, idx-50):min(len(text), idx+100)]
                                    st.text(f"...{context}...")
                                    st.markdown("---")
                
                # Strengths & Development Areas
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🌟 Key Strengths")
                    if 'strengths' in analysis and analysis['strengths']:
                        for strength in analysis['strengths'][:5]:  # Show top 5 strengths
                            st.markdown(f"- ✅ {strength}")
                    else:
                        st.markdown("No specific strengths identified")
                
                with col2:
                    st.subheader("📈 Development Areas")
                    if 'development_areas' in analysis and analysis['development_areas']:
                        for area in analysis['development_areas'][:5]:  # Show top 5 development areas
                            st.markdown(f"- 📌 {area}")
                    else:
                        st.markdown("No specific development areas identified")
                
                # Recruiter's Notes
                st.markdown("---")
                st.subheader("📝 Recruiter's Notes")
                
                if 'recommendation' in analysis:
                    rec = analysis['recommendation']
                    
                    st.markdown("#### 🎯 Recommended Roles")
                    if 'suggested_roles' in rec and rec['suggested_roles']:
                        roles = ", ".join(rec['suggested_roles'])
                        st.markdown(f"{roles}")
                    else:
                        st.markdown("No specific role recommendations available")
                    
                    st.markdown("#### 💰 Salary Benchmark")
                    if 'suggested_compensation_range' in rec and rec['suggested_compensation_range']:
                        comp = rec['suggested_compensation_range']
                        st.markdown(f"**Range:** {comp.get('currency', 'USD')} {comp.get('min', 'N/A')} - {comp.get('max', 'N/A')} per year")
                    else:
                        st.markdown("No salary benchmark available")
                    
                    st.markdown("#### 📋 Interview Focus Areas")
                    if 'interview_focus' in analysis and analysis['interview_focus']:
                        for focus in analysis['interview_focus'][:3]:  # Show top 3 focus areas
                            st.markdown(f"- 🔍 {focus}")
                    else:
                        st.markdown("No specific interview focus areas identified")
                    
                    st.markdown("#### 📝 Additional Notes")
                    if 'notes' in analysis and analysis['notes']:
                        st.markdown(analysis['notes'])
                    else:
                        st.markdown("No additional notes available")
                
                # Raw JSON (for debugging)
                with st.expander("View Raw Analysis"):
                    st.json(analysis)
            
            else:
                st.error(f"Error analyzing CV: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            st.error(f"An error occurred while analyzing the CV: {str(e)}")
        finally:
            # Clean up the temporary file
            try:
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
            except Exception as e:
                st.warning(f"Warning: Could not delete temporary file: {str(e)}")

if __name__ == "__main__":
    main_app()

def show_ai_matching_ranking():
    """Display the AI Matching & Ranking interface"""
    st.title("🤖 AI-Powered Candidate Matching & Ranking")
    st.markdown("""
    Use AI to find and rank the best candidates based on job requirements.
    The system analyzes skills, experience, seniority, and cultural fit.
    """)
    
    # Initialize session state for form data
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    if 'required_skills' not in st.session_state:
        st.session_state.required_skills = []
    if 'seniority' not in st.session_state:
        st.session_state.seniority = ""
    if 'experience_years' not in st.session_state:
        st.session_state.experience_years = ""
    if 'employment_type' not in st.session_state:
        st.session_state.employment_type = ""
    if 'locations' not in st.session_state:
        st.session_state.locations = []
    
    with st.form("job_requirements"):
        st.subheader("Job Requirements")
        
        # Job description
        job_desc = st.text_area(
            "Job Description",
            value=st.session_state.job_description,
            help="Enter a detailed job description"
        )
        
        # Skills input
        skills_input = st.text_input(
            "Required Skills (comma separated)",
            value=", ".join(st.session_state.required_skills),
            help="Enter skills separated by commas"
        )
        
        # Other fields
        col1, col2, col3 = st.columns(3)
        with col1:
            seniority = st.selectbox(
                "Seniority Level",
                ["", "Junior", "Mid-Level", "Senior"],
                index=["", "Junior", "Mid-Level", "Senior"].index(st.session_state.seniority) if st.session_state.seniority else 0
            )
        
        with col2:
            experience = st.selectbox(
                "Years of Experience",
                ["", "1-3", "3-5", "5-10", "10+", "15+"],
                index=["", "1-3", "3-5", "5-10", "10+", "15+"].index(st.session_state.experience_years) if st.session_state.experience_years else 0
            )
        
        with col3:
            emp_type = st.selectbox(
                "Employment Type",
                ["", "Full-time", "Part-time", "Contract", "Remote"],
                index=["", "Full-time", "Part-time", "Contract", "Remote"].index(st.session_state.employment_type) if st.session_state.employment_type else 0
            )
        
        # Locations
        locations = st.multiselect(
            "Preferred Locations",
            ["North America", "Europe", "Asia", "South America", "Africa", "Australia", "Remote"],
            default=st.session_state.locations
        )
        
        # Submit button
        submitted = st.form_submit_button("Find & Rank Candidates")
        
        if submitted:
            # Update session state
            st.session_state.job_description = job_desc
            st.session_state.required_skills = [s.strip() for s in skills_input.split(",") if s.strip()]
            st.session_state.seniority = seniority
            st.session_state.experience_years = experience
            st.session_state.employment_type = emp_type
            st.session_state.locations = locations
            
            # Process the form
            process_matching_form(job_desc, st.session_state.required_skills, seniority, 
                                experience, emp_type, locations)


def process_matching_form(job_desc, required_skills, seniority, experience, emp_type, locations):
    """Process the matching form and display results"""
    if not required_skills and not job_desc:
        st.warning("Please enter either job description or required skills")
        return
    
    with st.spinner("Finding and ranking candidates..."):
        try:
            # Initialize matcher and ranker
            matcher = AdvancedCandidateMatcher()
            ranker = CandidateRanker()
            
            # If job description is provided but no skills, extract skills from JD
            if not required_skills and job_desc:
                with st.spinner("Extracting skills from job description..."):
                    required_skills = extract_skills_from_jd(job_desc)
                    st.session_state.required_skills = required_skills
            
            # Match candidates
            matches = matcher.match_candidates(
                required_skills=required_skills,
                seniority=seniority.lower() if seniority else None,
                experience_years=experience if experience else None,
                employment_type=emp_type.lower() if emp_type else None,
                locations=[loc.lower() for loc in locations] if locations else None,
                top_n=10
            )
            
            # Convert matches to dict for ranking
            matches_dict = [asdict(match) for match in matches]
            
            # Rank candidates
            ranked_candidates = ranker.rank_candidates(
                candidates=matches_dict,
                job_description=job_desc,
                company_culture=""  # Could be loaded from company profile
            )
            
            # Display results
            display_ranked_candidates(ranked_candidates, required_skills)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)


def extract_skills_from_jd(job_description: str) -> List[str]:
    """Extract skills from job description using Groq"""
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that extracts skills from job descriptions. Return only a JSON array of skills."
                },
                {
                    "role": "user",
                    "content": f"Extract the key technical and professional skills from this job description. Return only a JSON array of skill names.\n\nJob Description:\n{job_description}"
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get('skills', [])
    except Exception as e:
        st.warning(f"Could not extract skills from job description: {str(e)}")
        return []


def display_ranked_candidates(candidates: List[Dict[str, Any]], required_skills: List[str]):
    """Display ranked candidates with detailed information"""
    if not candidates:
        st.info("No matching candidates found. Try adjusting your criteria.")
        return
    
    st.subheader("🥇 Top Candidates")
    st.markdown(f"Found {len(candidates)} matching candidates")
    
    for i, candidate in enumerate(candidates[:10], 1):  # Show top 10
        with st.expander(f"{i}. {candidate['name']} - Score: {candidate['ranking_scores']['overall']:.2f}"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric("Match Score", f"{candidate['ranking_scores']['overall']:.0%}")
                st.metric("Seniority", candidate.get('seniority', 'N/A').title())
                st.metric("Experience", candidate.get('experience_years', 'N/A'))
                st.metric("Employment Type", candidate.get('employment_type', 'N/A').title())
            
            with col2:
                # Skills section
                st.markdown("#### 🛠 Skills")
                
                # Display matching skills
                matching_skills = set(candidate.get('skills', [])).intersection(required_skills)
                if matching_skills:
                    st.markdown("✅ " + ", ".join(matching_skills))
                
                # Display missing skills
                missing_skills = set(required_skills) - set(candidate.get('skills', []))
                if missing_skills:
                    st.markdown("❌ Missing: " + ", ".join(missing_skills))
                
                # Additional skills
                other_skills = set(candidate.get('skills', [])) - set(required_skills)
                if other_skills:
                    st.markdown("🔹 Additional: " + ", ".join(other_skills))
                
                # Detailed scores
                with st.expander("Detailed Scores"):
                    scores = candidate.get('ranking_scores', {})
                    for key, value in scores.items():
                        if key != 'overall':
                            st.progress(int(value * 100), text=f"{key.replace('_', ' ').title()}: {value:.2f}")
            
            st.markdown("---")


def show_background_check():
    """Display the background check interface"""
    st.title("🔍 AI-Powered Background Check")
    st.markdown("""
    Generate interview questions and verify candidate information using AI.
    This helps streamline the pre-screening process.
    """)
    
    # Initialize session state
    if 'candidate_data' not in st.session_state:
        st.session_state.candidate_data = {
            'name': '',
            'email': '',
            'phone': '',
            'skills': [],
            'experience': [],
            'education': []
        }
    
    # Form for candidate information
    with st.form("candidate_info"):
        st.subheader("Candidate Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value=st.session_state.candidate_data['name'])
            email = st.text_input("Email", value=st.session_state.candidate_data['email'])
            phone = st.text_input("Phone", value=st.session_state.candidate_data['phone'])
        
        with col2:
            skills = st.text_area("Skills (one per line)", 
                               value="\n".join(st.session_state.candidate_data['skills']))
        
        # Experience section
        st.subheader("Work Experience")
        experience = []
        for i, exp in enumerate(st.session_state.candidate_data.get('experience', [{}])):
            with st.expander(f"Experience {i+1}" if exp.get('company') else "Add Experience"):
                col1, col2 = st.columns(2)
                with col1:
                    company = st.text_input("Company", key=f"exp_company_{i}", 
                                          value=exp.get('company', ''))
                    position = st.text_input("Position", key=f"exp_position_{i}", 
                                           value=exp.get('position', ''))
                with col2:
                    start_date = st.date_input("Start Date", key=f"exp_start_{i}",
                                             value=datetime.date(2020, 1, 1) if not exp.get('start_date') 
                                             else datetime.datetime.strptime(exp['start_date'], '%Y-%m-%d').date())
                    end_date = st.date_input("End Date", key=f"exp_end_{i}",
                                           value=datetime.date.today() if not exp.get('end_date') 
                                           else (datetime.datetime.strptime(exp['end_date'], '%Y-%m-%d').date() 
                                                 if exp['end_date'].lower() != 'present' 
                                                 else datetime.date.today()))
                description = st.text_area("Description", key=f"exp_desc_{i}",
                                         value=exp.get('description', ''))
                
                if company and position:
                    experience.append({
                        'company': company,
                        'position': position,
                        'start_date': start_date.strftime('%Y-%m-%d'),
                        'end_date': 'present' if end_date == datetime.date.today() else end_date.strftime('%Y-%m-%d'),
                        'description': description
                    })
        
        # Add new experience button
        if st.button("Add Another Position"):
            st.session_state.candidate_data['experience'].append({})
            st.experimental_rerun()
        
        # Education section
        st.subheader("Education")
        education = []
        for i, edu in enumerate(st.session_state.candidate_data.get('education', [{}])):
            with st.expander(f"Education {i+1}" if edu.get('institution') else "Add Education"):
                col1, col2 = st.columns(2)
                with col1:
                    institution = st.text_input("Institution", key=f"edu_inst_{i}",
                                              value=edu.get('institution', ''))
                    degree = st.text_input("Degree", key=f"edu_degree_{i}",
                                         value=edu.get('degree', ''))
                with col2:
                    field = st.text_input("Field of Study", key=f"edu_field_{i}",
                                        value=edu.get('field', ''))
                    grad_year = st.number_input("Graduation Year", key=f"edu_year_{i}",
                                               min_value=1900, max_value=datetime.date.today().year + 5,
                                               value=edu.get('year', datetime.date.today().year))
                
                if institution and degree:
                    education.append({
                        'institution': institution,
                        'degree': degree,
                        'field': field,
                        'year': grad_year
                    })
        
        # Add new education button
        if st.button("Add Another Degree"):
            st.session_state.candidate_data['education'].append({})
            st.experimental_rerun()
        
        # Job description
        st.subheader("Job Description")
        job_description = st.text_area("Paste the job description here", 
                                     height=200,
                                     value=st.session_state.get('job_description', ''))
        
        # Submit button
        submitted = st.form_submit_button("Generate Report")
        
        if submitted:
            # Update session state
            st.session_state.candidate_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'skills': [s.strip() for s in skills.split('\n') if s.strip()],
                'experience': experience,
                'education': education
            }
            st.session_state.job_description = job_description
            
            # Process the form
            asyncio.run(process_background_check(
                st.session_state.candidate_data,
                job_description
            ))


async def process_background_check(candidate_data: Dict[str, Any], job_description: str):
    """Process background check and generate report"""
    with st.spinner("Generating background check report..."):
        try:
            # Initialize background checker
            checker = BackgroundChecker()
            
            # Generate report
            report = await checker.generate_pre_screening_report(
                candidate_profile=candidate_data,
                job_description=job_description
            )
            
            # Display report
            display_background_report(report)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)


def display_background_report(report: Dict[str, Any]):
    """Display the background check report"""
    if not report or report.get('status') == 'error':
        st.error("Failed to generate report. Please try again.")
        return
    
    st.success("Background check report generated successfully!")
    
    # Candidate info
    st.subheader("👤 Candidate Information")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Name:** {report['candidate_info']['name']}")
        st.markdown(f"**Email:** {report['candidate_info']['email']}")
        st.markdown(f"**Phone:** {report['candidate_info']['phone']}")
    
    # Employment verification
    if 'employment_verification' in report:
        st.subheader("🏢 Employment Verification")
        verification = report['employment_verification']
        
        if verification.get('overall_status') == 'verified':
            st.success("✅ Employment history verified")
        elif verification.get('overall_status') == 'needs_review':
            st.warning("⚠️ Employment history needs review")
        elif verification.get('overall_status') == 'concerns':
            st.error("❌ Concerns found in employment history")
        
        if 'red_flags' in verification and verification['red_flags']:
            st.warning("**Potential Issues:**")
            for flag in verification['red_flags']:
                st.write(f"- {flag}")
    
    # Interview questions
    if 'interview_questions' in report and report['interview_questions']:
        st.subheader("❓ Recommended Interview Questions")
        
        for i, question in enumerate(report['interview_questions'][:5], 1):  # Show top 5
            with st.expander(f"{i}. {question.get('question', '')}"):
                st.markdown(f"**Type:** {question.get('type', 'N/A')}")
                st.markdown(f"**Evaluates:** {question.get('evaluates', 'N/A')}")
                if 'skills' in question and question['skills']:
                    st.markdown("**Skills Assessed:** " + ", ".join(question['skills']))
    
    # Assessment
    if 'assessment' in report:
        st.subheader("📝 Assessment")
        assessment = report['assessment']
        
        if 'summary' in assessment:
            st.markdown("### Summary")
            st.write(assessment['summary'])
        
        if 'strengths' in assessment and assessment['strengths']:
            st.markdown("### ✅ Key Strengths")
            if isinstance(assessment['strengths'], list):
                for strength in assessment['strengths']:
                    st.write(f"- {strength}")
            else:
                st.write(assessment['strengths'])
        
        if 'concerns' in assessment and assessment['concerns']:
            st.markdown("### ⚠️ Potential Concerns")
            if isinstance(assessment['concerns'], list):
                for concern in assessment['concerns']:
                    st.write(f"- {concern}")
            else:
                st.write(assessment['concerns'])
        
        if 'recommendations' in assessment and assessment['recommendations']:
            st.markdown("### 📋 Recommendations")
            if isinstance(assessment['recommendations'], list):
                for rec in assessment['recommendations']:
                    st.write(f"- {rec}")
            else:
                st.write(assessment['recommendations'])
    
    # Generated timestamp
    if 'generated_at' in report:
        st.caption(f"Report generated on {report['generated_at']}")


if __name__ == "__main__":
    import sys
    # Create an event loop for async operations
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        sys.exit(main_app())
    finally:
        loop.close()
