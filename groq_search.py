import os
import json
import re
from typing import List, Dict, Any, Set, Optional
from groq import Groq
from collections import defaultdict

class AICandidateSearch:
    def __init__(self):
        """Initialize the AI-powered candidate search."""
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY", "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")
        )
        self._load_dataset()
    
    def _load_dataset(self):
        """Load the dataset."""
        try:
            with open('dataset.json', 'r') as f:
                self.dataset = json.load(f)
        except FileNotFoundError:
            from dataset import CandidateGenerator
            generator = CandidateGenerator(num_candidates=100)
            generator.save_to_json()
            self.dataset = generator.dataset

    def _extract_keywords(self, query: str) -> Set[str]:
        """Extract relevant keywords from the search query."""
        # Remove common stop words and split into words
        stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", 
                     "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 
                     'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 
                     'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 
                     'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 
                     'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 
                     'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
                     'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
                     'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
                     'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 
                     'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
                     'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 
                     'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', 
                     "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 
                     'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', 
                     "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', 
                     "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', 
                     "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"}
        
        # Extract words, remove punctuation and convert to lowercase
        words = re.findall(r'\b\w+\b', query.lower())
        # Filter out stop words and short words
        keywords = {word for word in words if word not in stop_words and len(word) > 2}
        return keywords
    
    def _score_candidate(self, candidate: Dict[str, Any], keywords: Set[str]) -> int:
        """Score a candidate based on keyword matches."""
        score = 0
        
        # Check skills (higher weight)
        for skill in candidate.get('skills', []):
            skill_lower = skill.lower()
            for keyword in keywords:
                if keyword in skill_lower:
                    score += 3  # Higher weight for skill matches
        
        # Check other fields (lower weight)
        for field in ['seniority', 'location', 'employment_type', 'experience_years']:
            value = candidate.get(field, '')
            if isinstance(value, list):
                value = ' '.join(value)
            value = str(value).lower()
            for keyword in keywords:
                if keyword in value:
                    score += 1
        
        return score
    
    def _filter_candidates(self, query: str, top_n: int = 20) -> List[Dict[str, Any]]:
        """Filter candidates based on the search query."""
        if not query.strip():
            return []
            
        keywords = self._extract_keywords(query)
        if not keywords:
            return []
        
        # Score all candidates
        scored_candidates = []
        for candidate in self.dataset:
            score = self._score_candidate(candidate, keywords)
            if score > 0:
                scored_candidates.append((score, candidate))
        
        # Sort by score (descending) and take top N
        scored_candidates.sort(reverse=True, key=lambda x: x[0])
        return [candidate for score, candidate in scored_candidates[:top_n]]
    
    def _create_system_prompt(self) -> str:
        """Create a system prompt that understands candidate search."""
        return """You are an AI assistant that helps find the best candidates based on job requirements.
        You'll be given a list of candidate profiles and a search query.
        Your task is to analyze the query and return the most relevant candidates.
        Format your response as a JSON object with 'candidates' as an array of candidate objects.
        Each candidate should include a 'reason' field explaining the match.
        """
    
    def search_candidates(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for candidates using natural language processing.
        
        Args:
            query: Natural language search query
            
        Returns:
            List of candidate dictionaries with match reasons
        """
        if not query.strip():
            return []
            
        try:
            # First, filter candidates based on keywords
            filtered_candidates = self._filter_candidates(query)
            
            if not filtered_candidates:
                return []
                
            # Prepare the prompt with filtered candidates
            messages = [
                {"role": "system", "content": self._create_system_prompt()},
                {
                    "role": "user",
                    "content": f"""Search Query: {query}
                    
                    Filtered Candidates (top {min(20, len(filtered_candidates))} of {len(self.dataset)} total):
                    {json.dumps(filtered_candidates, indent=2)}
                    
                    Please return the most relevant candidates in JSON format with 'candidates' array.
                    For each candidate, include a 'reason' field explaining why they are a good match.
                    Focus on matching skills, experience, and other relevant criteria from the query."""
                }
            ]
            
            # Get AI response
            response = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            # Parse and return results
            result = json.loads(response.choices[0].message.content)
            return result.get('candidates', [])
            
        except Exception as e:
            print(f"Error searching candidates: {str(e)}")
            return []

    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Format AI search results into a readable string.
        
        Args:
            results: List of candidate dictionaries with match reasons
            
        Returns:
            Formatted string of results
        """
        if not results:
            return "🔍 No matching candidates found. Try a different search query."
            
        formatted = ["✨ Top Matching Candidates:"]
        
        for i, candidate in enumerate(results, 1):
            formatted.append(f"\n🔹 Candidate {i}:")
            formatted.append(f"   👤 {candidate.get('name', 'N/A')}")
            
            # Highlight key details
            if 'seniority' in candidate:
                formatted.append(f"   👔 {candidate['seniority'].title()}")
            if 'skills' in candidate and candidate['skills']:
                formatted.append(f"   🛠️  Skills: {', '.join(candidate['skills'][:3])}" + 
                              ("..." if len(candidate['skills']) > 3 else ""))
            if 'location' in candidate and candidate['location']:
                formatted.append(f"   🌍 {', '.join(candidate['location'])}")
            if 'reason' in candidate:
                formatted.append(f"   💡 Match Reason: {candidate['reason']}")
                
        return '\n'.join(formatted)

def interactive_search():
    """Run an interactive search session with natural language queries."""
    print("🤖 AI-Powered Candidate Search")
    print("Type 'exit' or press Ctrl+C to quit\n")
    
    search = AICandidateSearch()
    
    try:
        while True:
            try:
                query = input("🔍 Search for candidates (e.g., 'senior python developer in Europe'): ")
                
                if query.lower() in ('exit', 'quit'):
                    print("👋 Goodbye!")
                    break
                
                print("\n🔍 Searching...")
                results = search.search_candidates(query)
                
                print("\n" + "="*50)
                print(search.format_results(results))
                print("\n" + "="*50 + "\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try a different search query.\n")
                
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        print("The application encountered an error and needs to close.")

if __name__ == "__main__":
    interactive_search()
