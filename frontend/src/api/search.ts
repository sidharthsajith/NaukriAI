import apiClient from './client';
import { SearchRequest, SearchResponse, AdvancedMatchRequest, AdvancedMatchResponse, Candidate } from '../types/api';
import { mockCandidates, simulateApiDelay } from '../utils/mockData';

export const searchApi = {
  searchCandidates: async (query: string): Promise<SearchResponse> => {
    try {
      const requestData: SearchRequest = { query };
      const response = await apiClient.post('/search-candidates', requestData);
      // Log raw response to help debug issues in search API
      console.log('searchCandidates raw response:', response);
      
      // FastAPI docs show response as string, but we expect structured data
      // Handle both cases
      let data = response.data;
      if (typeof data === 'string') {
        try {
          data = JSON.parse(data);
        } catch {
          // If it's just a string response, create a structured response
          return {
            candidates: [],
            total: 0,
            query,
          };
        }
      }
      
      // If backend returns `results`, map them to our Candidate structure
      if (!data.candidates && Array.isArray((data as any).results)) {
        const resultsArray = (data as any).results;
        data = {
          candidates: resultsArray.map((item: any) => ({
            id: Math.random().toString(36),
            name: item.name || 'Unknown',
            email: item.email || '',
            skills: Array.isArray(item.skills) ? item.skills : [],
            experience_years: typeof item.experience_years === 'string' ? parseInt(item.experience_years.replace('+', '')) || 0 : (item.experience_years || 0),
            seniority: item.seniority || 'Unknown',
            employment_type: item.employment_type || 'Unknown',
            score: item.score,
            summary: item.reason || item.summary || '',
          })),
          total: resultsArray.length,
        };
      }

      // Ensure we have the expected structure
      return {
        candidates: Array.isArray(data.candidates) ? data.candidates.map((candidate: any) => ({
          id: candidate.id || Math.random().toString(36),
          name: candidate.name || 'Unknown',
          email: candidate.email || '',
          skills: Array.isArray(candidate.skills) ? candidate.skills : [],
          experience_years: candidate.experience_years || 0,
          seniority: candidate.seniority || 'Unknown',
          employment_type: candidate.employment_type || 'Unknown',
          score: candidate.score,
          summary: candidate.summary
        })) : [],
        total: data.total || 0,
        query,
      };
    } catch (error: any) {
      if (error.isNetworkError) {
        console.warn('API unavailable, using mock data for candidate search');
        await simulateApiDelay(1000);
        
        // Simple mock search logic
        const filteredCandidates = mockCandidates.filter(candidate => 
          candidate.skills.some(skill => 
            skill.toLowerCase().includes(query.toLowerCase())
          ) ||
          candidate.name.toLowerCase().includes(query.toLowerCase()) ||
          candidate.seniority.toLowerCase().includes(query.toLowerCase())
        );

        return {
          candidates: filteredCandidates,
          total: filteredCandidates.length,
          query,
        };
      }
      throw error;
    }
  },

  advancedMatch: async (criteria: AdvancedMatchRequest): Promise<AdvancedMatchResponse> => {
    try {
      // Ensure experience_years is sent as string per FastAPI docs
      const requestData = {
        ...criteria,
        experience_years: criteria.experience_years.toString(),
        preferred_skills: criteria.preferred_skills || [], // Ensure array
      };
      
      const response = await apiClient.post('/advanced-match', requestData);
      
      // Handle string response from FastAPI
      let data = response.data;
      if (typeof data === 'string') {
        try {
          data = JSON.parse(data);
        } catch {
          return {
            matches: [],
            total: 0,
            criteria,
          };
        }
      }
      
      return {
        matches: Array.isArray(data.matches) ? data.matches.map((candidate: any) => ({
          id: candidate.id || Math.random().toString(36),
          name: candidate.name || 'Unknown',
          email: candidate.email || '',
          skills: Array.isArray(candidate.skills) ? candidate.skills : [],
          experience_years: candidate.experience_years || 0,
          seniority: candidate.seniority || 'Unknown',
          employment_type: candidate.employment_type || 'Unknown',
          score: candidate.score,
          summary: candidate.summary
        })) : [],
        total: data.total || 0,
        criteria,
      };
    } catch (error: any) {
      if (error.isNetworkError) {
        console.warn('API unavailable, using mock data for advanced matching');
        await simulateApiDelay(1500);
        
        // Simple mock matching logic
        let filteredCandidates = mockCandidates;

        // Filter by required skills
        if (criteria.required_skills.length > 0) {
          filteredCandidates = filteredCandidates.filter(candidate =>
            criteria.required_skills.some(skill =>
              candidate.skills.some(candidateSkill =>
                candidateSkill.toLowerCase().includes(skill.toLowerCase())
              )
            )
          );
        }

        // Filter by seniority
        if (criteria.seniority) {
          filteredCandidates = filteredCandidates.filter(candidate =>
            candidate.seniority.toLowerCase() === criteria.seniority.toLowerCase()
          );
        }

        // Filter by experience (convert string to number for comparison)
        const experienceYears = parseInt(criteria.experience_years) || 0;
        if (experienceYears > 0) {
          filteredCandidates = filteredCandidates.filter(candidate =>
            candidate.experience_years >= experienceYears
          );
        }

        // Limit results
        const limitedResults = filteredCandidates.slice(0, criteria.top_n);

        return {
          matches: limitedResults,
          total: limitedResults.length,
          criteria,
        };
      }
      throw error;
    }
  },
};