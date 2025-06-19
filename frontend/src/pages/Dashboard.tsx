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
        <SkillsChart />
        <SeniorityChart />
        <ExperienceChart />
        <EmploymentChart />
      </div>
    </div>
  );
};