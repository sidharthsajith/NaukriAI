import { useQuery } from '@tanstack/react-query';
import { datasetApi } from '../api/dataset';

export const useTopSkills = (topN: number = 10) => {
  return useQuery({
    queryKey: ['topSkills', topN],
    queryFn: () => datasetApi.getTopSkills(topN),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: (failureCount, error: any) => {
      // Don't retry network errors, use mock data instead
      if (error?.isNetworkError) return false;
      return failureCount < 2;
    },
  });
};

export const useSeniorityDistribution = () => {
  return useQuery({
    queryKey: ['seniorityDistribution'],
    queryFn: () => datasetApi.getSeniorityDistribution(),
    staleTime: 5 * 60 * 1000,
    retry: (failureCount, error: any) => {
      if (error?.isNetworkError) return false;
      return failureCount < 2;
    },
  });
};

export const useExperienceDistribution = () => {
  return useQuery({
    queryKey: ['experienceDistribution'],
    queryFn: () => datasetApi.getExperienceDistribution(),
    staleTime: 5 * 60 * 1000,
    retry: (failureCount, error: any) => {
      if (error?.isNetworkError) return false;
      return failureCount < 2;
    },
  });
};

export const useEmploymentTypeDistribution = () => {
  return useQuery({
    queryKey: ['employmentTypeDistribution'],
    queryFn: () => datasetApi.getEmploymentTypeDistribution(),
    staleTime: 5 * 60 * 1000,
    retry: (failureCount, error: any) => {
      if (error?.isNetworkError) return false;
      return failureCount < 2;
    },
  });
};

export const useSkillsBySeniority = (seniority: string) => {
  return useQuery({
    queryKey: ['skillsBySeniority', seniority],
    queryFn: () => datasetApi.getSkillsBySeniority(seniority),
    enabled: !!seniority,
    staleTime: 5 * 60 * 1000,
    retry: (failureCount, error: any) => {
      if (error?.isNetworkError) return false;
      return failureCount < 2;
    },
  });
};