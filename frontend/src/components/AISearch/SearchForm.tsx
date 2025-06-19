import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

interface SearchFormProps {
  onSearch: (query: string) => void;
  isLoading: boolean;
}

export const SearchForm: React.FC<SearchFormProps> = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        AI-Powered Candidate Search
      </h2>
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        Use natural language to describe the candidate you're looking for. 
        Our AI will understand your requirements and find matching profiles.
      </p>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="search-query" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Search Query
          </label>
          <textarea
            id="search-query"
            rows={4}
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
            placeholder="e.g., Find senior React developers with 5+ years experience in fintech, skilled in TypeScript and GraphQL"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
          />
        </div>
        
        <button
          type="submit"
          disabled={!query.trim() || isLoading}
          className="w-full flex items-center justify-center px-6 py-3 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg hover:bg-gray-800 dark:hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <Loader2 className="h-5 w-5 animate-spin mr-2" />
          ) : (
            <Search className="h-5 w-5 mr-2" />
          )}
          {isLoading ? 'Searching...' : 'Search Candidates'}
        </button>
      </form>
    </div>
  );
};