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
export interface HealthResponse {
  [key: string]: string;
}