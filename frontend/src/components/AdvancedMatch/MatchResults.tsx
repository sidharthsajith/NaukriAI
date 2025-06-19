import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Star } from 'lucide-react';
import { Candidate } from '../../types/api';
import { ResultCard } from '../AISearch/ResultCard';

interface MatchResultsProps {
  matches: Candidate[];
  total: number;
}

export const MatchResults: React.FC<MatchResultsProps> = ({ matches, total }) => {
  const [expandedCount, setExpandedCount] = useState(5);
  const [showAll, setShowAll] = useState(false);

  const displayedMatches = showAll ? matches : matches.slice(0, expandedCount);

  const toggleExpansion = () => {
    if (showAll) {
      setShowAll(false);
      setExpandedCount(5);
    } else {
      setShowAll(true);
    }
  };

  if (matches.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 p-8 rounded-lg border border-gray-200 dark:border-gray-700 text-center">
        <Star className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
          No Matches Found
        </h3>
        <p className="text-gray-500 dark:text-gray-400">
          Try adjusting your search criteria to find more candidates.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Matching Results
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Found {total} candidates matching your criteria
            </p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              {total}
            </div>
            <div className="text-sm text-gray-500 dark:text-gray-400">
              Total Matches
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {displayedMatches.map((candidate, index) => (
          <div key={candidate.id} className="animate-slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
            <ResultCard candidate={candidate} />
          </div>
        ))}
      </div>

      {matches.length > 5 && (
        <div className="text-center">
          <button
            onClick={toggleExpansion}
            className="inline-flex items-center px-6 py-3 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            {showAll ? (
              <>
                <ChevronUp className="h-5 w-5 mr-2" />
                Show Less
              </>
            ) : (
              <>
                <ChevronDown className="h-5 w-5 mr-2" />
                Show All {matches.length} Results
              </>
            )}
          </button>
        </div>
      )}
    </div>
  );
};