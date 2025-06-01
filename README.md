# NaukriAI: End-to-End AI Hiring Copilot

**Submission for: HireAI by 100xEngineers Hackathon**  
**Category:** LLMs / AI for Recruitment

---

## 🚀 Executive Summary

NaukriAI is an end-to-end AI-powered hiring copilot designed to dramatically reduce time, cost, and bias in recruiting specialized AI talent. Leveraging advanced LLMs (Groq), NaukriAI enables recruiters to:
- Instantly search and rank candidates using plain-English queries ("PeopleGPT")
- Parse and analyze resumes with AI for skill extraction and red-flag detection
- Auto-score and match candidates to complex job requirements
- Generate AI-powered pre-screening questions
- Visualize talent pool insights and analytics
- Launch personalized, high-conversion outreach in seconds

**Demo-ready, extensible, and built for real-world impact.**

---

## 🏆 Hackathon Problem Mapping

| Hackathon Requirement                                                                 | NaukriAI Feature                                  | Status      |
|--------------------------------------------------------------------------------------|---------------------------------------------------|-------------|
| Natural-language multi-source talent search engine ("PeopleGPT")                     | PeopleGPT LLM Search Engine                       | ✅ Complete |
| Automated resume parsing and skill extraction                                         | CV Analyzer (AI-driven parsing & extraction)      | ✅ Complete |
| Candidate ranking and scoring system based on recruiter criteria                     | Advanced Matching & Scoring                       | ✅ Complete |
| AI-powered background checking and pre-screening (Q&A generation)                    | Pre-Screening Q&A (AI-generated questions)        | 🟡 Partial  |
| Talent-pool insights dashboards and analytics (e.g., PostHog)                        | Interactive Analytics Dashboard                   | ✅ Complete |
| Personalized outreach to candidates                                                  | AI Outreach Message Generator                     | ✅ Complete |

---

## 🌟 Key Features & Technical Highlights

### 1. PeopleGPT: Natural-Language Talent Search
- Recruiters type queries like:  
  _"Find senior Gen-AI engineers with LangChain + RAG experience in Europe, open to contract work"_
- Groq LLM parses, understands, and executes multi-factor search over the candidate pool
- Supports exclusions, preferences, and ranking

### 2. Automated CV Parsing & Skill Extraction
- Upload PDF/DOCX resumes for instant AI-powered parsing
- Extracts structured info: skills, experience, education, red flags
- Uses LLM for deep semantic analysis and recommendations

### 3. Candidate Ranking & Advanced Matching
- Smart scoring based on skills, seniority, location, experience, and recruiter-defined weights
- Skill gap analysis and compatibility scoring
- AI-generated interview/pre-screening questions for missing skills

### 4. Talent-Pool Insights Dashboard
- Visual analytics: top skills, seniority, experience, demand trends
- Interactive charts and filters for deep talent pool insights

### 5. Personalized Outreach System
- AI generates tailored outreach messages based on candidate CV and job details
- Multiple tones/styles, download/copy options
- Demo-ready UI for recruiter productivity

### 6. Extensibility & Future Work
- Modular codebase for easy integration with external sources (LinkedIn, GitHub, email APIs)
- Planned: Automated background verification, direct outreach via email/LinkedIn, response analytics

---

## 🖥️ Demo & Usage

**1. Launch the App**
```
streamlit run streamlit_app.py
```

**2. Explore the Workflow:**
- **PeopleGPT Search:** Type a plain-English query to instantly find and rank candidates
- **CV Analyzer:** Upload a resume for AI-powered parsing and assessment
- **Advanced Matching:** Match candidates to job requirements with smart scoring
- **Pre-Screening Q&A:** Generate interview questions based on candidate gaps
- **Analytics Dashboard:** Visualize key insights about your talent pool
- **Outreach Generator:** Craft and download personalized outreach messages

**See the full presentation script below for a step-by-step demo scenario!**

---

## 🤖 Tech Stack
- Python, Streamlit (UI)
- Groq LLM API (AI/LLM reasoning)
- Plotly (analytics/visualization)
- Modular backend for candidate data and parsing

---

## 📈 Submission Notes
- All core hackathon requirements are implemented and demo-ready
- Pre-screening Q&A is live; automated background checks are planned for future release
- Outreach is fully personalized and ready for integration with email/LinkedIn APIs
- Codebase is clean, extensible, and thoroughly documented

**NaukriAI is ready to revolutionize AI hiring—today!**

---

# Presentation Script: Winning Demo Walkthrough

## 1. Opening Statement

> "Welcome to NaukriAI—the end-to-end AI hiring copilot built for the future of recruitment! In the next few minutes, you’ll see how we’re transforming the way companies find, screen, and engage top AI talent—at lightning speed, with zero bias, and maximum intelligence."

## 2. PeopleGPT: Natural-Language Talent Search

- _"Let’s start with PeopleGPT. As a recruiter, I just type what I want: '
  **Find senior Gen-AI engineers with LangChain + RAG experience in Europe, open to contract work**.'
- Instantly, NaukriAI parses my query using Groq LLM and returns a ranked, de-duplicated list of the best-fit candidates—no manual filtering, no spreadsheets, just results."

## 3. CV Analyzer: AI-Powered Resume Parsing

- _"Now, let’s upload a candidate’s CV—PDF or DOCX. NaukriAI parses it, extracts all key skills, experience, education, and even flags inconsistencies. The AI provides a structured JSON summary and actionable hiring recommendations—saving hours of manual review."

## 4. Advanced Matching & Smart Scoring

- _"Suppose I want to match candidates to a new job opening. I specify required and preferred skills, seniority, and location. NaukriAI’s advanced matcher scores every candidate, highlights skill gaps, and even generates custom interview questions for missing skills. I can tweak weights and instantly see the top matches."

## 5. Pre-Screening Q&A

- _"For each candidate, the AI generates tailored pre-screening questions—helping me focus interviews on real gaps. This is next-level automation for technical hiring."

## 6. Talent Pool Analytics Dashboard

- _"Curious about the talent pool? The dashboard visualizes top skills, seniority, experience, and more. Interactive charts help me spot trends and make data-driven decisions."

## 7. Personalized Outreach Generator

- _"Ready to reach out? NaukriAI crafts a personalized outreach message based on the candidate’s profile and my job details. I can choose the tone, download, or copy the message—ready to send in seconds."

## 8. Closing Statement

> "With NaukriAI, recruiters get superpowers: instant search, deep AI insights, and automated engagement—all in one platform. We’re ready to partner with enterprises to make hiring faster, smarter, and fairer. Thank you!"

---

**Try NaukriAI now and experience the future of AI-powered recruitment.**
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
