import os
import json
from groq import Groq
from typing import List, Dict, Any

class CandidateSearch:
    def __init__(self):
        self.client = Groq(
            api_key="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"
        )
        
        # Load dataset
        with open('dataset.json', 'r') as f:
            self.dataset = json.load(f)

    def search_candidates(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for candidates based on the user query
        Args:
            query (str): User's search query
        Returns:
            List[Dict[str, Any]]: List of matched candidates
        """
        # Create a structured prompt with dataset schema
        schema_prompt = """
        You are a candidate search assistant. The dataset contains candidate profiles with the following structure:
        {
            "name": string,
            "seniority": string ("junior", "midlevel", "senior"),
            "skills": array of strings,
            "location": array of strings,
            "employment_type": string,
            "experience_years": string
        }

        Your task is to analyze the user query and return indices of candidates that match the criteria. 
        Use logical operators (AND, OR, NOT) to combine conditions.
        
        Examples:
        - For "5+ experience": check if experience_years is "5+" or greater
        - For "skills in llama index or langchain": check if either skill is present in the skills array
        - For "not both": ensure only one of the conditions is true
        """

        # Combine schema with user query
        prompt = f"""
        {schema_prompt}
        
        Query: {query}
        
        Return format: [1, 5, 8] (indices of matching candidates)
        """

        # Get Groq response
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            stream=False,
        )

        # Parse the response
        try:
            indices_str = chat_completion.choices[0].message.content.strip()
            # Try to parse as JSON array
            indices = json.loads(indices_str)
            # Validate the response
            if not isinstance(indices, list) or not all(isinstance(i, int) for i in indices):
                raise ValueError("Invalid response format")
        except (json.JSONDecodeError, IndexError, ValueError) as e:
            print(f"Error parsing Groq response: {str(e)}")
            # Try to extract indices from text if JSON parsing fails
            try:
                # Look for numbers in the response
                import re
                numbers = re.findall(r'\d+', indices_str)
                indices = [int(n) for n in numbers if 0 <= int(n) < len(self.dataset)]
                if not indices:
                    print("No valid indices found in response")
                    return []
            except Exception:
                print("Failed to extract indices from response")
                return []

        # Return matching candidates
        return [self.dataset[i] for i in indices if 0 <= i < len(self.dataset)]

    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Format search results into a readable string
        Args:
            results (List[Dict[str, Any]]): List of candidate dictionaries
        Returns:
            str: Formatted string of results
        """
        if not results:
            return "No candidates found matching your criteria"

        formatted = []
        for candidate in results:
            formatted.append(f"""
Name: {candidate['name']}
Seniority: {candidate['seniority']}
Skills: {', '.join(candidate['skills'])}
Location: {', '.join(candidate['location'])}
Employment Type: {candidate['employment_type']}
Experience: {candidate['experience_years']}
""")

        return '\n'.join(formatted)

# Example usage
def main():
    search = CandidateSearch()
    
    while True:
        query = input("\nEnter your search query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
            
        results = search.search_candidates(query)
        print("\nSearch Results:")
        print(search.format_results(results))

if __name__ == "__main__":
    main()
