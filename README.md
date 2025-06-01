# NaukriAI - AI-Powered Talent Search Platform

## Overview
NaukriAI is an AI-powered talent search and management platform designed to revolutionize the recruitment process. The platform leverages advanced AI technologies to provide intelligent candidate search, automated resume parsing, and comprehensive talent pool analytics.

## Planned Features

### 1. CV Analyzer - AI-Powered Resume Analysis
- Implemented ✅
- Description: An intelligent CV analysis tool that parses and analyzes resumes in PDF or DOCX format. It provides a comprehensive assessment of candidates using Groq's LLM, including skills extraction, experience evaluation, and hiring recommendations.
- Features:
  - Supports both PDF and DOCX formats
  - Extracts and structures key candidate information
  - Identifies technical and soft skills
  - Evaluates work experience and qualifications
  - Detects potential red flags and inconsistencies
  - Provides detailed hiring recommendations with reasoning
  - Outputs analysis in structured JSON format
- Current Status: Ready for use with Groq API integration

### 2. PeopleGPT - Natural-Language Multi-Source Talent Search Engine
- Implemented ✅
- Description: A conversational search engine that allows recruiters to find candidates using natural language queries. The system uses Groq's LLM to understand complex search criteria and return relevant candidates from multiple data sources.
- Current Status: Basic implementation completed with Groq integration for natural language search

### 3. Advanced Candidate Matching System
- Implemented ✅
- Description: AI-powered system that goes beyond basic parsing to deeply understand candidate qualifications and match them with job requirements using semantic search and skill gap analysis.
- Features:
  - Semantic understanding of job descriptions
  - Skill gap analysis between candidates and job requirements
  - Compatibility scoring based on multiple factors
  - Detailed scoring breakdown for each candidate
  - AI-generated interview questions based on profile gaps
  - Support for required and preferred skills weighting

### 4. Candidate Ranking and Scoring System
- Implemented ✅
- Description: Intelligent scoring system that ranks candidates based on recruiter-defined criteria, including skill match, experience, and other relevant factors.
- Features:
  - Customizable scoring weights for different criteria
  - Detailed scoring breakdown for each candidate
  - Support for filtering by seniority, location, and employment type
  - Configurable number of top candidates to return

### 5. AI-Powered Pre-Screening
- Partially Implemented ✅
- Description: Automated pre-screening with AI-generated interview questions based on candidate profiles and identified skill gaps.
- Current Features:
  - AI-generated interview questions based on profile gaps
  - Structured question generation focusing on missing skills
- Future Work:
  - Integration with background verification services
  - Automated response analysis

### 6. Talent-Pool Insights Dashboard
- Implemented ✅
- Description: Interactive analytics dashboard providing comprehensive insights into the talent pool with real-time visualizations.
- Features:
  - Key metrics overview (total candidates, senior candidates, top skills)
  - Skill distribution and demand analysis
  - Seniority level distribution
  - Experience level analysis
  - Skills breakdown by seniority level
  - Interactive charts with filtering capabilities

### 7. Personalized Outreach System
- Implemented ✅
- Description: AI-powered system for generating personalized outreach messages to candidates based on their profiles and job requirements.
- Features:
  - CV upload and analysis
  - Customizable message templates
  - Dynamic content generation based on candidate skills
  - Multiple tone options (Professional, Friendly, etc.)
  - Download and copy message functionality
  - Regeneration of messages with different tones
- Future Work:
  - Integration with email services for direct sending
  - Response tracking and analytics
  - Template library for different outreach scenarios

## Current Implementation

### CV Analyzer
The CV Analyzer provides comprehensive resume analysis with the following capabilities:
- **Document Parsing**: Extracts text and structure from PDF and DOCX files
- **Structured Analysis**: Breaks down the CV into key components (skills, experience, education, etc.)
- **AI-Powered Assessment**: Uses Groq's LLM to provide detailed feedback and recommendations
- **JSON Output**: Returns analysis in a structured, machine-readable format

### PeopleGPT Search Engine
The PeopleGPT search engine allows natural language search across candidate profiles:
- Understands natural language search queries
- Analyzes candidate profiles based on predefined schema
- Returns relevant candidates with matching criteria
- Formats results in a readable, structured format

### Advanced Candidate Matching
Our advanced matching system provides intelligent candidate-job matching:
- **Smart Scoring**: Rates candidates based on skill matches and gaps
- **Customizable Weights**: Adjust importance of required vs preferred skills
- **Detailed Analysis**: Provides breakdown of matching skills and missing qualifications
- **AI-Generated Questions**: Creates targeted interview questions based on profile gaps
- **Flexible Filtering**: Filter by seniority, location, employment type, and experience

### Candidate Ranking System
The ranking system evaluates candidates based on multiple dimensions:
- **Skill Match Score**: How well the candidate's skills match the job requirements
- **Experience Level**: Years of relevant experience
- **Education**: Relevant degrees and certifications
- **Employment History**: Career progression and role relevance
- **Custom Weights**: Recruiters can adjust the importance of each factor

## Getting Started

### Prerequisites
- Python 3.8+
- Groq API Key (Get one from [Groq Cloud](https://console.groq.com/))
- Required packages:
  ```bash
  pip install groq python-dotenv PyPDF2 python-docx streamlit pandas plotly
  ```

### Installation
```bash
pip install -r requirements.txt
export GROQ_API_KEY=your_api_key_here
```

### Usage

#### CV Analyzer
```bash
# Basic usage
python cv_analyser.py path/to/resume.pdf

# Save output to a file
python cv_analyser.py path/to/resume.pdf --output analysis.json

# Specify Groq API key (optional if set in environment)
python cv_analyser.py path/to/resume.pdf --api-key your_api_key_here
```

#### Advanced Features
To launch the complete application with all features:
```bash
streamlit run streamlit_app.py
```

##### PeopleGPT Search Engine
```bash
python groq_search.py
```

Natural language search examples:
- "Find senior developers with experience in Python"
- "Candidates with 5+ years experience in AI/ML"
- "Junior developers with skills in React or Angular"

##### Advanced Candidate Matching
Use the Streamlit interface to:
1. Upload job requirements or enter them manually
2. Set skill weights (required vs preferred)
3. Filter candidates by seniority, location, and employment type
4. View detailed matching reports and AI-generated interview questions

For programmatic use:
```python
from advanced_matching import AdvancedCandidateMatcher

matcher = AdvancedCandidateMatcher('dataset.json')
matches = matcher.match_candidates(
    required_skills=['Python', 'Machine Learning'],
    preferred_skills=['TensorFlow', 'PyTorch'],
    seniority='Senior',
    top_n=5
)
```

## Future Development Roadmap
1. Enhance CV Analyzer with more detailed skills assessment
2. Candidate scoring and ranking system
3. Background checking integration
4. Analytics dashboard development
5. Personalized outreach system
6. Integration between CV Analyzer and PeopleGPT search engine

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[To be determined]
