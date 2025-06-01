import os
import json
from typing import List, Dict, Any
from groq import Groq
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Candidate:
    name: str
    seniority: str
    skills: List[str]
    location: List[str]
    employment_type: str
    experience_years: str

class AICandidateSearch:
    def __init__(self, dataset_path: str = 'dataset.json'):
        """Initialize the candidate search."""
        self.dataset_path = dataset_path
        self.dataset = self._load_dataset()
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY", "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")
        )
    
    def _load_dataset(self) -> List[Dict[str, Any]]:
        """Load the dataset from JSON file."""
        try:
            with open(self.dataset_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            from dataset import CandidateGenerator
            generator = CandidateGenerator(num_candidates=100)
            generator.save_to_json(self.dataset_path)
            return generator.dataset

    def _extract_search_terms(self, query: str) -> Dict[str, List[str]]:
        """Extract search terms from query and map to dataset fields."""
        terms = {
            'skills': [],
            'seniority': [],
            'location': [],
            'employment_type': [],
            'experience_years': [],
            'exclude_skills': []
        }
        
        # Convert query to lowercase for case-insensitive matching
        query_lower = query.lower()
        
        # Handle negative conditions (no/not/without + skill)
        negative_phrases = ['no ', 'not ', 'without ']
        for phrase in negative_phrases:
            if phrase in query_lower:
                # Get the text after the negative phrase
                after_phrase = query_lower.split(phrase, 1)[1]
                # Extract the next word/phrase as the negative term
                negative_term = after_phrase.split()[0]
                # Check if it's a known skill
                known_skills = [
                    'langchain', 'rag', 'agentic ai', 'generative-ai', 'llama index',
                    'langflow', 'python', 'javascript', 'react', 'node.js',
                    'machine learning', 'data science', 'cloud computing',
                    'devops', 'kubernetes', 'docker', 'aws', 'azure'
                ]
                
                for skill in known_skills:
                    if skill in negative_term or skill.split()[0] in negative_term:
                        terms['exclude_skills'].append(skill)
        
        # Check for seniority levels
        for level in ['junior', 'midlevel', 'senior']:
            if level in query_lower:
                terms['seniority'].append(level)
        
        # Check for employment types
        for emp_type in ['full-time', 'part-time', 'contract', 'remote']:
            if emp_type in query_lower:
                terms['employment_type'].append(emp_type)
        
        # Check for experience years
        for exp in ['1-3', '3-5', '5+', '10+', '15+']:
            if exp in query:
                terms['experience_years'].append(exp)
        
        # Check for locations
        locations = ['europe', 'asia', 'north america', 'south america', 'africa', 'australia']
        for loc in locations:
            if loc in query_lower:
                terms['location'].append(loc)
        
        # Extract skills (check against known skills)
        known_skills = [
            'langchain', 'rag', 'agentic ai', 'generative-ai', 'llama index',
            'langflow', 'python', 'javascript', 'react', 'node.js',
            'machine learning', 'data science', 'cloud computing',
            'devops', 'kubernetes', 'docker', 'aws', 'azure'
        ]
        
        # Extract positive skills (not in negative context)
        for skill in known_skills:
            if skill in query_lower:
                # Check if this skill is in a negative context
                is_negative = False
                for neg_skill in terms['exclude_skills']:
                    if neg_skill in skill or skill in neg_skill:
                        is_negative = True
                        break
                if not is_negative:
                    terms['skills'].append(skill)
        
        return terms
    
    def _match_candidates(self, search_terms: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Match candidates based on search terms."""
        if not any(v for k, v in search_terms.items() if k != 'exclude_skills'):
            return []
            
        matched = []
        
        for candidate in self.dataset:
            match = True
            
            # Check each field for positive matches
            for field, values in search_terms.items():
                if field == 'exclude_skills' or not values:
                    continue
                    
                candidate_value = candidate.get(field, '')
                if isinstance(candidate_value, list):
                    candidate_value = [str(v).lower() for v in candidate_value]
                    if not any(v in candidate_value for v in values):
                        match = False
                        break
                else:
                    candidate_value = str(candidate_value).lower()
                    if not any(v in candidate_value for v in values):
                        match = False
                        break
            
            # Check for excluded skills
            if match and search_terms.get('exclude_skills'):
                candidate_skills = [s.lower() for s in candidate.get('skills', [])]
                for skill in search_terms['exclude_skills']:
                    if any(skill in s or s in skill for s in candidate_skills):
                        match = False
                        break
                        
            if match:
                matched.append(candidate)
                
        return matched
    
    def _llm_system_prompt(self):
        return (
            "You are an expert AI recruiter. You will be given a user query and a list of candidates. "
            "Analyze the query and return the most relevant candidates as a JSON array under the key 'candidates', "
            "each with a 'reason' field. If you cannot decide with the given candidates, reply with a JSON object: {\"reflex\": true, \"reason\": \"Need more candidates\"}. "
            "Be concise and only ask for more candidates if you are truly unable to answer."
        )

    def search_candidates(self, query: str) -> List[Dict[str, Any]]:
        """
        Use the LLM to handle candidate searching and selection. Sends candidates in batches of 3, lets the LLM reflexively request more if needed.
        """
        if not query.strip():
            return []
        try:
            batch_size = 3
            idx = 0
            total = len(self.dataset)
            messages = [
                {"role": "system", "content": self._llm_system_prompt()},
                {"role": "user", "content": f"Search Query: {query}"}
            ]
            while idx < total:
                batch = self.dataset[idx:idx+batch_size]
                messages.append({
                    "role": "user",
                    "content": (
                        f"Candidates {idx+1}-{idx+len(batch)} of {total}:\n"
                        f"{json.dumps(batch, indent=2)}\n"
                        "If you can answer, return the best candidates as JSON. If not, reply with {\"reflex\": true}."
                    )
                })
                response = self.client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.2,
                    max_tokens=1500,
                    response_format={"type": "json_object"}
                )
                try:
                    result = json.loads(response.choices[0].message.content)
                except Exception as e:
                    print(f"LLM response error: {e}")
                    return []
                # If LLM returns candidates, return them
                if isinstance(result, dict) and result.get('candidates'):
                    return result['candidates']
                # If LLM asks for more, continue
                if isinstance(result, dict) and result.get('reflex'):
                    idx += batch_size
                    continue
                # If LLM returns a list, treat as candidates
                if isinstance(result, list):
                    return result
                # Otherwise, break
                break
            return []
        except Exception as e:
            print(f"Error in LLM search: {str(e)}")
            return []

    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Return the results as a JSON dump string.
        """
        return json.dumps(results, indent=2) if results else "[]"
        
    def generate_outreach_email(self, candidate_name: str, recruiter_name: str, company_name: str, 
                             job_title: str, work_location: str, key_requirements: str) -> str:
        """
        Generate a personalized outreach email using Groq.
        """
        try:
            # Prepare the prompt for the LLM
            system_prompt = """You are an expert recruiter who writes compelling and personalized outreach emails. 
            Create a professional yet engaging email that will catch the candidate's attention. 
            The email should be concise, personalized, and highlight why the opportunity is exciting."""
            
            user_prompt = f"""
            Write a personalized outreach email with the following details:
            - Candidate Name: {candidate_name}
            - Recruiter Name: {recruiter_name}
            - Company: {company_name}
            - Job Title: {job_title}
            - Work Location: {work_location}
            - Key Requirements: {key_requirements}
            
            The email should:
            1. Start with a personalized greeting
            2. Mention something specific about the candidate's background that matches the role
            3. Briefly describe the opportunity and why it's exciting
            4. Highlight 2-3 key requirements that match the candidate's profile
            5. Include a clear call-to-action for next steps
            6. End professionally with the recruiter's name and company
            
            Keep the tone professional but conversational. The email should be concise (3-4 short paragraphs max).
            """
            
            # Call Groq API
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract and return the generated email
            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content.strip()
            return ""
            
        except Exception as e:
            print(f"Error generating outreach email: {str(e)}")
            raise
