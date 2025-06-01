import json
from typing import List, Dict, Any, Tuple
import numpy as np
from groq import Groq
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class ScoredCandidate:
    candidate: Dict[str, Any]
    score: float
    skill_matches: List[str]
    missing_skills: List[str]
    skill_gap_analysis: Dict[str, str]
    interview_questions: List[str] = None

class AdvancedCandidateMatcher:
    def __init__(self, dataset_path: str = 'dataset.json'):
        """Initialize the advanced candidate matcher."""
        self.dataset_path = dataset_path
        self.dataset = self._load_dataset()
        self.client = Groq(
            api_key=st.secrets["groq"]["api_key_1"]
        )
    
    def _load_dataset(self) -> List[Dict[str, Any]]:
        """Load the dataset from JSON file."""
        with open(self.dataset_path, 'r') as f:
            return json.load(f)
    
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
        """
        Match candidates based on job requirements using advanced scoring.
        
        Args:
            required_skills: List of required skills for the position
            preferred_skills: List of preferred but not required skills
            seniority: Desired seniority level
            location: Desired location
            employment_type: Type of employment (full-time, part-time, contract)
            experience_years: Required years of experience
            top_n: Number of top candidates to return
            
        Returns:
            List of ScoredCandidate objects sorted by match score
        """
        if preferred_skills is None:
            preferred_skills = []
            
        scored_candidates = []
        
        for candidate in self.dataset:
            # Initial filtering
            if seniority and candidate.get('seniority') != seniority:
                continue
            if location and location.lower() not in [loc.lower() for loc in candidate.get('location', [])]:
                continue
            if employment_type and employment_type.lower() != candidate.get('employment_type', '').lower():
                continue
            if experience_years and experience_years != candidate.get('experience_years'):
                continue
                
            # Calculate skill matches
            candidate_skills = set(skill.lower() for skill in candidate.get('skills', []))
            required_skills_lower = [s.lower() for s in required_skills]
            preferred_skills_lower = [s.lower() for s in preferred_skills]
            
            # Calculate skill matches and gaps
            matched_required = [s for s in required_skills_lower if s in candidate_skills]
            matched_preferred = [s for s in preferred_skills_lower if s in candidate_skills]
            missing_required = [s for s in required_skills_lower if s not in candidate_skills]
            
            # Skip if missing required skills
            if missing_required:
                continue
                
            # Calculate base score (0-100)
            score = 0
            
            # Base score from required skills (50% of total)
            if required_skills_lower:
                score += 50 * (len(matched_required) / len(required_skills_lower))
            
            # Bonus for preferred skills (30% of total)
            if preferred_skills_lower:
                score += 30 * (len(matched_preferred) / len(preferred_skills_lower))
            
            # Seniority bonus (10% of total)
            if seniority and candidate.get('seniority') == seniority:
                score += 10
                
            # Experience bonus (10% of total)
            if experience_years and candidate.get('experience_years') == experience_years:
                score += 10
            
            # Generate skill gap analysis
            skill_gap_analysis = self._generate_skill_gap_analysis(
                candidate_skills, 
                required_skills_lower + preferred_skills_lower
            )
            
            # Generate interview questions
            interview_questions = self._generate_interview_questions(
                candidate, 
                required_skills_lower + preferred_skills_lower
            )
            
            scored_candidate = ScoredCandidate(
                candidate=candidate,
                score=min(100, score),  # Cap at 100
                skill_matches=matched_required + matched_preferred,
                missing_skills=missing_required,
                skill_gap_analysis=skill_gap_analysis,
                interview_questions=interview_questions
            )
            
            scored_candidates.append(scored_candidate)
        
        # Sort by score in descending order
        scored_candidates.sort(key=lambda x: x.score, reverse=True)
        
        return scored_candidates[:top_n]
    
    def _generate_skill_gap_analysis(
        self, 
        candidate_skills: set, 
        required_skills: List[str]
    ) -> Dict[str, str]:
        """Generate skill gap analysis for a candidate."""
        missing_skills = [s for s in required_skills if s not in candidate_skills]
        
        if not missing_skills:
            return {"status": "All required skills met"}
            
        # Use Groq to generate gap analysis
        prompt = f"""
        For the following missing skills, provide a brief analysis of the learning path or 
        alternative skills that could compensate for each missing skill.
        
        Missing skills: {', '.join(missing_skills)}
        
        Candidate's current skills: {', '.join(candidate_skills)}
        
        Provide the analysis in a structured format with each skill as a key and the analysis as the value.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful career advisor providing skill gap analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse the response into a dictionary
            analysis = {}
            lines = response.choices[0].message.content.split('\n')
            current_skill = None
            
            for line in lines:
                line = line.strip()
                if ':' in line:
                    current_skill, analysis_text = line.split(':', 1)
                    analysis[current_skill.strip()] = analysis_text.strip()
                elif current_skill and line:
                    analysis[current_skill] += ' ' + line
            
            return analysis
            
        except Exception as e:
            return {"error": f"Failed to generate skill gap analysis: {str(e)}"}
    
    def _generate_interview_questions(
        self, 
        candidate: Dict[str, Any], 
        required_skills: List[str]
    ) -> List[str]:
        """Generate interview questions based on candidate profile and required skills."""
        candidate_skills = set(skill.lower() for skill in candidate.get('skills', []))
        missing_skills = [s for s in required_skills if s not in candidate_skills]
        
        prompt = f"""
        Generate 5 technical interview questions to assess a candidate's fit for a position.
        
        Candidate Profile:
        - Name: {candidate.get('name')}
        - Seniority: {candidate.get('seniority')}
        - Current Skills: {', '.join(candidate.get('skills', []))}
        - Experience: {candidate.get('experience_years')}
        
        Required Skills: {', '.join(required_skills)}
        
        Missing Skills to Focus On: {', '.join(missing_skills) if missing_skills else 'None'}
        
        Please provide 5 specific technical interview questions that would help evaluate both 
        the candidate's existing skills and their ability to quickly learn the missing skills.
        Format the response as a numbered list of questions.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an experienced technical interviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            
            # Parse the response into a list of questions
            questions = []
            lines = response.choices[0].message.content.split('\n')
            
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-')):
                    # Remove numbering/bullet points
                    question = line.split('.', 1)[1].strip() if '.' in line else line[1:].strip()
                    questions.append(question)
            
            return questions[:5]  # Return at most 5 questions
            
        except Exception as e:
            return [
                f"Tell me about your experience with {skill}?" 
                for skill in required_skills[:5]
            ]
    
    def generate_candidate_report(
        self, 
        candidate: ScoredCandidate,
        job_title: str,
        job_description: str
    ) -> str:
        """Generate a comprehensive candidate evaluation report."""
        report = """# Candidate Evaluation Report
        
## Position: {job_title}

## Candidate: {candidate_name}

## Match Score: {score:.1f}/100

## Skills Assessment
**Matched Skills:** {matched_skills}

**Missing Skills:** {missing_skills}

## Skill Gap Analysis
""".format(
            job_title=job_title,
            candidate_name=candidate.candidate['name'],
            score=candidate.score,
            matched_skills=', '.join(candidate.skill_matches) if candidate.skill_matches else 'None',
            missing_skills=', '.join(candidate.missing_skills) if hasattr(candidate, 'missing_skills') and candidate.missing_skills else 'None'
        )
        
        # Add skill gap analysis
        if hasattr(candidate, 'skill_gap_analysis') and candidate.skill_gap_analysis:
            report += "\n### Detailed Skill Gap Analysis\n"
            for skill, analysis in candidate.skill_gap_analysis.items():
                report += f"- **{skill}:** {analysis}\n"
        
        # Add interview questions
        if hasattr(candidate, 'interview_questions') and candidate.interview_questions:
            report += "\n## Recommended Interview Questions\n"
            for i, question in enumerate(candidate.interview_questions, 1):
                report += f"{i}. {question}\n"
        
        # Add overall recommendation
        report += "\n## Overall Recommendation\n"
        if candidate.score >= 80:
            report += "**Strongly Recommended** - This candidate has an excellent match with the required skills and experience."
        elif candidate.score >= 60:
            report += "**Recommended** - This candidate meets most requirements and shows potential for growth."
        elif candidate.score >= 40:
            report += "**Consider with Caution** - This candidate has some relevant skills but significant gaps exist."
        else:
            report += "**Not Recommended** - This candidate does not meet the minimum requirements for this position."
        
        return report
