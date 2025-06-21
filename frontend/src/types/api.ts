export interface Skill {
  name: string;
  count: number;
  percentage?: number;
}

export interface SeniorityDistribution {
  seniority: string;
  count: number;
  percentage: number;
}

export interface ExperienceDistribution {
  experience_range: string;
  count: number;
  percentage: number;
}

export interface EmploymentTypeDistribution {
  employment_type: string;
  count: number;
  percentage: number;
}

export interface Candidate {
  id: string;
  name: string;
  email: string;
  skills: string[];
  experience_years: number;
  seniority: string;
  employment_type: string;
  score?: number;
  summary?: string;
}

// FastAPI request/response types based on documentation
export interface SearchRequest {
  query: string;
}

export interface SearchResponse {
  candidates: Candidate[];
  total: number;
  query: string;
}

export interface AdvancedMatchRequest {
  required_skills: string[];
  preferred_skills: string[];
  seniority: string;
  experience_years: string; // FastAPI docs show this as string
  employment_type: string;
  top_n: number;
}

export interface AdvancedMatchResponse {
  matches: Candidate[];
  total: number;
  criteria: AdvancedMatchRequest;
}

export interface CVAnalysisResult {
  // Basic candidate info
  name: string;
  email: string;
  phone?: string;
  skills: string[];
  experience_years: number;
  seniority: string;
  summary: string;
  education: string[];
  certifications: string[];
  score: number;
  // Additional analysis fields
  strengths?: string[];
  red_flags?: string[];
  verification_needed?: string[];
  recommended?: boolean;
  recommendation_reasoning?: string;
  suggested_roles?: string[];
  suggested_compensation_range?: {
    min: number;
    max: number;
    currency: string;
  };
  suggested_interview_questions?: string[];
}

// FastAPI validation error structure
export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export interface FastAPIError {
  detail: ValidationError[];
}

export interface ApiError {
  message: string;
  status?: number;
  isNetworkError?: boolean;
}

// Health check response
// Outreach email generation
export interface OutreachEmailRequest {
  candidate_name: string;
  recruiter_name: string;
  company_name: string;
  job_title: string;
  work_location: string;
  key_requirements: string;
}

export interface OutreachEmailResponse {
  email: string;
}

export interface HealthResponse {
  [key: string]: string;
}