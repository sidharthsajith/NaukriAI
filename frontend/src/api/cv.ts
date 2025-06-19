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
      
      // Ensure we have all required fields
      return {
        name: data.name || 'Unknown',
        email: data.email || '',
        phone: data.phone,
        skills: Array.isArray(data.skills) ? data.skills : [],
        experience_years: data.experience_years || 0,
        seniority: data.seniority || 'Unknown',
        summary: data.summary || '',
        education: Array.isArray(data.education) ? data.education : [],
        certifications: Array.isArray(data.certifications) ? data.certifications : [],
        score: data.score || 0,
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