import React from 'react';
import { User, Mail, Briefcase, Clock } from 'lucide-react';
import { Candidate } from '../../types/api';

interface ResultCardProps {
  candidate: Candidate;
}

export const ResultCard: React.FC<ResultCardProps> = ({ candidate }) => {
  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center">
          <div className="h-12 w-12 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center">
            <User className="h-6 w-6 text-gray-600 dark:text-gray-300" />
          </div>
          <div className="ml-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {candidate.name}
            </h3>
            <div className="flex items-center text-gray-600 dark:text-gray-400 text-sm">
              <Mail className="h-4 w-4 mr-1" />
              {candidate.email}
            </div>
          </div>
        </div>
        {candidate.score && (
          <div className="text-right">
            <div className="text-sm text-gray-500 dark:text-gray-400">Match Score</div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              {Math.round(candidate.score * 100)}%
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="flex items-center text-gray-600 dark:text-gray-400">
          <Briefcase className="h-4 w-4 mr-2" />
          <span className="text-sm">{candidate.seniority}</span>
        </div>
        <div className="flex items-center text-gray-600 dark:text-gray-400">
          <Clock className="h-4 w-4 mr-2" />
          <span className="text-sm">{candidate.experience_years} years exp.</span>
        </div>
      </div>

      <div className="mb-4">
        <div className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Skills
        </div>
        <div className="flex flex-wrap gap-2">
          {candidate.skills.slice(0, 6).map((skill) => (
            <span
              key={skill}
              className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 text-xs rounded-md"
            >
              {skill}
            </span>
          ))}
          {candidate.skills.length > 6 && (
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 text-xs rounded-md">
              +{candidate.skills.length - 6} more
            </span>
          )}
        </div>
      </div>

      {candidate.summary && (
        <div>
          <div className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Summary
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3">
            {candidate.summary}
          </p>
        </div>
      )}
    </div>
  );
};