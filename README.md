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
- Planned 📋
- Description: AI-powered system that goes beyond basic parsing to deeply understand candidate qualifications and match them with job requirements using semantic search and skill gap analysis.
- Future Work:
  - Semantic understanding of job descriptions
  - Skill gap analysis between candidates and job requirements
  - Compatibility scoring based on company culture and team fit
  - Integration with existing ATS systems

### 4. Candidate Ranking and Scoring System
- Planned 📋
- Description: Intelligent scoring system that ranks candidates based on recruiter-defined criteria, including skill match, experience, and cultural fit.
- Future Work: Development of scoring algorithms and criteria weighting system

### 5. AI-Powered Background Checking and Pre-Screening
- Planned 📋
- Description: Automated background verification and pre-screening process with AI-generated interview questions based on candidate profiles.
- Future Work: Implementation of background checking system and Q&A generation engine

### 6. Talent-Pool Insights Dashboards
- Planned 📋
- Description: Comprehensive analytics dashboard for monitoring talent pool metrics using PostHog or similar analytics platform.
- Future Work: Integration with analytics platform and development of visualization dashboards

### 7. Personalized Outreach System
- Planned 📋
- Description: AI-powered system for generating personalized outreach messages to candidates based on their profiles and preferences.
- Future Work: Implementation of outreach message generation and delivery system

## Current Implementation

### CV Analyzer
The CV Analyzer provides comprehensive resume analysis with the following capabilities:
- **Document Parsing**: Extracts text and structure from PDF and DOCX files
- **Structured Analysis**: Breaks down the CV into key components (skills, experience, education, etc.)
- **AI-Powered Assessment**: Uses Groq's LLM to provide detailed feedback and recommendations
- **JSON Output**: Returns analysis in a structured, machine-readable format

### PeopleGPT Search Engine
The PeopleGPT search engine allows natural language search across candidate profiles:
1. Understands natural language search queries
2. Analyzes candidate profiles based on predefined schema
3. Returns relevant candidates with matching criteria
4. Formats results in a readable, structured format

## Getting Started

### Prerequisites
- Python 3.8+
- Groq API Key (Get one from [Groq Cloud](https://console.groq.com/))
- Required packages:
  ```bash
  pip install groq python-dotenv PyPDF2 python-docx
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

#### PeopleGPT Search Engine
```bash
python groq_search.py
```

The system will prompt you to enter search queries. You can use natural language queries like:
- "Find senior developers with experience in Python"
- "Candidates with 5+ years experience in AI/ML"
- "Junior developers with skills in React or Angular"

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
