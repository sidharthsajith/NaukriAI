import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { cvApi } from '../api/cv';
import { FileUploader } from '../components/CVAnalyzer/FileUploader';
import { FileDiff } from 'lucide-react';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { CandidateSummary } from '../components/CVComparator/CandidateSummary';

interface ComparisonResult {
  best_candidate: number; // 1 or 2
  reasoning: string;
  candidate_1_summary?: Record<string, any>;
  candidate_2_summary?: Record<string, any>;
}

export const CVComparator: React.FC = () => {
  const [cv1, setCv1] = useState<File | null>(null);
  const [cv2, setCv2] = useState<File | null>(null);
  const [criteria, setCriteria] = useState('');
  const [result, setResult] = useState<ComparisonResult | null>(null);

  const compareMutation = useMutation({
    mutationFn: ({ cv1, cv2, criteria }: { cv1: File; cv2: File; criteria: string }) =>
      cvApi.compareCVs(cv1, cv2, criteria),
    onSuccess: (data) => setResult(data as ComparisonResult),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!cv1 || !cv2 || !criteria.trim()) return;
    setResult(null);
    compareMutation.mutate({ cv1, cv2, criteria });
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">CV Comparator</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Upload two CVs and specify your ideal candidate criteria. Our AI will recommend the better fit.
        </p>
      </div>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
        <div className="flex items-center mb-6">
          <FileDiff className="h-6 w-6 text-gray-900 dark:text-white mr-3" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Compare Two CVs</h2>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Recruiter Criteria</label>
          <textarea
            className="w-full p-3 rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            rows={3}
            value={criteria}
            onChange={(e) => setCriteria(e.target.value)}
            placeholder="E.g. Senior React engineer with 5+ years experience and leadership skills"
            required
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FileUploader
              onFileSelect={(file) => setCv1(file)}
              selectedFile={cv1}
              onClearFile={() => setCv1(null)}
              isLoading={compareMutation.isPending}
            />
          <FileUploader
              onFileSelect={(file) => setCv2(file)}
              selectedFile={cv2}
              onClearFile={() => setCv2(null)}
              isLoading={compareMutation.isPending}
            />
        </div>
        <button
          type="submit"
          disabled={compareMutation.isPending}
          className="w-full flex items-center justify-center px-6 py-3 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg hover:bg-gray-800 dark:hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Compare CVs
        </button>
      </form>
      </div>

      {compareMutation.isPending && (
        <div className="bg-white dark:bg-gray-800 p-8 rounded-lg border border-gray-200 dark:border-gray-700 flex flex-col items-center">
          <LoadingSpinner size="lg" className="mb-4" />
          <p className="text-gray-600 dark:text-gray-400">Comparing candidates...</p>
        </div>
      )}

      {compareMutation.error && (
        <ErrorMessage error={compareMutation.error as any} onRetry={() => {
          if (cv1 && cv2 && criteria) compareMutation.mutate({ cv1, cv2, criteria });
        }} />
      )}

      {result && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700 space-y-6">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">Recommendation</h2>
          <p className="text-gray-600 dark:text-gray-400">
            Best Candidate: <span className="font-medium">Candidate {result.best_candidate}</span>
          </p>
          <p className="text-gray-600 dark:text-gray-400 whitespace-pre-wrap">{result.reasoning}</p>

          {result.candidate_1_summary && (
            <CandidateSummary title="Candidate 1 Summary" summary={result.candidate_1_summary} />
          )}
          {result.candidate_2_summary && (
            <CandidateSummary title="Candidate 2 Summary" summary={result.candidate_2_summary} />
          )}
        </div>
      )}
    </div>
  );
};
