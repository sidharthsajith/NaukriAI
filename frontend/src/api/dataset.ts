// NOTE: The dashboard now reads data directly from the local dataset.json file that sits in the Vite `public` folder (or project root during dev).
// No network requests are made – everything is computed client-side.
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
import {
  Skill,
  SeniorityDistribution,
  ExperienceDistribution,
  EmploymentTypeDistribution,
} from '../types/api';


/**
 * Cache the parsed JSON so we only fetch once per session.
 */
let _cache: any[] | null = null;

const DATASET_URL = '/dataset.json'; // served statically by Vite from the project root / public folder

async function loadDataset(): Promise<any[]> {
  if (_cache) return _cache;
  const res = await fetch(DATASET_URL);
  if (!res.ok) throw new Error(`Failed to load dataset.json – HTTP ${res.status}`);
  const json = await res.json();
  if (!Array.isArray(json)) throw new Error('dataset.json must be an array of records');
  _cache = json;
  return json;
}

function percentage(part: number, whole: number): number {
  return whole === 0 ? 0 : Number(((part / whole) * 100).toFixed(1));
}

export const datasetApi = {
  /** Return the top-N skills (name/count/percentage). */
  getTopSkills: async (topN: number = 10): Promise<Skill[]> => {
    const data = await loadDataset();
    const counter: Record<string, number> = {};
    data.forEach((rec) => {
      (rec.skills ?? []).forEach((skill: string) => {
        counter[skill] = (counter[skill] ?? 0) + 1;
      });
    });
    const total = Object.values(counter).reduce((acc, c) => acc + c, 0);
    return (
      Object.entries(counter)
        .sort((a, b) => b[1] - a[1])
        .slice(0, topN)
        .map(([name, count]) => ({ name, count, percentage: percentage(count, total) }))
    );
  }

  getSeniorityDistribution: async (): Promise<SeniorityDistribution[]> => {
    const data = await loadDataset();
    const counter: Record<string, number> = {};
    data.forEach((rec) => {
      const s = rec.seniority ?? 'Unknown';
      counter[s] = (counter[s] ?? 0) + 1;
    });
    const total = Object.values(counter).reduce((acc, c) => acc + c, 0);
    return Object.entries(counter).map(([seniority, count]) => ({
      seniority,
      count,
      percentage: percentage(count, total),
    }));
  }
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
    const data = await loadDataset();
    const counter: Record<string, number> = {};
    data.forEach((rec) => {
      const range = rec.experience_years ?? 'Unknown';
      counter[range] = (counter[range] ?? 0) + 1;
    });
    const total = Object.values(counter).reduce((acc, c) => acc + c, 0);
    return Object.entries(counter).map(([experience_range, count]) => ({
      experience_range,
      count,
      percentage: percentage(count, total),
    }));
  }
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
    const data = await loadDataset();
    const counter: Record<string, number> = {};
    data.forEach((rec) => {
      const typ = rec.employment_type ?? 'Unknown';
      counter[typ] = (counter[typ] ?? 0) + 1;
    });
    const total = Object.values(counter).reduce((acc, c) => acc + c, 0);
    return Object.entries(counter).map(([employment_type, count]) => ({
      employment_type,
      count,
      percentage: percentage(count, total),
    }));
  }
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
    const data = await loadDataset();
    const counter: Record<string, number> = {};
    data.filter((rec) => rec.seniority === seniority).forEach((rec) => {
      (rec.skills ?? []).forEach((skill: string) => {
        counter[skill] = (counter[skill] ?? 0) + 1;
      });
    });
    const total = Object.values(counter).reduce((acc, c) => acc + c, 0);
    return Object.entries(counter)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([name, count]) => ({ name, count, percentage: percentage(count, total) }));
  },
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