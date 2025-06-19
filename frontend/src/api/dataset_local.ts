// Reads the local `dataset.json` file (placed in the Vite `public` folder or project root) and computes
// statistics entirely client-side for the dashboard charts.
import {
  Skill,
  SeniorityDistribution,
  ExperienceDistribution,
  EmploymentTypeDistribution,
} from '../types/api';

let cache: any[] | null = null;
const DATASET_URL = '/dataset.json';

async function loadDataset(): Promise<any[]> {
  if (cache) return cache;
  const res = await fetch(DATASET_URL);
  if (!res.ok) throw new Error(`Failed to fetch dataset.json (status ${res.status})`);
  const json = await res.json();
  if (!Array.isArray(json)) throw new Error('dataset.json should be an array of records');
  cache = json;
  return json;
}

function pct(part: number, whole: number): number {
  return whole === 0 ? 0 : Number(((part / whole) * 100).toFixed(1));
}

export const datasetApi = {
  async getTopSkills(topN = 10): Promise<Skill[]> {
    const data = await loadDataset();
    const counts: Record<string, number> = {};
    data.forEach(rec => {
      (rec.skills ?? []).forEach((s: string) => {
        counts[s] = (counts[s] ?? 0) + 1;
      });
    });
    const total = Object.values(counts).reduce((a, b) => a + b, 0);
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, topN)
      .map(([name, count]) => ({ name, count, percentage: pct(count, total) }));
  },

  async getSeniorityDistribution(): Promise<SeniorityDistribution[]> {
    const data = await loadDataset();
    const counts: Record<string, number> = {};
    data.forEach(rec => {
      const key = rec.seniority ?? 'Unknown';
      counts[key] = (counts[key] ?? 0) + 1;
    });
    const total = Object.values(counts).reduce((a, b) => a + b, 0);
    return Object.entries(counts).map(([seniority, count]) => ({
      seniority,
      count,
      percentage: pct(count, total),
    }));
  },

  async getExperienceDistribution(): Promise<ExperienceDistribution[]> {
    const data = await loadDataset();
    const counts: Record<string, number> = {};
    data.forEach(rec => {
      const key = rec.experience_years ?? 'Unknown';
      counts[key] = (counts[key] ?? 0) + 1;
    });
    const total = Object.values(counts).reduce((a, b) => a + b, 0);
    return Object.entries(counts).map(([experience_range, count]) => ({
      experience_range,
      count,
      percentage: pct(count, total),
    }));
  },

  async getEmploymentTypeDistribution(): Promise<EmploymentTypeDistribution[]> {
    const data = await loadDataset();
    const counts: Record<string, number> = {};
    data.forEach(rec => {
      const key = rec.employment_type ?? 'Unknown';
      counts[key] = (counts[key] ?? 0) + 1;
    });
    const total = Object.values(counts).reduce((a, b) => a + b, 0);
    return Object.entries(counts).map(([employment_type, count]) => ({
      employment_type,
      count,
      percentage: pct(count, total),
    }));
  },

  async getSkillsBySeniority(seniority: string): Promise<Skill[]> {
    const data = await loadDataset();
    const counts: Record<string, number> = {};
    data.filter(rec => rec.seniority === seniority).forEach(rec => {
      (rec.skills ?? []).forEach((s: string) => {
        counts[s] = (counts[s] ?? 0) + 1;
      });
    });
    const total = Object.values(counts).reduce((a, b) => a + b, 0);
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([name, count]) => ({ name, count, percentage: pct(count, total) }));
  },
};
