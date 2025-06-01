# streamlit_app.py
import streamlit as st
import pandas as pd
import json
import plotly.express as px
from collections import Counter
from typing import List, Dict, Any, Optional
import numpy as np
import tempfile
import os
from pathlib import Path
import time

# Import local modules
from cv_analyser import CVAnalyzer
from groq_search import AICandidateSearch
from advanced_matching import AdvancedCandidateMatcher, ScoredCandidate

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
    
    
    # Initialize session state for app mode if it doesn't exist
    if 'app_mode' not in st.session_state:
        st.session_state.app_mode = "Home"
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["Home", "CV Analyzer", "AI Candidate Search", "Advanced Matching"],
        index=0,
    )
    
    # Update app mode based on navigation
    st.session_state.app_mode = page
    
    # Route to the selected page
    if st.session_state.app_mode == "Home":
        show_home()
    elif st.session_state.app_mode == "CV Analyzer":
        show_cv_analyser()
    elif st.session_state.app_mode == "AI Candidate Search":
        display_ai_candidate_search()
    elif st.session_state.app_mode == "Advanced Matching":
        show_advanced_matching()
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
                
                # Display overall assessment and recommendation if available
                if 'overall_assessment' in analysis:
                    with st.expander("📝 Overall Assessment"):
                        st.write(analysis['overall_assessment'])
                
                # Display recommendation
                if 'recommendation' in analysis:
                    with st.expander("✅ Recommendation"):
                        rec = analysis['recommendation']
                        st.write(f"**Recommended:** {'✅ Yes' if rec.get('recommended', False) else '❌ No'}")
                        st.write(f"**Reasoning:** {rec.get('reasoning', 'N/A')}")
                        
                        if 'suggested_roles' in rec and rec['suggested_roles']:
                            st.write("**Suggested Roles:**")
                            for role in rec['suggested_roles']:
                                st.write(f"- {role}")
                        
                        if 'suggested_compensation_range' in rec:
                            comp = rec['suggested_compensation_range']
                            st.write(f"**Suggested Compensation:** {comp.get('currency', 'USD')} {comp.get('min', 'N/A')} - {comp.get('max', 'N/A')}")
                
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
                
                # Get skills from candidate_summary if available
                candidate_skills = []
                if 'candidate_summary' in analysis and 'key_skills' in analysis['candidate_summary']:
                    candidate_skills = analysis['candidate_summary']['key_skills']
                
                # Fall back to top-level skills if not in candidate_summary
                if not candidate_skills and 'skills' in analysis and analysis['skills']:
                    candidate_skills = analysis['skills']
                
                if candidate_skills:
                    # Categorize skills
                    tech_skills = [s for s in candidate_skills if any(tech in str(s).lower() for tech in ['python', 'java', 'c++', 'javascript', 'sql', 'cloud', 'aws', 'azure', 'docker', 'kubernetes', 'ml', 'ai', 'data', 'artificial intelligence', 'machine learning', 'deep learning', 'nlp'])]
                    soft_skills = [s for s in candidate_skills if str(s).lower() in ['leadership', 'communication', 'teamwork', 'problem solving', 'time management', 'adaptability', 'analytical thinking', 'creativity']]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("##### 🛠️ Technical Skills")
                        for skill in tech_skills[:10]:  # Show top 10 technical skills
                            st.markdown(f"- {skill}")
                    with col2:
                        st.markdown("##### 🤝 Soft Skills")
                        if soft_skills:
                            for skill in soft_skills:
                                st.markdown(f"- {skill}")
                        else:
                            st.markdown("Not explicitly mentioned")
                
                # Strengths and Development Areas
                st.markdown("---")
                st.subheader("🌟 Key Strengths")
                
                # Get strengths from analysis
                strengths = []
                if 'strengths' in analysis and analysis['strengths']:
                    strengths = analysis['strengths']
                
                if strengths:
                    for strength in strengths:
                        st.markdown(f"✅ {strength}")
                else:
                    st.info("No specific strengths identified in the CV.")
                
                # Development Areas
                st.markdown("---")
                st.subheader("📈 Development Areas")
                
                # Get development areas from red_flags or other fields
                development_areas = []
                if 'red_flags' in analysis and analysis['red_flags']:
                    development_areas = analysis['red_flags']
                
                if development_areas:
                    for area in development_areas:
                        st.markdown(f"🔧 {area}")
                else:
                    st.info("No specific development areas identified.")
                
                # Work Experience Analysis
                st.markdown("---")
                st.subheader("💼 Work Experience Analysis")
                
                # Try to extract experience from different possible fields
                experience_data = []
                
                # Check standard experience field first
                if 'experience' in analysis and analysis['experience']:
                    experience_data = analysis['experience']
                # Check if experience is in candidate_summary
                elif 'candidate_summary' in analysis and 'experience' in analysis['candidate_summary']:
                    exp = analysis['candidate_summary'].get('experience')
                    if isinstance(exp, str):
                        # If experience is a string, convert it to a list of dictionaries
                        experience_data = [{'details': exp}]
                    elif isinstance(exp, list):
                        experience_data = exp
                # Check if experience is in work_experience
                elif 'work_experience' in analysis and analysis['work_experience']:
                    experience_data = analysis['work_experience']
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
                        # Handle different job data formats
                        if isinstance(job, str):
                            with st.expander(f"Experience {idx + 1}"):
                                st.markdown(job)
                        elif isinstance(job, dict):
                            # Create a title for the expander
                            title_parts = []
                            if 'title' in job:
                                title_parts.append(job['title'])
                            if 'company' in job:
                                title_parts.append(f"at {job['company']}")
                            if 'duration' in job:
                                title_parts.append(f"({job['duration']})")
                            
                            expander_title = " ".join(title_parts) if title_parts else f"Experience {idx + 1}"
                            
                            with st.expander(expander_title):
                                # Display role and company if available
                                if 'title' in job or 'company' in job:
                                    st.markdown(f"**Role:** {job.get('title', 'Not specified')}")
                                    st.markdown(f"**Company:** {job.get('company', 'Not specified')}")
                                
                                # Display duration if available
                                if 'duration' in job:
                                    st.markdown(f"**Duration:** {job['duration']}")
                                
                                # Display details or responsibilities
                                if 'details' in job:
                                    st.markdown("**Details:**")
                                    st.markdown(job['details'])
                                elif 'responsibilities' in job and job['responsibilities']:
                                    st.markdown("**Key Responsibilities:**")
                                    if isinstance(job['responsibilities'], list):
                                        for resp in job['responsibilities']:
                                            st.markdown(f"- {resp}")
                                    else:
                                        st.markdown(job['responsibilities'])
                else:
                    st.info("No detailed work experience found in the CV. Here's what we found in the text:")
                    if 'text' in analysis and len(analysis['text']) > 0:
                        # Show first 500 characters of the text as a fallback
                        preview_text = analysis['text'][:500] + '...' if len(analysis['text']) > 500 else analysis['text']
                        st.text(preview_text)
                    else:
                        st.warning("No work experience information could be extracted from the CV.")
                    
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
                
                # Salary Benchmark
                st.markdown("##### 💰 Salary Benchmark")
                if 'recommendation' in analysis and 'suggested_compensation_range' in analysis['recommendation']:
                    comp = analysis['recommendation']['suggested_compensation_range']
                    st.markdown(f"Range: {comp.get('currency', 'USD')} {comp.get('min', 'N/A')} - {comp.get('max', 'N/A')} per year")
                else:
                    st.info("Salary benchmark not available")
                
                # Interview Focus Areas
                st.markdown("##### 📋 Interview Focus Areas")
                if 'red_flags' in analysis and analysis['red_flags']:
                    for flag in analysis['red_flags']:
                        st.markdown(f"- Explore: {flag}")
                else:
                    st.info("No specific focus areas identified. Consider standard technical and behavioral questions.")
                
                # Additional Notes
                st.markdown("##### 📝 Additional Notes")
                if 'additional_notes' in analysis and analysis['additional_notes']:
                    st.write(analysis['additional_notes'])
                else:
                    st.info("No additional notes available")
                
                # Display raw analysis in an expander
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

