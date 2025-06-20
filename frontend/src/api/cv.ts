import apiClient from './client';
import { CVAnalysisResult } from '../types/api';
import { mockCVAnalysis, simulateApiDelay } from '../utils/mockData';

export const cvApi = {
  analyzeCV: async (file: File): Promise<CVAnalysisResult> => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await apiClient.post('/analyze-cv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      // Log raw response to help debug CV analyzer API
      console.log('CV analyzer raw response:', response);
      console.log('CV analyzer response data:', response.data);
      
      // Handle string response from FastAPI
      let data = response.data;
      if (typeof data === 'string') {
        try {
          data = JSON.parse(data);
        } catch {
          // If parsing fails, return mock data with file info
          return {
            ...mockCVAnalysis,
            name: file.name.replace(/\.[^/.]+$/, "").replace(/[-_]/g, ' ') || mockCVAnalysis.name,
          };
        }
      }
      
      // Normalize backend response. FastAPI may wrap analysis under `analysis` key
      let analysisData: any = data;
      if (data && data.analysis) {
        analysisData = {
          ...data.analysis,
          // Flatten candidate_summary to top-level for easier mapping
          ...data.analysis.candidate_summary,
        };
      }

      // Extract and transform fields with sensible defaults
      const skills: string[] = Array.isArray(analysisData.key_skills)
        ? analysisData.key_skills
        : Array.isArray(analysisData.skills)
        ? analysisData.skills
        : [];

      // Determine recommendation info if present
      const recommendationData: any = (data && data.analysis && data.analysis.recommendation) || analysisData.recommendation || {};

      // Attempt to parse experience from textual representations like "5 years" or "Less than 1 year"
      let yearsExp = 0;
      if (typeof analysisData.years_experience === 'number') {
        yearsExp = analysisData.years_experience;
      } else if (typeof analysisData.years_experience === 'string') {
        const match = analysisData.years_experience.match(/(\d+)/);
        yearsExp = match ? parseInt(match[1], 10) : 0;
      } else if (typeof analysisData.experience_years === 'number') {
        yearsExp = analysisData.experience_years;
      }

      return {
        name: analysisData.name || 'Unknown',
        email: analysisData.email || '',
        phone: analysisData.phone,
        skills,
        experience_years: yearsExp,
        seniority: analysisData.current_role || analysisData.seniority || 'Unknown',
        summary: analysisData.overall_assessment || analysisData.summary || '',
        education: Array.isArray(analysisData.education) ? analysisData.education : [],
        certifications: Array.isArray(analysisData.certifications) ? analysisData.certifications : [],
        score: analysisData.score || 0,
        strengths: analysisData.strengths || [],
        red_flags: analysisData.red_flags || [],
        verification_needed: analysisData.verification_needed || [],
        recommended: recommendationData.recommended,
        recommendation_reasoning: recommendationData.reasoning,
        suggested_roles: recommendationData.suggested_roles || [],
        suggested_compensation_range: recommendationData.suggested_compensation_range,
        suggested_interview_questions: (data as any).suggested_interview_questions || [],
      };
    } catch (error: any) {
      if (error.isNetworkError) {
        console.warn('API unavailable, using mock data for CV analysis');
        await simulateApiDelay(2000);
        
        // Return mock analysis with file name incorporated
        return {
          ...mockCVAnalysis,
          name: file.name.replace(/\.[^/.]+$/, "").replace(/[-_]/g, ' ') || mockCVAnalysis.name,
        };
      }
      throw error;
    }
  },
};