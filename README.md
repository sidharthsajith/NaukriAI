# NaukriAI - AI-Powered Talent Search Platform

## Overview
NaukriAI is an AI-powered talent search and management platform designed to revolutionize the recruitment process. The platform leverages advanced AI technologies to provide intelligent candidate search, automated resume parsing, and comprehensive talent pool analytics.

## Planned Features

### 1. PeopleGPT - Natural-Language Multi-Source Talent Search Engine
- Implemented ✅
- Description: A conversational search engine that allows recruiters to find candidates using natural language queries. The system uses Groq's LLM to understand complex search criteria and return relevant candidates from multiple data sources.
- Current Status: Basic implementation completed with Groq integration for natural language search

### 2. Automated Resume Parsing and Skill Extraction
- Planned 📋
- Description: AI-powered system to automatically parse resumes and extract relevant skills, experience, and qualifications.
- Future Work: Implementation of resume parsing pipeline and skill extraction using NLP techniques

### 3. Candidate Ranking and Scoring System
- Planned 📋
- Description: Intelligent scoring system that ranks candidates based on recruiter-defined criteria, including skill match, experience, and cultural fit.
- Future Work: Development of scoring algorithms and criteria weighting system

### 4. AI-Powered Background Checking and Pre-Screening
- Planned 📋
- Description: Automated background verification and pre-screening process with AI-generated interview questions based on candidate profiles.
- Future Work: Implementation of background checking system and Q&A generation engine

### 5. Talent-Pool Insights Dashboards
- Planned 📋
- Description: Comprehensive analytics dashboard for monitoring talent pool metrics using PostHog or similar analytics platform.
- Future Work: Integration with analytics platform and development of visualization dashboards

### 6. Personalized Outreach System
- Planned 📋
- Description: AI-powered system for generating personalized outreach messages to candidates based on their profiles and preferences.
- Future Work: Implementation of outreach message generation and delivery system

## Current Implementation
The current implementation focuses on the first feature - the PeopleGPT search engine. The system uses Groq's LLM to:
1. Understand natural language search queries
2. Analyze candidate profiles based on predefined schema
3. Return relevant candidates with matching criteria
4. Format results in a readable, structured format

## Getting Started

### Prerequisites
- Python 3.8+
- Groq API Key
- Required packages (see requirements.txt)

### Installation
```bash
pip install -r requirements.txt
export GROQ_API_KEY=your_api_key_here
```

### Usage
```bash
python groq_search.py
```

The system will prompt you to enter search queries. You can use natural language queries like:
- "Find senior developers with experience in Python"
- "Candidates with 5+ years experience in AI/ML"
- "Junior developers with skills in React or Angular"

## Future Development Roadmap
1. Resume parsing and skill extraction
2. Candidate scoring and ranking system
3. Background checking integration
4. Analytics dashboard development
5. Personalized outreach system

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[To be determined]
