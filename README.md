# NaukriAI: End-to-End AI Hiring Copilot

**Submission for: HireAI by 100xEngineers Hackathon**  
**Category:** LLMs / AI for Recruitment

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Technical Architecture](#-technical-architecture)
- [Core Components](#-core-components)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [License](#-license)

---

## 🚀 Project Overview

NaukriAI is an end-to-end AI-powered hiring copilot designed to streamline the recruitment process for technical roles. The platform leverages advanced LLMs (Groq) to provide intelligent candidate matching, CV analysis, and talent pool analytics.

### Key Features
- **Natural Language Search**: Find candidates using plain-English queries ("PeopleGPT")
- **AI-Powered CV Analysis**: Extract skills, experience, and red flags from resumes
- **Advanced Candidate Matching**: Score and rank candidates based on job requirements
- **Talent Analytics**: Visualize skill distributions and talent pool metrics
- **Personalized Outreach**: Generate tailored outreach messages for candidates
- **Interview Question Generation**: AI-generated questions based on candidate profiles

## 🏗️ Technical Architecture

NaukriAI is built using a modular Python architecture with the following key components:

- **Frontend**: Streamlit-based web interface
- **Backend**: Python 3.8+
- **AI/ML**: Groq LLM API (Llama 3.3 70B)
- **Data Processing**: Custom document parsing and analysis pipelines
- **Data Storage**: JSON-based storage for candidate data

## 🧩 Core Components

### 1. `streamlit_app.py`
Main application entry point and UI layer. Implements the Streamlit-based web interface with the following pages:
- **Dashboard**: Overview of talent pool metrics
- **CV Analyzer**: Upload and analyze candidate resumes
- **AI Candidate Search**: Natural language search for candidates
- **Advanced Matching**: Configure and run candidate matching
- **Outreach**: Generate personalized outreach messages

### 2. `cv_analyser.py`
Responsible for parsing and analyzing CVs using Groq's LLM:
- Supports PDF and DOCX formats
- Extracts key information (skills, experience, education)
- Identifies red flags and potential issues
- Generates candidate assessment reports

### 3. `groq_search.py`
Implements the natural language search functionality:
- Processes natural language queries
- Maps queries to structured search terms
- Filters and ranks candidates
- Uses Groq LLM for semantic understanding

### 4. `advanced_matching.py`
Handles candidate-to-job matching:
- Implements scoring algorithms
- Calculates skill gaps
- Generates interview questions
- Ranks candidates based on job requirements

### 5. `docs_parser.py`
Utility module for document processing:
- Extracts text from PDF and DOCX files
- Handles different document structures
- Normalizes text for analysis
- Processes tables and formatting

### 6. `dataset.py`
Manages candidate data:
- Generates synthetic candidate data for testing
- Handles data loading and persistence
- Provides data validation and transformation

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

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key (https://console.groq.com/)
- Required packages (see `requirements.txt`)

### Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd NaukriAI
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
echo "GROQ_API_KEY=your_api_key_here" > .env
```

## 🚀 Usage

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. Open your browser to `http://localhost:8501`

### Key Features

#### 1. PeopleGPT Search
- Type natural language queries to find candidates
- Example: "Find senior Python developers with ML experience in Europe"
- Results include match scores and key qualifications

#### 2. CV Analyzer
- Upload PDF or DOCX resumes
- View AI-generated analysis including:
  - Skills and experience extraction
  - Red flag detection
  - Candidate assessment

#### 3. Advanced Matching
- Upload job descriptions or enter requirements manually
- Configure matching criteria and weights
- View ranked candidates with match scores
- Generate interview questions for specific candidates

#### 4. Talent Analytics
- Visualize skill distributions
- Analyze experience levels
- Track hiring metrics
- Export reports

---

## 📚 API Documentation

### CVAnalyzer Class
```python
class CVAnalyzer:
    """Analyzes CVs using Groq's LLM API."""
    
    def __init__(self, groq_api_key: str = None):
        """Initialize with optional Groq API key."""
        
    def analyze_cv(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Analyze a CV file and return structured results."""
```

### AICandidateSearch Class
```python
class AICandidateSearch:
    """Handles natural language candidate search."""
    
    def search_candidates(self, query: str) -> List[Dict[str, Any]]:
        """Search candidates using natural language query."""
```

### AdvancedCandidateMatcher Class
```python
class AdvancedCandidateMatcher:
    """Matches candidates to job requirements."""
    
    def match_candidates(
        self,
        required_skills: List[str],
        preferred_skills: List[str] = None,
        seniority: str = None,
        location: str = None,
        employment_type: str = None,
        experience_years: str = None,
        top_n: int = 10
    ) -> List[ScoredCandidate]:
        """Match candidates based on job requirements."""
```

## 🛠️ Development

### Project Structure
```
NaukriAI/
├── streamlit_app.py     # Main application
├── cv_analyser.py       # CV analysis module
├── groq_search.py       # Natural language search
├── advanced_matching.py # Candidate matching
├── docs_parser.py       # Document parsing
├── dataset.py           # Data management
├── requirements.txt     # Dependencies
└── README.md           # This file
```

### Adding New Features
1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Add tests if applicable
4. Run linter: `pylint *.py`
5. Commit changes: `git commit -m "Add your feature"`
6. Push to branch: `git push origin feature/your-feature`
7. Create a pull request

### Testing
Run the test suite:
```bash
pytest
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For questions or feedback, please contact [Your Email].

---

## 📈 Submission Notes
- All core hackathon requirements are implemented and demo-ready
- Pre-screening Q&A is live; automated background checks are planned for future release
- Outreach is fully personalized and ready for integration with email/LinkedIn APIs
- Codebase is clean, extensible, and thoroughly documented

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
