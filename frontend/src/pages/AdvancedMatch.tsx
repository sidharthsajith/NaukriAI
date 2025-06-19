import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { searchApi } from '../api/search';
import { MatchForm } from '../components/AdvancedMatch/MatchForm';
import { MatchResults } from '../components/AdvancedMatch/MatchResults';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { AdvancedMatchRequest, AdvancedMatchResponse } from '../types/api';

export const AdvancedMatch: React.FC = () => {
  const [matchResults, setMatchResults] = useState<AdvancedMatchResponse | null>(null);

  const matchMutation = useMutation({
    mutationFn: searchApi.advancedMatch,
    onSuccess: (data) => {
      setMatchResults(data);
    },
  });

  const handleMatch = (criteria: AdvancedMatchRequest) => {
    matchMutation.mutate(criteria);
  };

  const handleRetry = () => {
    if (matchResults?.criteria) {
      matchMutation.mutate(matchResults.criteria);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Advanced Matching
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Find candidates using detailed criteria and preferences
        </p>
      </div>

      <MatchForm onSubmit={handleMatch} isLoading={matchMutation.isPending} />

      {matchMutation.error && (
        <ErrorMessage 
          error={matchMutation.error} 
          onRetry={handleRetry} 
        />
      )}

      {matchResults && (
        <MatchResults 
          matches={matchResults.matches} 
          total={matchResults.total} 
        />
      )}
    </div>
  );
};