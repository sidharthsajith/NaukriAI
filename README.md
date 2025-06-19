# NaukriAI: AI-Powered Hiring Copilot

**Submission for: HireAI by 100xEngineers Hackathon**  
**Category:** LLMs / AI for Recruitment

## 📋 Table of Contents
- [Features](#-key-features)
- [Technical Architecture](#-technical-architecture)
- [Core Components](#-core-components)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Development](#-development)
- [License](#-license)

---

## 🚀 Key Features

### 🔍 PeopleGPT Search
- Natural language queries for candidate search
- Real-time semantic understanding
- Multi-factor ranking and filtering

### 📄 CV Analysis
- Parse PDF/DOCX resumes
- Extract skills, experience, and education
- Identify red flags and potential issues

### 🎯 Advanced Matching
- Smart scoring based on job requirements
- Skill gap analysis
- AI-generated interview questions

### 📊 Talent Analytics
- Interactive dashboard
- Visualize skill distributions
- Track hiring metrics

### ✉️ Outreach Automation
- Generate personalized messages
- Multiple tone options
- Track response rates

---

## 🏗️ Technical Architecture

NaukriAI is built with a modern, scalable architecture:

```mermaid
graph TD
    A[React + Tailwind Frontend] --> B[API Layer (Python)]
    B --> C[AI Processing (Groq LLM)]
    B --> D[Document Parser]
    B --> E[Scoring Engine]
    B --> F[Analytics Engine]
    B --> G[Data Layer (JSON/DB)]
    B --> H[File Upload Handler]
    C --> G
    D --> G
    F --> G
```

### Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **AI/ML**: Groq LLM API
- **Data**: JSON-based storage
- **Processing**: Multi-threaded pipelines

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

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Groq API key
- Required packages (see `requirements.txt`)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd NaukriAI
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
echo "GROQ_API_KEY=your_api_key_here" > .env
```

## 💻 Usage

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. Open your browser to `http://localhost:8501`

### Basic Workflow

1. **Search Candidates**
   - Use natural language to find candidates
   - Filter by skills, location, experience
   - Save your favorite candidates

2. **Analyze Resumes**
   - Upload candidate resumes
   - View detailed skill analysis
   - Get AI-powered insights

3. **Match to Jobs**
   - Define job requirements
   - Get ranked candidates
   - Generate interview questions

4. **Outreach**
   - Create personalized messages
   - Track responses
   - Schedule interviews

### Example Queries
- "Find senior Python developers with 5+ years experience"
- "Show me ML engineers in Europe open to remote work"
- "Rank candidates for a Full Stack Developer role"

---

## 🛠️ Development

### Project Structure
```
NaukriAI/
├── streamlit_app.py     # Main application
├── cv_analyser.py       # CV analysis
├── groq_search.py       # Search functionality
├── advanced_matching.py # Candidate matching
├── docs_parser.py       # Document parsing
├── dataset.py           # Data management
└── requirements.txt     # Dependencies
```

### Setup for Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Start the development server:
```bash
streamlit run streamlit_app.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙋‍♂️ Need Help?

Open an issue or contact us at [your-email@example.com](mailto:your-email@example.com)

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
