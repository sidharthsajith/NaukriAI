"""
FastAPI wrapper around the core business logic that was originally exposed through the Streamlit
UI (see `streamlit_app.py`). Every public function that performed data-processing or AI inference
has been mapped to a HTTP endpoint so it can be consumed programmatically.

Run locally:
    uvicorn fastapi_app:app --reload
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import List, Optional, Any, Dict

import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Local modules – these are already a part of the project.
from cv_analyser import CVAnalyzer
from cv_comparator import CVComparator
from groq_search import AICandidateSearch
from advanced_matching import AdvancedCandidateMatcher, ScoredCandidate

###############################################################################
# Data helpers                                                                 
###############################################################################
DATASET_PATH = Path(__file__).with_name("dataset.json")
_df_cache: Optional[pd.DataFrame] = None  # Lazy-loaded global cache


def load_data() -> pd.DataFrame:
    """Read the JSON dataset into a cached `pd.DataFrame`."""
    global _df_cache
    if _df_cache is not None:
        return _df_cache

    if not DATASET_PATH.exists():
        raise FileNotFoundError("dataset.json not found; expected at project root")

    try:
        with DATASET_PATH.open() as fp:
            data = json.load(fp)
    except json.JSONDecodeError as exc:
        raise RuntimeError("dataset.json contains invalid JSON") from exc

    if not isinstance(data, (list, dict)):
        raise RuntimeError("dataset.json has an unexpected structure – expected list[dict] or dict")

    _df_cache = pd.DataFrame(data)
    return _df_cache


def get_top_skills(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    from collections import Counter

    all_skills = [skill for sublist in df["skills"].dropna() for skill in sublist]
    skill_counts = Counter(all_skills)
    return pd.DataFrame(skill_counts.most_common(top_n), columns=["skill", "count"])


def get_seniority_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df["seniority"].value_counts().reset_index().rename(columns={"index": "seniority", "seniority": "count"})
    )


def get_experience_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df["experience_years"].value_counts().reset_index().rename(columns={"index": "experience", "experience_years": "count"})
    )


def get_employment_type_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return df["employment_type"].value_counts().reset_index().rename(columns={"index": "employment_type", "employment_type": "count"})


def get_skills_by_seniority(df: pd.DataFrame, seniority: str) -> pd.DataFrame:
    from collections import Counter

    filtered_df = df[df["seniority"] == seniority]
    all_skills = [skill for sublist in filtered_df["skills"].dropna() for skill in sublist]
    skill_counts = Counter(all_skills)
    return pd.DataFrame(skill_counts.most_common(10), columns=["skill", "count"])

###############################################################################
# FastAPI application                                                          
###############################################################################

app = FastAPI(title="NaukriAI API", version="1.0.0", description="Programmatic access to NaukriAI features.")

# Allow the frontend (or any origin during development) to hit the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###############################################################################
# Request/response models                                                      
###############################################################################


class SearchRequest(BaseModel):
    query: str


class AdvancedMatchRequest(BaseModel):
    required_skills: List[str]
    preferred_skills: List[str] = []
    seniority: Optional[str] = None
    experience_years: Optional[str] = None
    employment_type: Optional[str] = None
    top_n: int = 5


###############################################################################
# Dataset endpoints                                                            
###############################################################################


@app.get("/dataset/top-skills")
def api_top_skills(top_n: int = 10) -> List[Dict[str, Any]]:
    """Return the top-N most common skills."""
    df = load_data()
    return get_top_skills(df, top_n).to_dict(orient="records")


@app.get("/dataset/seniority-distribution")
def api_seniority_distribution() -> List[Dict[str, Any]]:
    df = load_data()
    return get_seniority_distribution(df).to_dict(orient="records")


@app.get("/dataset/experience-distribution")
def api_experience_distribution() -> List[Dict[str, Any]]:
    df = load_data()
    return get_experience_distribution(df).to_dict(orient="records")


@app.get("/dataset/employment-type-distribution")
def api_employment_type_distribution() -> List[Dict[str, Any]]:
    df = load_data()
    return get_employment_type_distribution(df).to_dict(orient="records")


@app.get("/dataset/skills-by-seniority/{seniority}")
def api_skills_by_seniority(seniority: str) -> List[Dict[str, Any]]:
    df = load_data()
    return get_skills_by_seniority(df, seniority).to_dict(orient="records")

###############################################################################
# AI-powered features                                                          
###############################################################################


@app.post("/search-candidates")
def api_search_candidates(req: SearchRequest):
    """Natural-language candidate search using the `AICandidateSearch` class."""
    try:
        searcher = AICandidateSearch()
        results = searcher.search_candidates(req.query)

        # Post-process: enrich minimal LLM results (name / reason only) with full dataset info
        if results:
            df = load_data()
            df_by_name = {row["name"]: row for _, row in df.iterrows()}
            enriched_results = []
            for item in results:
                if not isinstance(item, dict):
                    # skip malformed entry
                    continue
                base = dict(item)
                record = df_by_name.get(base.get("name"))
                if record is not None:
                    # Fill missing keys from dataset where not already present
                    for key in [
                        "skills",
                        "seniority",
                        "employment_type",
                        "experience_years",
                        "location",
                    ]:
                        if key not in base or base[key] in (None, "", []):
                            base[key] = record[key]
                enriched_results.append(base)
            results = enriched_results

        return {"results": results}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/advanced-match")
def api_advanced_match(req: AdvancedMatchRequest):
    """Return the best-matching candidates for a job requirement."""
    try:
        matcher = AdvancedCandidateMatcher()
        candidates: List[ScoredCandidate] = matcher.match_candidates(
            required_skills=req.required_skills,
            preferred_skills=req.preferred_skills,
            seniority=req.seniority,
            employment_type=req.employment_type,
            experience_years=req.experience_years,
            top_n=req.top_n,
        )
        # `ScoredCandidate` is a dataclass; convert to dicts for JSON serialisation.
        matches = [
            {
                **c.candidate,
                "score": c.score,
                "skill_matches": c.skill_matches,
                "missing_skills": c.missing_skills,
                "skill_gap_analysis": c.skill_gap_analysis,
                "interview_questions": c.interview_questions,
            }
            for c in candidates
        ]
        return {
            "matches": matches,
            "total": len(matches)
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/analyze-cv")
async def api_analyze_cv(file: UploadFile = File(...)):
    """Upload a CV (PDF, DOCX, TXT) and return a structured analysis."""
    suffix = Path(file.filename).suffix or ".cv"
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = Path(tmp.name)

        analyzer = CVAnalyzer()
        result = analyzer.analyze_cv(str(tmp_path))
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        try:
            tmp_path.unlink(missing_ok=True)  # Clean up temporary file
        except Exception:
            pass


@app.post("/compare-cvs")
async def api_compare_cvs(
    criteria: str = Form(...),
    cv1: UploadFile = File(...),
    cv2: UploadFile = File(...),
):
    """Upload two CVs and recruiter criteria; return structured comparison."""
    suffix1 = Path(cv1.filename).suffix or ".cv1"
    suffix2 = Path(cv2.filename).suffix or ".cv2"
    tmp1_path = tmp2_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix1) as tmp1:
            tmp1.write(await cv1.read())
            tmp1_path = Path(tmp1.name)
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix2) as tmp2:
            tmp2.write(await cv2.read())
            tmp2_path = Path(tmp2.name)

        comparator = CVComparator()
        result = comparator.compare(str(tmp1_path), str(tmp2_path), criteria)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        for p in (tmp1_path, tmp2_path):
            try:
                if p is not None:
                    p.unlink(missing_ok=True)
            except Exception:
                pass

###############################################################################
# Healthcheck                                                                  
###############################################################################


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}

###############################################################################
# Local dev helper                                                             
###############################################################################

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=8000, reload=True)
