import React from 'react';
import { User, Mail, Phone, GraduationCap, Award, Briefcase, CheckCircle, AlertTriangle, HelpCircle } from 'lucide-react';
import { CVAnalysisResult } from '../../types/api';

interface AnalysisResultsProps {
  result: CVAnalysisResult;
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ result }) => {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center">
            <div className="h-16 w-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center">
              <User className="h-8 w-8 text-gray-600 dark:text-gray-300" />
            </div>
            <div className="ml-4">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                {result.name}
              </h2>
              <div className="flex items-center text-gray-600 dark:text-gray-400 mt-1">
                <Mail className="h-4 w-4 mr-2" />
                {result.email}
              </div>
              {result.phone && (
                <div className="flex items-center text-gray-600 dark:text-gray-400 mt-1">
                  <Phone className="h-4 w-4 mr-2" />
                  {result.phone}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center text-gray-600 dark:text-gray-400">
            <Briefcase className="h-4 w-4 mr-2" />
            <span className="text-sm">{result.seniority}</span>
          </div>
          <div className="flex items-center text-gray-600 dark:text-gray-400">
            <Briefcase className="h-4 w-4 mr-2" />
            <span className="text-sm">{result.experience_years} years experience</span>
          </div>
        </div>
      </div>

      {/* Summary */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
          Professional Summary
        </h3>
        <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
          {result.summary}
        </p>
      </div>

      {/* Skills */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
          Technical Skills
        </h3>
        <div className="flex flex-wrap gap-2">
          {result.skills.map((skill) => (
            <span
              key={skill}
              className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-sm font-medium"
            >
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* Strengths */}
      {result.strengths && result.strengths.length > 0 && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center mb-3">
            <CheckCircle className="h-5 w-5 text-green-600 dark:text-green-400 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Strengths
            </h3>
          </div>
          <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
            {result.strengths.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Red Flags */}
      {result.red_flags && result.red_flags.length > 0 && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center mb-3">
            <AlertTriangle className="h-5 w-5 text-red-600 dark:text-red-400 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Red Flags
            </h3>
          </div>
          <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
            {result.red_flags.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Verification Needed */}
      {result.verification_needed && result.verification_needed.length > 0 && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center mb-3">
            <HelpCircle className="h-5 w-5 text-yellow-600 dark:text-yellow-400 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Verification Needed
            </h3>
          </div>
          <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
            {result.verification_needed.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendation */}
      {result.recommended !== undefined && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
            Recommendation
          </h3>
          <p className="mb-2 text-gray-700 dark:text-gray-300">
            <span className="font-medium">Recommended:</span>{' '}
            {result.recommended ? 'Yes' : 'No'}
          </p>
          {result.recommendation_reasoning && (
            <p className="text-gray-700 dark:text-gray-300">
              {result.recommendation_reasoning}
            </p>
          )}
          {result.suggested_roles && result.suggested_roles.length > 0 && (
            <p className="mt-2 text-gray-700 dark:text-gray-300">
              <span className="font-medium">Suggested Roles:</span>{' '}
              {result.suggested_roles.join(', ')}
            </p>
          )}
          {result.suggested_compensation_range && (
            <p className="mt-2 text-gray-700 dark:text-gray-300">
              <span className="font-medium">Suggested Compensation:</span>{' '}
              {`${result.suggested_compensation_range.min} - ${result.suggested_compensation_range.max} ${result.suggested_compensation_range.currency}`}
            </p>
          )}
        </div>
      )}

      {/* Interview Questions */}
      {result.suggested_interview_questions && result.suggested_interview_questions.length > 0 && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
            Suggested Interview Questions
          </h3>
          <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
            {result.suggested_interview_questions.map((q, idx) => (
              <li key={idx}>{q}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Education */}
      {result.education.length > 0 && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center mb-3">
            <GraduationCap className="h-5 w-5 text-gray-600 dark:text-gray-300 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Education
            </h3>
          </div>
          <ul className="space-y-2">
            {result.education.map((edu, index) => (
              <li key={index} className="text-gray-600 dark:text-gray-400">
                {edu}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Certifications */}
      {result.certifications.length > 0 && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center mb-3">
            <Award className="h-5 w-5 text-gray-600 dark:text-gray-300 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Certifications
            </h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {result.certifications.map((cert) => (
              <span
                key={cert}
                className="px-3 py-1 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded-full text-sm font-medium border border-blue-200 dark:border-blue-800"
              >
                {cert}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};