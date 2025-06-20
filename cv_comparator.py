"""cv_comparator.py
Compare two CVs against recruiter criteria using Groq LLM
Copyright (c) 2025 NaukriAI
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Union

import streamlit as st  # Re-use Streamlit secrets handling for local dev parity
from dotenv import load_dotenv
from groq import Groq

from docs_parser import DocumentParser

# ---------------------------------------------------------------------------
# Environment / setup
# ---------------------------------------------------------------------------
load_dotenv()


class CVComparator:
    """Compare two CVs and recommend the better fit for the recruiter's needs.

    The class re-uses :class:`docs_parser.DocumentParser` to extract raw text from
    the CVs and Groq's LLM to do the reasoning / comparison in a structured way.
    """

    def __init__(self, groq_api_key: str | None = None):
        # Pull from Streamlit secrets first for consistency with the rest of the
        # codebase, falling back to environment variable.
        self.groq_api_key: str | None = (
            groq_api_key or (st.secrets.get("groq", {}).get("api_key_1") if hasattr(st, "secrets") else None)
        )
        if not self.groq_api_key:
            # Last-ditch attempt – environment variable.
            self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError(
                "Groq API key not provided. Set it via Streamlit secrets or the GROQ_API_KEY environment variable."
            )

        self.client = Groq(api_key=self.groq_api_key)
        self.parser = DocumentParser()

    # ---------------------------------------------------------------------
    # Private helpers
    # ---------------------------------------------------------------------
    def _call_groq_api(self, prompt: str, *, model: str = "llama-3.3-70b-versatile") -> Dict[str, Any]:
        """Wrapper around Groq chat completion with sensible defaults & JSON enforcement."""
        messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "You are an experienced HR manager and technical recruiter. "
                    "Always respond with valid JSON matching the requested schema."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.2,
            max_tokens=4000,
            response_format={"type": "json_object"},
        )
        content: str = response.choices[0].message.content
        # Attempt to parse JSON strictly; fall back to finding first/last braces.
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start == -1 or end <= start:
                raise ValueError(f"Groq response is not valid JSON: {content}")
            return json.loads(content[start:end])

    def _create_comparison_prompt(self, cv1_text: str, cv2_text: str, criteria: str) -> str:
        """Craft the comparison prompt with an explicit JSON schema."""
        schema = {
            "best_candidate": "1 if first CV, 2 if second CV",
            "reasoning": "Detailed reasoning",
            "candidate_1_summary": {
                "key_strengths": "[]",
                "red_flags": "[]",
            },
            "candidate_2_summary": {
                "key_strengths": "[]",
                "red_flags": "[]",
            },
        }
        prompt = (
            "You will be given two candidate CVs (Candidate 1 and Candidate 2) as well as a description of "
            "the recruiter's ideal candidate. Analyse both CVs against the criteria and recommend which one is the "
            "best fit. Always answer in valid JSON exactly matching this schema:\n" + json.dumps(schema, indent=2) + "\n\n"  # noqa: E501
            "Recruiter criteria: "
            f"""{criteria}\n\nCV of Candidate 1:\n{cv1_text[:8000]}\n\nCV of Candidate 2:\n{cv2_text[:8000]}"""
        )
        return prompt

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def compare(
        self,
        cv1_path: Union[str, Path],
        cv2_path: Union[str, Path],
        criteria: str,
        *,
        model: str = "llama-3.3-70b-versatile",
    ) -> Dict[str, Any]:
        """Compare *cv1* and *cv2* against *criteria* and return structured result."""
        cv1_text = self.parser.parse_document(cv1_path).get("text", "")
        cv2_text = self.parser.parse_document(cv2_path).get("text", "")
        prompt = self._create_comparison_prompt(cv1_text, cv2_text, criteria)
        return self._call_groq_api(prompt, model=model)


# ---------------------------------------------------------------------------
# CLI utility
# ---------------------------------------------------------------------------

def _cli() -> int:
    parser = argparse.ArgumentParser(description="Compare two CVs and pick the best candidate.")
    parser.add_argument("cv1", help="Path to first candidate CV (pdf, docx)")
    parser.add_argument("cv2", help="Path to second candidate CV (pdf, docx)")
    parser.add_argument("--criteria", "-c", required=True, help="Description of the ideal candidate")
    parser.add_argument("--api-key", help="Groq API key (overrides env/secrets)")
    parser.add_argument("--model", default="llama-3.3-70b-versatile", help="Groq model to use")
    parser.add_argument("--output", "-o", help="Optional path to save JSON result")

    args = parser.parse_args()

    comparator = CVComparator(groq_api_key=args.api_key)
    result = comparator.compare(args.cv1, args.cv2, args.criteria, model=args.model)

    json_output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(json_output, encoding="utf-8")
        print(f"Comparison saved to {args.output}")
    else:
        print(json_output)

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(_cli())
