import React, { useState } from 'react';
import { Target, Plus, X } from 'lucide-react';
import { AdvancedMatchRequest } from '../../types/api';

interface MatchFormProps {
  onSubmit: (criteria: AdvancedMatchRequest) => void;
  isLoading: boolean;
}

export const MatchForm: React.FC<MatchFormProps> = ({ onSubmit, isLoading }) => {
  const [requiredSkills, setRequiredSkills] = useState<string[]>(['']);
  const [preferredSkills, setPreferredSkills] = useState<string[]>(['']);
  const [seniority, setSeniority] = useState('');
  const [experienceYears, setExperienceYears] = useState('0'); // Changed to string to match API
  const [employmentType, setEmploymentType] = useState('');
  const [topN, setTopN] = useState(10);

  const addSkillField = (type: 'required' | 'preferred') => {
    if (type === 'required') {
      setRequiredSkills([...requiredSkills, '']);
    } else {
      setPreferredSkills([...preferredSkills, '']);
    }
  };

  const removeSkillField = (type: 'required' | 'preferred', index: number) => {
    if (type === 'required') {
      setRequiredSkills(requiredSkills.filter((_, i) => i !== index));
    } else {
      setPreferredSkills(preferredSkills.filter((_, i) => i !== index));
    }
  };

  const updateSkill = (type: 'required' | 'preferred', index: number, value: string) => {
    if (type === 'required') {
      const updated = [...requiredSkills];
      updated[index] = value;
      setRequiredSkills(updated);
    } else {
      const updated = [...preferredSkills];
      updated[index] = value;
      setPreferredSkills(updated);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const criteria: AdvancedMatchRequest = {
      required_skills: requiredSkills.filter(skill => skill.trim()),
      preferred_skills: preferredSkills.filter(skill => skill.trim()),
      seniority,
      experience_years: experienceYears, // Keep as string per API spec
      employment_type: employmentType,
      top_n: topN,
    };

    onSubmit(criteria);
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
      <div className="flex items-center mb-6">
        <Target className="h-6 w-6 text-gray-900 dark:text-white mr-3" />
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          Advanced Candidate Matching
        </h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Required Skills */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Required Skills *
          </label>
          {requiredSkills.map((skill, index) => (
            <div key={index} className="flex items-center mb-2">
              <input
                type="text"
                value={skill}
                onChange={(e) => updateSkill('required', index, e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                placeholder="e.g., React, JavaScript, Node.js"
              />
              {requiredSkills.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeSkillField('required', index)}
                  className="ml-2 p-2 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md"
                >
                  <X className="h-4 w-4" />
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={() => addSkillField('required')}
            className="flex items-center text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
          >
            <Plus className="h-4 w-4 mr-1" />
            Add Required Skill
          </button>
        </div>

        {/* Preferred Skills */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Preferred Skills
          </label>
          {preferredSkills.map((skill, index) => (
            <div key={index} className="flex items-center mb-2">
              <input
                type="text"
                value={skill}
                onChange={(e) => updateSkill('preferred', index, e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                placeholder="e.g., GraphQL, AWS, Docker"
              />
              <button
                type="button"
                onClick={() => removeSkillField('preferred', index)}
                className="ml-2 p-2 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          ))}
          <button
            type="button"
            onClick={() => addSkillField('preferred')}
            className="flex items-center text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
          >
            <Plus className="h-4 w-4 mr-1" />
            Add Preferred Skill
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Seniority */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Seniority Level
            </label>
            <select
              value={seniority}
              onChange={(e) => setSeniority(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option value="">Any Level</option>
              <option value="Junior">Junior</option>
              <option value="Mid-level">Mid-level</option>
              <option value="Senior">Senior</option>
              <option value="Lead">Lead</option>
              <option value="Principal">Principal</option>
            </select>
          </div>

          {/* Experience Years */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Minimum Experience (Years)
            </label>
            <input
              type="text"
              value={experienceYears}
              onChange={(e) => setExperienceYears(e.target.value)}
              placeholder="e.g., 5"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
          </div>

          {/* Employment Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Employment Type
            </label>
            <select
              value={employmentType}
              onChange={(e) => setEmploymentType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option value="">Any Type</option>
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Contract">Contract</option>
              <option value="Freelance">Freelance</option>
            </select>
          </div>

          {/* Top N Results */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Number of Results
            </label>
            <input
              type="number"
              value={topN}
              onChange={(e) => setTopN(Number(e.target.value))}
              min="1"
              max="100"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading || requiredSkills.filter(s => s.trim()).length === 0}
          className="w-full flex items-center justify-center px-6 py-3 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg hover:bg-gray-800 dark:hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Target className="h-5 w-5 mr-2" />
          {isLoading ? 'Finding Matches...' : 'Find Matching Candidates'}
        </button>
      </form>
    </div>
  );
};