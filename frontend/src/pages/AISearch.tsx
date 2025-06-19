import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { searchApi } from '../api/search';
import { SearchForm } from '../components/AISearch/SearchForm';
import { ResultCard } from '../components/AISearch/ResultCard';
import { EmptyState } from '../components/common/EmptyState';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { SearchResponse } from '../types/api';
import { Search } from 'lucide-react';

export const AISearch: React.FC = () => {
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);

  const searchMutation = useMutation({
    mutationFn: searchApi.searchCandidates,
    onSuccess: (data) => {
      setSearchResults(data);
    },
  });

  const handleSearch = (query: string) => {
    searchMutation.mutate(query);
  };

  const handleRetry = () => {
    if (searchResults?.query) {
      searchMutation.mutate(searchResults.query);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          AI-Powered Search
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Find candidates using natural language queries
        </p>
      </div>

      <SearchForm onSearch={handleSearch} isLoading={searchMutation.isPending} />

      {searchMutation.error && (
        <ErrorMessage 
          error={searchMutation.error} 
          onRetry={handleRetry} 
        />
      )}

      {searchResults && (
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-medium text-gray-900 dark:text-white">
                  Search Results
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Query: "{searchResults.query}"
                </p>
              </div>
              <div className="text-sm text-gray-500 dark:text-gray-400">
                {searchResults.total} candidates found
              </div>
            </div>
          </div>

          {searchResults.candidates.length === 0 ? (
            <EmptyState
              title="No candidates found"
              description="Try refining your search query or using different keywords."
              icon={<Search className="h-12 w-12 text-gray-400 mb-4" />}
            />
          ) : (
            <div className="grid gap-4">
              {searchResults.candidates.map((candidate) => (
                <ResultCard key={candidate.id} candidate={candidate} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};