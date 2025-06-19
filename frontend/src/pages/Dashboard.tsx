import React from 'react';
import { SkillsChart } from '../components/Dashboard/SkillsChart';
import { SeniorityChart } from '../components/Dashboard/SeniorityChart';
import { ExperienceChart } from '../components/Dashboard/ExperienceChart';
import { EmploymentChart } from '../components/Dashboard/EmploymentChart';

export const Dashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Dashboard
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Overview of candidate data and market insights
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Welcome to NaukriAI Dashboard
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Your AI-powered recruitment platform is ready. The charts below will populate with real data once connected to your API.
          </p>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Quick Stats
          </h3>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Total Candidates</span>
              <span className="font-semibold text-gray-900 dark:text-white">Loading...</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Active Searches</span>
              <span className="font-semibold text-gray-900 dark:text-white">0</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SkillsChart />
        <SeniorityChart />
        <ExperienceChart />
        <EmploymentChart />
      </div>
    </div>
  );
};