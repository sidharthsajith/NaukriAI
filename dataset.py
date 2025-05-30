import random
import json
from typing import List, Dict, Any

class CandidateGenerator:
    def __init__(self, num_candidates: int = 50):
        self.num_candidates = num_candidates
        self.names = self._load_names()
        self.locations = [
            "Europe", "Asia", "North America", "South America", "Africa", "Australia"
        ]
        self.skills = [
            "langchain", "rag", "agentic ai", "generative-ai", "llama index",
            "langflow", "python", "javascript", "react", "node.js",
            "machine learning", "data science", "cloud computing",
            "devops", "kubernetes", "docker", "aws", "azure"
        ]
        self.seniorities = ["junior", "midlevel", "senior"]
        self.employment_types = ["full-time", "part-time", "contract", "remote"]
        self.experience_years = ["1-3", "3-5", "5+", "10+", "15+"]

    def _load_names(self) -> List[str]:
        """Load common names from a file"""
        # In a real implementation, you might want to load names from a larger dataset
        first_names = ["John", "Sarah", "Michael", "Emily", "William", "Olivia", "James", "Ava", "Robert", "Sophia"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        return [f"{first} {last}" for first in first_names for last in last_names]

    def generate_candidate(self) -> Dict[str, Any]:
        """Generate a single candidate profile"""
        candidate = {
            "name": random.choice(self.names),
            "seniority": random.choice(self.seniorities),
            "skills": random.sample(self.skills, random.randint(3, 6)),
            "location": random.sample(self.locations, random.randint(1, 2)),
            "employment_type": random.choice(self.employment_types),
            "experience_years": random.choice(self.experience_years)
        }
        return candidate

    def generate_dataset(self) -> List[Dict[str, Any]]:
        """Generate a dataset of candidates"""
        dataset = []
        for _ in range(self.num_candidates):
            candidate = self.generate_candidate()
            dataset.append(candidate)
        return dataset

    def save_to_json(self, filename: str = "dataset.json"):
        """Save the generated dataset to a JSON file"""
        dataset = self.generate_dataset()
        with open(filename, 'w') as f:
            json.dump(dataset, f, indent=2)
            print(f"Generated {len(dataset)} candidates and saved to {filename}")

if __name__ == "__main__":
    # Create an instance of the generator
    generator = CandidateGenerator(num_candidates=1000)
    
    # Generate and save the dataset
    generator.save_to_json()
    
    # Print some statistics
    print("\nDataset Statistics:")
    print(f"Total candidates generated: {generator.num_candidates}")
    print(f"Unique names: {len(generator.names)}")
    print(f"Skills available: {len(generator.skills)}")
    print(f"Locations available: {len(generator.locations)}")
    print(f"Seniority levels: {len(generator.seniorities)}")
    print(f"Employment types: {len(generator.employment_types)}")
    print(f"Experience levels: {len(generator.experience_years)}")
    print(f"Total possible combinations: {len(generator.names) * len(generator.seniorities) * len(generator.experience_years)}")