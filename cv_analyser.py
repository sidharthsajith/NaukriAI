import os
import json
import argparse
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from dotenv import load_dotenv

# Import our document parser
from docs_parser import DocumentParser
from groq import Groq


# Load environment variables
load_dotenv()


class CVAnalyzer:
    """
    A class to analyze CVs using Groq's LLM API.
    Performs HR and recruiter-style analysis of candidate CVs.
    """
    
    def __init__(self, groq_api_key: str = None):
        """
        Initialize the CV analyzer with Groq API key.
        
        Args:
            groq_api_key: Optional Groq API key. If not provided, will try to get from environment.
        """
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("Groq API key not provided. Set GROQ_API_KEY environment variable or pass it as an argument.")
        
        # Initialize Groq client
        self.client = Groq(api_key=self.groq_api_key)
        self.parser = DocumentParser()
    
    def _call_groq_api(self, prompt: str, model: str = "llama-3.3-70b-versatile") -> Dict[str, Any]:
        """
        Call Groq's API with the given prompt.
        
        Args:
            prompt: The prompt to send to the model
            model: The Groq model to use (default: llama-3.3-70b-versatile)
            
        Returns:
            dict: The JSON response from the API
        """
        messages = [
            {
                "role": "system",
                "content": "You are an experienced HR manager and technical recruiter with 10+ years of experience. "
                          "Your task is to analyze CVs and provide detailed, professional feedback. "
                          "Always respond with valid JSON that matches the requested schema."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=0.2,
                max_tokens=4000,
                response_format={"type": "json_object"}
            )
            
            # Extract the JSON content from the response
            content = response.choices[0].message.content
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If the response is not valid JSON, try to extract JSON from the response
                try:
                    # Try to find JSON in the response
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start >= 0 and end > start:
                        return json.loads(content[start:end])
                    raise
                except:
                    raise ValueError(f"Failed to parse LLM response as JSON: {content}")
                    
        except Exception as e:
            raise Exception(f"Error calling Groq API: {str(e)}")
    
    def analyze_cv(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Analyze a CV file and return the analysis results.
        
        Args:
            file_path: Path to the CV file (PDF or DOCX)
            
        Returns:
            dict: Analysis results in a structured format
            
        Raises:
            Exception: If there's an error during analysis
        """
        try:
            # Parse the document
            cv_data = self.parser.parse_document(file_path)
            
            # Prepare the prompt
            prompt = self._create_analysis_prompt(cv_data)
            
            # Call Groq API and get the analysis
            analysis = self._call_groq_api(prompt)
            
            # Generate interview questions
            interview_questions = self._generate_interview_questions(cv_data)

            # Return the structured result
            return {
                'status': 'success',
                'analysis': analysis,
                'suggested_interview_questions': interview_questions,
                'metadata': {
                    'file_path': str(file_path),
                    'file_type': 'pdf' if str(file_path).lower().endswith('.pdf') else 'docx'
                }
            }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _create_analysis_prompt(self, cv_data: Dict[str, Any]) -> str:
        """
        Create a detailed prompt for CV analysis.
        
        Args:
            cv_data: Parsed CV data from DocumentParser
            
        Returns:
            str: Formatted prompt for Groq API
        """
        # Extract text content
        text_content = cv_data.get('text', '')
        
        prompt = """Analyze the following CV in detail and provide a comprehensive analysis. 
Focus on both technical and soft skills, experience, and overall presentation. Look for:

1. Key strengths and qualifications
2. Potential red flags or inconsistencies
3. Areas that might need verification
4. Overall fit for technical roles
5. Any signs of potential exaggeration or misrepresentation

Format your response as a JSON object with the following structure:
{
  "candidate_summary": {
    "name": "Full name if available",
    "current_role": "Current/most recent position",
    "years_experience": "Estimated years of experience",
    "key_skills": ["list", "of", "key", "skills"]
  },
  "strengths": ["list", "of", "strengths"],
  "red_flags": ["list", "of", "potential", "issues"],
  "verification_needed": ["list", "of", "items", "to", "verify"],
  "overall_assessment": "Detailed assessment of the candidate",
  "recommendation": {
    "recommended": true/false,
    "reasoning": "Detailed reasoning behind the recommendation",
    "suggested_roles": ["list", "of", "suitable", "roles"],
    "suggested_compensation_range": {
      "min": 0,
      "max": 0,
      "currency": "USD"
    }
  }
}

CV Content:
"""
        prompt += text_content[:15000]  # Limit to avoid token limits
        return prompt

    def _generate_interview_questions(self, cv_data: Dict[str, Any]) -> List[str]:
        """
        Generate general interview questions based on CV content.

        Args:
            cv_data: Parsed CV data from DocumentParser

        Returns:
            List[str]: A list of suggested interview questions
        """
        text_content = cv_data.get('text', '')

        prompt = f"""Based on the following CV content, generate 5-7 general interview questions. 
The questions should help evaluate the candidate's overall suitability, covering aspects like their experience, 
key skills, problem-solving abilities, and behavioral traits. 

Format your response as a JSON object with a single key "interview_questions" which contains a list of strings (the questions).

CV Content:
{text_content[:4000]}
"""

        try:
            response_json = self._call_groq_api(prompt)
            return response_json.get("interview_questions", [])
        except Exception as e:
            # Log error or handle appropriately
            print(f"Error generating interview questions: {e}")
            return ["Could not generate interview questions at this time."]

def main():
    parser = argparse.ArgumentParser(description='Analyze a CV using Groq LLM')
    parser.add_argument('file_path', help='Path to the CV file (PDF or DOCX)')
    parser.add_argument('--api-key', help='Groq API key (optional if GROQ_API_KEY is set in environment)')
    parser.add_argument('--output', help='Output JSON file path (optional)')
    
    args = parser.parse_args()
    
    try:
        analyzer = CVAnalyzer(groq_api_key=args.api_key)
        result = analyzer.analyze_cv(args.file_path)
        
        if result['status'] == 'success':
            json_output = json.dumps(result, indent=2, ensure_ascii=False)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(json_output)
                print(f"Analysis saved to {args.output}")
            else:
                print(json_output)
        else:
            print(f"Error: {result.get('message', 'Unknown error')}")
            return 1
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())