def show_advanced_matching():
    """Display the advanced candidate matching interface."""
    st.title("🔍 Advanced Candidate Matching")
    st.write("""
    Use this tool to find the best candidates based on job requirements.
    The system will analyze skills, experience, and provide interview questions.
    """)
    
    with st.form("job_requirements"):
        st.subheader("Job Requirements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input("Job Title", "Senior Software Engineer")
            required_skills = st.text_area(
                "Required Skills (comma-separated)", 
                "python, machine learning, data analysis"
            )
            preferred_skills = st.text_area(
                "Preferred Skills (comma-separated)", 
                "docker, kubernetes, aws"
            )
        
        with col2:
            seniority = st.selectbox(
                "Seniority Level",
                ["", "junior", "midlevel", "senior"],
                index=2
            )
            experience_years = st.selectbox(
                "Minimum Experience",
                ["", "0-2", "3-5", "5-10", "10+"],
                index=3
            )
            employment_type = st.selectbox(
                "Employment Type",
                ["", "full-time", "part-time", "contract"],
                index=1
            )
        
        job_description = st.text_area(
            "Job Description",
            "We are looking for an experienced software engineer with strong skills in Python and machine learning..."
        )
        
        submitted = st.form_submit_button("Find Best Matches")
    
    if submitted:
        with st.spinner("Finding the best candidates..."):
            try:
                matcher = AdvancedCandidateMatcher()
                
                # Process skills
                required_skills_list = [s.strip() for s in required_skills.split(',') if s.strip()]
                preferred_skills_list = [s.strip() for s in preferred_skills.split(',') if s.strip()]
                
                # Get matched candidates
                candidates = matcher.match_candidates(
                    required_skills=required_skills_list,
                    preferred_skills=preferred_skills_list,
                    seniority=seniority if seniority else None,
                    employment_type=employment_type if employment_type else None,
                    experience_years=experience_years if experience_years else None,
                    top_n=5
                )
                
                if not candidates:
                    st.warning("No candidates found matching all criteria. Try broadening your search.")
                    return
                
                # Display results
                st.subheader(f"Top {len(candidates)} Matches")
                
                for i, candidate in enumerate(candidates, 1):
                    with st.expander(f"{i}. {candidate.candidate['name']} - Score: {candidate.score:.1f}"):
                        st.markdown(f"**Seniority:** {candidate.candidate.get('seniority', 'N/A')}")
                        st.markdown(f"**Experience:** {candidate.candidate.get('experience_years', 'N/A')}")
                        st.markdown(f"**Employment Type:** {candidate.candidate.get('employment_type', 'N/A')}")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Skills:**")
                            for skill in candidate.candidate.get('skills', []):
                                st.markdown(f"- {skill}")
                        
                        with col2:
                            if candidate.skill_matches:
                                st.markdown("**Matched Skills:**")
                                for skill in candidate.skill_matches:
                                    st.markdown(f"- ✅ {skill}")
                            
                            if hasattr(candidate, 'missing_skills') and candidate.missing_skills:
                                st.markdown("**Missing Skills:**")
                                for skill in candidate.missing_skills:
                                    st.markdown(f"- ❌ {skill}")
                        
                        # Show skill gap analysis
                        if hasattr(candidate, 'skill_gap_analysis') and candidate.skill_gap_analysis:
                            st.markdown("**Skill Gap Analysis:**")
                            for skill, analysis in candidate.skill_gap_analysis.items():
                                with st.expander(f"Analysis for {skill}"):
                                    st.write(analysis)
                        
                        # Show interview questions
                        if hasattr(candidate, 'interview_questions') and candidate.interview_questions:
                            st.markdown("**Suggested Interview Questions:**")
                            for j, question in enumerate(candidate.interview_questions, 1):
                                st.markdown(f"{j}. {question}")
                        
                        # Generate full report
                        if st.button(f"Generate Full Report for {candidate.candidate['name']}"):
                            report = matcher.generate_candidate_report(
                                candidate,
                                job_title=job_title,
                                job_description=job_description
                            )
                            st.download_button(
                                label="Download Report as Markdown",
                                data=report,
                                file_name=f"candidate_report_{candidate.candidate['name'].lower().replace(' ', '_')}.md",
                                mime="text/markdown"
                            )
                            
                            st.markdown("---")
                            st.markdown("## Full Report Preview")
                            st.markdown(report)
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                import traceback
                st.text(traceback.format_exc())

if __name__ == "__main__":
    main_app()
