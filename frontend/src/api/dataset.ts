import apiClient from './client';
import {
  Skill,
  SeniorityDistribution,
  ExperienceDistribution,
  EmploymentTypeDistribution,
} from '../types/api';
import {
  mockSkills,
  mockSeniorityDistribution,
  mockExperienceDistribution,
  mockEmploymentTypeDistribution,
  simulateApiDelay,
} from '../utils/mockData';

export const datasetApi = {
  getTopSkills: async (topN: number = 10): Promise<Skill[]> => {
    try {
      const response = await apiClient.get(`/dataset/top-skills`, {
        params: { top_n: topN }
      });
      
      // FastAPI returns array of objects, need to transform to our Skill interface
      const data = response.data;
      if (Array.isArray(data)) {
        return data.map((item: any) => ({
          name: item.skill || item.name || 'Unknown',
          count: item.count || 0,
          percentage: item.percentage
        }));
      }
      return data;
    } catch (error: any) {
      // If network error, return mock data
      if (error.isNetworkError) {
        console.warn('API unavailable, using mock data for top skills');
        await simulateApiDelay(500);
        return mockSkills.slice(0, topN);
      }
      throw error;
    }
  },

  getSeniorityDistribution: async (): Promise<SeniorityDistribution[]> => {
    try {
      const response = await apiClient.get('/dataset/seniority-distribution');
      const data = response.data;
      
      if (Array.isArray(data)) {
        return data.map((item: any) => ({
          seniority: item.seniority || item.level || 'Unknown',
          count: item.count || 0,
          percentage: item.percentage || 0
        }));
      }
      return data;
    } catch (error: any) {
      if (error.isNetworkError) {
        console.warn('API unavailable, using mock data for seniority distribution');
        await simulateApiDelay(500);
        return mockSeniorityDistribution;
      }
      throw error;
    }
  },

  getExperienceDistribution: async (): Promise<ExperienceDistribution[]> => {
    try {
      const response = await apiClient.get('/dataset/experience-distribution');
      const data = response.data;
      
      if (Array.isArray(data)) {
        return data.map((item: any) => ({
          experience_range: item.experience_range || item.range || 'Unknown',
          count: item.count || 0,
          percentage: item.percentage || 0
        }));
      }
      return data;
    } catch (error: any) {
      if (error.isNetworkError) {
        console.warn('API unavailable, using mock data for experience distribution');
        await simulateApiDelay(500);
        return mockExperienceDistribution;
      }
      throw error;
    }
  },

  getEmploymentTypeDistribution: async (): Promise<EmploymentTypeDistribution[]> => {
    try {
      const response = await apiClient.get('/dataset/employment-type-distribution');
      const data = response.data;
      
      if (Array.isArray(data)) {
        return data.map((item: any) => ({
          employment_type: item.employment_type || item.type || 'Unknown',
          count: item.count || 0,
          percentage: item.percentage || 0
        }));
      }
      return data;
    } catch (error: any) {
      if (error.isNetworkError) {
        console.warn('API unavailable, using mock data for employment type distribution');
        await simulateApiDelay(500);
        return mockEmploymentTypeDistribution;
      }
      throw error;
    }
  },

  getSkillsBySeniority: async (seniority: string): Promise<Skill[]> => {
    try {
      const response = await apiClient.get(`/dataset/skills-by-seniority/${encodeURIComponent(seniority)}`);
      const data = response.data;
      
      if (Array.isArray(data)) {
        return data.map((item: any) => ({
          name: item.skill || item.name || 'Unknown',
          count: item.count || 0,
          percentage: item.percentage
        }));
      }
      return data;
    } catch (error: any) {
      if (error.isNetworkError) {
        console.warn('API unavailable, using mock data for skills by seniority');
        await simulateApiDelay(500);
        // Return filtered mock skills based on seniority
        return mockSkills.slice(0, 5);
      }
      throw error;
    }
  },
};