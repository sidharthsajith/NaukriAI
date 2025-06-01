import json
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from groq import Groq
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import re

@dataclass
class CandidateMatch:
    """Data class to store matching results for a candidate."""
    name: str
    seniority: str
    skills: List[str]
    experience_years: str
    employment_type: str
    location: List[str]
    match_score: float
    skill_gaps: List[str]
    skill_matches: List[str]
    experience_match: float
    seniority_match: float
    employment_match: float
    location_match: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'seniority': self.seniority,
            'skills': self.skills,
            'experience_years': self.experience_years,
            'employment_type': self.employment_type,
            'location': self.location,
            'match_score': round(self.match_score, 2),
            'skill_gaps': self.skill_gaps,
            'skill_matches': self.skill_matches,
            'experience_match': round(self.experience_match, 2),
            'seniority_match': round(self.seniority_match, 2),
            'employment_match': round(self.employment_match, 2),
            'location_match': round(self.location_match, 2)
        }

class AdvancedCandidateMatcher:
    """Advanced candidate matching system with skill gap analysis."""
    
    def __init__(self, dataset_path: str = 'dataset.json'):
        """Initialize the matcher with the dataset."""
        self.dataset_path = dataset_path
        self.dataset = self._load_dataset()
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.skill_weights = self._initialize_skill_weights()
        
    def _load_dataset(self) -> List[Dict[str, Any]]:
        """Load the dataset from JSON file."""
        with open(self.dataset_path, 'r') as f:
            return json.load(f)
    
    def _initialize_skill_weights(self) -> Dict[str, float]:
        """Initialize default weights for different skills."""
        # These weights can be adjusted based on domain knowledge
        return {
            'python': 1.0,
            'javascript': 0.9,
            'react': 0.9,
            'node.js': 0.9,
            'machine learning': 1.2,
            'data science': 1.1,
            'cloud computing': 1.0,
            'aws': 1.0,
            'azure': 1.0,
            'kubernetes': 1.1,
            'docker': 1.0,
            'devops': 1.0,
            'rag': 1.2,
            'langchain': 1.2,
            'llama index': 1.2,
            'langflow': 1.1,
            'agentic ai': 1.3,
            'generative-ai': 1.3
        }
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for similarity comparison."""
        return ' '.join(re.sub(r'[^\w\s-]', '', text.lower()).split())
    
    def _calculate_skill_similarity(self, required_skills: List[str], candidate_skills: List[str]) -> Tuple[float, List[str], List[str]]:
        """Calculate skill similarity between required and candidate skills."""
        if not required_skills:
            return 1.0, [], []
            
        # Preprocess skills
        required_skills = [self._preprocess_text(skill) for skill in required_skills]
        candidate_skills = [self._preprocess_text(skill) for skill in candidate_skills]
        
        # Find matches and gaps
        matches = []
        gaps = []
        
        for req_skill in required_skills:
            found = False
            for cand_skill in candidate_skills:
                # Simple word-level matching (can be enhanced with embeddings)
                if req_skill in cand_skill or cand_skill in req_skill:
                    matches.append(cand_skill)
                    found = True
                    break
            if not found:
                gaps.append(req_skill)
        
        # Calculate match score with weights
        match_score = 0.0
        total_weight = 0.0
        
        for skill in required_skills:
            weight = self.skill_weights.get(skill, 1.0)
            total_weight += weight
            if any(skill in m or m in skill for m in matches):
                match_score += weight
        
        normalized_score = match_score / total_weight if total_weight > 0 else 0.0
        
        return normalized_score, gaps, matches
    
    def _calculate_experience_match(self, required_exp: str, candidate_exp: str) -> float:
        """Calculate experience match score."""
        # Map experience levels to numerical values
        exp_map = {
            '1-3': 1,
            '3-5': 2,
            '5-10': 3,
            '10+': 4,
            '15+': 5
        }
        
        req_level = exp_map.get(required_exp.lower(), 0)
        cand_level = exp_map.get(candidate_exp.lower(), 0)
        
        if req_level == 0 or cand_level == 0:
            return 0.5  # Default score if experience not specified
            
        # Higher is better, but not penalizing for over-qualification as much
        if cand_level >= req_level:
            return 1.0
        else:
            return max(0.1, 0.1 + (cand_level / req_level) * 0.9)  # At least 10% match
    
    def _calculate_seniority_match(self, required_seniority: str, candidate_seniority: str) -> float:
        """Calculate seniority match score."""
        seniority_levels = {
            'junior': 1,
            'midlevel': 2,
            'senior': 3
        }
        
        req_level = seniority_levels.get(required_seniority.lower(), 0)
        cand_level = seniority_levels.get(candidate_seniority.lower(), 0)
        
        if req_level == 0 or cand_level == 0:
            return 0.5  # Default score if seniority not specified
            
        # Higher is better, but not penalizing for over-qualification as much
        if cand_level >= req_level:
            return 1.0
        else:
            return max(0.1, 0.1 + (cand_level / req_level) * 0.9)  # At least 10% match
    
    def _calculate_employment_match(self, required_type: str, candidate_type: str) -> float:
        """Calculate employment type match score."""
        if required_type.lower() == candidate_type.lower():
            return 1.0
        # Consider remote as flexible
        if 'remote' in required_type.lower() or 'remote' in candidate_type.lower():
            return 0.8
        return 0.0
    
    def _calculate_location_match(self, required_locations: List[str], candidate_locations: List[str]) -> float:
        """Calculate location match score."""
        if not required_locations:
            return 1.0
            
        required_locations = [loc.lower() for loc in required_locations]
        candidate_locations = [loc.lower() for loc in candidate_locations]
        
        # Check for any overlap
        if any(loc in candidate_locations for loc in required_locations):
            return 1.0
        
        # Check for remote work
        if 'remote' in required_locations or 'remote' in candidate_locations:
            return 0.8
            
        return 0.0
    
    def match_candidates(
        self,
        required_skills: List[str],
        seniority: str = None,
        experience_years: str = None,
        employment_type: str = None,
        locations: List[str] = None,
        top_n: int = 10
    ) -> List[CandidateMatch]:
        """
        Match candidates based on job requirements.
        
        Args:
            required_skills: List of required skills
            seniority: Required seniority level (junior, midlevel, senior)
            experience_years: Required years of experience
            employment_type: Type of employment (full-time, part-time, contract)
            locations: List of preferred locations
            top_n: Number of top matches to return
            
        Returns:
            List of CandidateMatch objects sorted by match score
        """
        matches = []
        
        for candidate in self.dataset:
            # Calculate individual match scores
            skill_score, skill_gaps, skill_matches = self._calculate_skill_similarity(
                required_skills, candidate.get('skills', []))
                
            exp_score = self._calculate_experience_match(
                experience_years, candidate.get('experience_years', '')) if experience_years else 1.0
                
            seniority_score = self._calculate_seniority_match(
                seniority, candidate.get('seniority', '')) if seniority else 1.0
                
            employment_score = self._calculate_employment_match(
                employment_type, candidate.get('employment_type', '')) if employment_type else 1.0
                
            location_score = self._calculate_location_match(
                locations, candidate.get('location', [])) if locations else 1.0
            
            # Calculate weighted average score
            weights = {
                'skills': 0.5,
                'experience': 0.2,
                'seniority': 0.15,
                'employment': 0.1,
                'location': 0.05
            }
            
            total_score = (
                skill_score * weights['skills'] +
                exp_score * weights['experience'] +
                seniority_score * weights['seniority'] +
                employment_score * weights['employment'] +
                location_score * weights['location']
            ) / sum(weights.values())
            
            # Create match object
            match = CandidateMatch(
                name=candidate.get('name', 'Unknown'),
                seniority=candidate.get('seniority', ''),
                skills=candidate.get('skills', []),
                experience_years=candidate.get('experience_years', ''),
                employment_type=candidate.get('employment_type', ''),
                location=candidate.get('location', []),
                match_score=total_score,
                skill_gaps=skill_gaps,
                skill_matches=skill_matches,
                experience_match=exp_score,
                seniority_match=seniority_score,
                employment_match=employment_score,
                location_match=location_score
            )
            
            matches.append(match)
        
        # Sort by match score (descending)
        matches.sort(key=lambda x: x.match_score, reverse=True)
        
        # Return top N matches
        return matches[:top_n]
    
    def analyze_skill_gaps(self, candidate_skills: List[str], required_skills: List[str]) -> Dict[str, Any]:
        """
        Analyze skill gaps between a candidate and job requirements.
        
        Args:
            candidate_skills: List of candidate's skills
            required_skills: List of required skills for the job
            
        Returns:
            Dictionary with gap analysis
        """
        # Find missing skills
        candidate_skills_lower = [s.lower() for s in candidate_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        missing_skills = []
        matching_skills = []
        
        for req_skill in required_skills_lower:
            found = False
            for cand_skill in candidate_skills_lower:
                if req_skill in cand_skill or cand_skill in req_skill:
                    matching_skills.append(req_skill)
                    found = True
                    break
            if not found:
                missing_skills.append(req_skill)
        
        # Calculate coverage
        coverage = len(matching_skills) / len(required_skills) if required_skills else 0.0
        
        # Generate learning recommendations
        recommendations = []
        for skill in missing_skills:
            recommendations.append({
                'skill': skill,
                'resources': self._generate_learning_resources(skill)
            })
        
        return {
            'missing_skills': missing_skills,
            'matching_skills': matching_skills,
            'coverage': round(coverage * 100, 2),
            'recommendations': recommendations
        }
    
    def _generate_learning_resources(self, skill: str) -> List[Dict[str, str]]:
        """Generate learning resources for a skill."""
        # This is a simplified version - in practice, you might want to use an API or database
        resources = {
            'python': [
                {'title': 'Python Official Documentation', 'url': 'https://docs.python.org/3/'},
                {'title': 'Real Python Tutorials', 'url': 'https://realpython.com/'},
                {'title': 'Python for Data Science Handbook', 'url': 'https://jakevdp.github.io/PythonDataScienceHandbook/'}
            ],
            'javascript': [
                {'title': 'MDN JavaScript Guide', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide'},
                {'title': 'Eloquent JavaScript', 'url': 'https://eloquentjavascript.net/'},
                {'title': 'You Don\'t Know JS', 'url': 'https://github.com/getify/You-Dont-Know-JS'}
            ],
            'machine learning': [
                {'title': 'Fast.ai Practical Deep Learning', 'url': 'https://course.fast.ai/'},
                {'title': 'Google ML Crash Course', 'url': 'https://developers.google.com/machine-learning/crash-course'},
                {'title': 'Andrew Ng\'s Machine Learning Course', 'url': 'https://www.coursera.org/learn/machine-learning'}
            ],
            'data science': [
                {'title': 'Data Science Handbook', 'url': 'https://jakevdp.github.io/PythonDataScienceHandbook/'},
                {'title': 'Kaggle Learn', 'url': 'https://www.kaggle.com/learn'},
                {'title': 'DataCamp', 'url': 'https://www.datacamp.com/'}
            ],
            'cloud computing': [
                {'title': 'AWS Training and Certification', 'url': 'https://aws.amazon.com/training/'},
                {'title': 'Google Cloud Training', 'url': 'https://cloud.google.com/training'},
                {'title': 'Microsoft Learn', 'url': 'https://docs.microsoft.com/en-us/learn/'}
            ]
        }
        
        # Default resources if skill not found
        default_resources = [
            {'title': f'Search for {skill} on Coursera', 'url': f'https://www.coursera.org/search?query={skill.replace(" ", "+")}'},
            {'title': f'Search for {skill} on edX', 'url': f'https://www.edx.org/search?q={skill.replace(" ", "+")}'},
            {'title': f'Search for {skill} on YouTube', 'url': f'https://www.youtube.com/results?search_query={skill.replace(" ", "+")}+tutorial'}
        ]
        
        return resources.get(skill.lower(), default_resources)[:3]  # Return top 3 resources


class CandidateRanker:
    """Intelligent candidate ranking system."""
    
    def __init__(self, criteria_weights: Dict[str, float] = None):
        """
        Initialize the ranker with optional custom criteria weights.
        
        Args:
            criteria_weights: Dictionary mapping criteria to weights (sum should be 1.0)
        """
        self.criteria_weights = criteria_weights or {
            'skill_match': 0.4,
            'experience': 0.25,
            'seniority': 0.15,
            'education': 0.1,
            'cultural_fit': 0.1
        }
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def rank_candidates(
        self,
        candidates: List[Dict[str, Any]],
        job_description: str,
        company_culture: str = None,
        custom_criteria: Dict[str, float] = None
    ) -> List[Dict[str, Any]]:
        """
        Rank candidates based on multiple criteria.
        
        Args:
            candidates: List of candidate dictionaries
            job_description: Job description text
            company_culture: Description of company culture (optional)
            custom_criteria: Custom criteria and weights (optional)
            
        Returns:
            List of candidates with ranking scores
        """
        if custom_criteria:
            self.criteria_weights.update(custom_criteria)
        
        # Calculate scores for each candidate
        for candidate in candidates:
            # Skill match score (already calculated in matching)
            skill_score = candidate.get('match_score', 0) if 'match_score' in candidate else 0.5
            
            # Experience score (normalize to 0-1)
            experience = candidate.get('experience_years', '')
            exp_score = self._calculate_experience_score(experience)
            
            # Seniority score
            seniority = candidate.get('seniority', '').lower()
            seniority_score = self._calculate_seniority_score(seniority)
            
            # Education score (placeholder - would come from candidate data)
            education_score = 0.7  # Placeholder
            
            # Cultural fit score (using AI)
            cultural_fit_score = self._calculate_cultural_fit(
                candidate, job_description, company_culture) if company_culture else 0.5
            
            # Calculate weighted score
            weighted_score = (
                skill_score * self.criteria_weights['skill_match'] +
                exp_score * self.criteria_weights['experience'] +
                seniority_score * self.criteria_weights['seniority'] +
                education_score * self.criteria_weights['education'] +
                cultural_fit_score * self.criteria_weights['cultural_fit']
            )
            
            # Store scores
            candidate['ranking_scores'] = {
                'overall': round(weighted_score, 2),
                'skill_match': round(skill_score, 2),
                'experience': round(exp_score, 2),
                'seniority': round(seniority_score, 2),
                'education': round(education_score, 2),
                'cultural_fit': round(cultural_fit_score, 2)
            }
        
        # Sort by overall score
        return sorted(candidates, key=lambda x: x['ranking_scores']['overall'], reverse=True)
    
    def _calculate_experience_score(self, experience: str) -> float:
        """Calculate experience score from years of experience."""
        if not experience:
            return 0.5
            
        # Extract years from experience string
        years = 0
        if '-' in experience:
            years = float(experience.split('-')[0])
        elif '+' in experience:
            years = float(experience.replace('+', ''))
        
        # Normalize to 0-1 (assuming 0-20 years is the range)
        return min(1.0, max(0.0, years / 20.0))
    
    def _calculate_seniority_score(self, seniority: str) -> float:
        """Calculate seniority score."""
        seniority_levels = {
            'junior': 0.3,
            'midlevel': 0.6,
            'senior': 0.9,
            'lead': 1.0,
            'principal': 1.0
        }
        return seniority_levels.get(seniority.lower(), 0.5)
    
    def _calculate_cultural_fit(
        self,
        candidate: Dict[str, Any],
        job_description: str,
        company_culture: str
    ) -> float:
        """
        Use AI to calculate cultural fit score.
        
        This is a placeholder that would use Groq's LLM to analyze cultural fit.
        In a real implementation, you would want to fine-tune this based on your needs.
        """
        try:
            prompt = f"""
            You are an AI assistant helping to evaluate cultural fit between a candidate and a company.
            
            Job Description:
            {job_description}
            
            Company Culture:
            {company_culture}
            
            Candidate Profile:
            {json.dumps(candidate, indent=2)}
            
            Based on the information above, rate the cultural fit of this candidate on a scale of 0.0 to 1.0,
            where 0.0 is a poor fit and 1.0 is an excellent fit. Consider factors like work style, values,
            and alignment with company culture.
            
            Return a JSON object with a single key 'cultural_fit_score' containing the score.
            """
            
            response = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant that evaluates cultural fit between candidates and companies. Return only a JSON object with a 'cultural_fit_score' field."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.2,
                max_tokens=100,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return float(result.get('cultural_fit_score', 0.5))
            
        except Exception as e:
            print(f"Error calculating cultural fit: {str(e)}")
            return 0.5  # Default score on error


class BackgroundChecker:
    """AI-powered background checking and pre-screening system."""
    
    def __init__(self):
        """Initialize the background checker with Groq client."""
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    async def generate_interview_questions(
        self,
        candidate_profile: Dict[str, Any],
        job_description: str,
        num_questions: int = 5,
        question_types: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate interview questions based on candidate profile and job requirements.
        
        Args:
            candidate_profile: Dictionary containing candidate information
            job_description: Job description text
            num_questions: Number of questions to generate
            question_types: Types of questions to generate (e.g., technical, behavioral, situational)
            
        Returns:
            List of generated questions with metadata
        """
        if question_types is None:
            question_types = ["technical", "behavioral", "situational"]
        
        try:
            prompt = f"""
            You are an expert interviewer creating customized interview questions based on a candidate's profile.
            
            Candidate Profile:
            {json.dumps(candidate_profile, indent=2)}
            
            Job Description:
            {job_description}
            
            Generate {num_questions} interview questions that assess the candidate's fit for this role.
            Include a mix of the following question types: {', '.join(question_types)}.
            
            For each question, include:
            1. The question text
            2. Question type (from the provided types)
            3. What the answer should demonstrate
            4. Relevant skills or experience being assessed
            
            Return the questions as a JSON array of objects with these fields:
            - question: The interview question
            - type: The question type
            - evaluates: What the question evaluates
            - skills: List of relevant skills being assessed
            
            Format the response as valid JSON only, with no additional text.
            """
            
            response = await self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert interviewer creating customized interview questions. Return only valid JSON with no additional text."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get('questions', [])
            
        except Exception as e:
            print(f"Error generating interview questions: {str(e)}")
            return []
    
    async def verify_employment_history(
        self,
        candidate_name: str,
        employment_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Verify employment history using AI (simulated).
        
        In a real implementation, this would integrate with background check services.
        This is a placeholder that simulates the process.
        """
        try:
            prompt = f"""
            You are an AI assistant helping to verify employment history.
            
            Candidate: {candidate_name}
            
            Employment History:
            {json.dumps(employment_history, indent=2)}
            
            Analyze this employment history for any potential red flags such as:
            - Employment gaps
            - Job title inconsistencies
            - Suspiciously short job durations
            - Overlapping employment periods
            
            Return a JSON object with:
            - overall_status: "verified", "needs_review", or "concerns"
            - red_flags: List of any potential issues found
            - confidence_score: A score from 0.0 to 1.0 indicating confidence in verification
            - notes: Any additional notes or observations
            
            Format the response as valid JSON only, with no additional text.
            """
            
            response = await self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant that analyzes employment history. Return only valid JSON with no additional text."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error verifying employment history: {str(e)}")
            return {
                'overall_status': 'error',
                'red_flags': ['Error during verification'],
                'confidence_score': 0.0,
                'notes': f'Error: {str(e)}'
            }
    
    async def generate_pre_screening_report(
        self,
        candidate_profile: Dict[str, Any],
        job_description: str
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive pre-screening report for a candidate.
        
        This combines interview questions, employment verification, and other checks.
        """
        try:
            # Generate interview questions
            questions = await self.generate_interview_questions(candidate_profile, job_description)
            
            # Verify employment history (simulated)
            employment_verification = {}
            if 'employment_history' in candidate_profile:
                employment_verification = await self.verify_employment_history(
                    candidate_profile.get('name', 'Candidate'),
                    candidate_profile['employment_history']
                )
            
            # Generate overall assessment
            assessment_prompt = f"""
            You are an AI recruitment assistant creating a pre-screening report.
            
            Candidate Profile:
            {json.dumps(candidate_profile, indent=2)}
            
            Job Description:
            {job_description}
            
            Employment Verification:
            {json.dumps(employment_verification, indent=2)}
            
            Generate a comprehensive pre-screening report with the following sections:
            1. Summary of candidate's qualifications
            2. Key strengths for this role
            3. Potential concerns or gaps
            4. Recommended next steps
            
            Return the report as a JSON object with these sections.
            Format the response as valid JSON only, with no additional text.
            """
            
            response = await self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI recruitment assistant creating a pre-screening report. Return only valid JSON with no additional text."
                    },
                    {
                        "role": "user",
                        "content": assessment_prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            report = json.loads(response.choices[0].message.content)
            
            # Combine all information
            return {
                'candidate_info': {
                    'name': candidate_profile.get('name'),
                    'email': candidate_profile.get('email'),
                    'phone': candidate_profile.get('phone')
                },
                'job_title': job_description.split('\n')[0] if job_description else 'Unknown Position',
                'interview_questions': questions,
                'employment_verification': employment_verification,
                'assessment': report,
                'generated_at': datetime.datetime.now().isoformat(),
                'status': 'completed'
            }
            
        except Exception as e:
            print(f"Error generating pre-screening report: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'generated_at': datetime.datetime.now().isoformat()
            }
