import React from 'react';

interface Props {
  title: string;
  summary: Record<string, any>;
}

function normaliseListField(value: unknown): string[] {
  if (!value) return [];
  if (Array.isArray(value)) return value.map(String);
  if (typeof value === 'string') {
    // Try JSON parse first incase it's a serialized array
    try {
      const parsed = JSON.parse(value);
      if (Array.isArray(parsed)) return parsed.map(String);
    } catch {
      /* ignored */
    }
    return value.split(/,\s*/).map((s) => s.replace(/^[-•\s]+/, '').trim());
  }
  return [String(value)];
}

export const CandidateSummary: React.FC<Props> = ({ title, summary }) => {
  const strengths = normaliseListField(summary.key_strengths || summary.strengths);
  const redFlags = normaliseListField(summary.red_flags || summary.weaknesses);

  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">{title}</h3>
      {strengths.length > 0 && (
        <div className="mb-3">
          <h4 className="font-medium text-gray-800 dark:text-gray-200 mb-1">Key Strengths</h4>
          <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 space-y-1">
            {strengths.map((s, idx) => (
              <li key={idx}>{s}</li>
            ))}
          </ul>
        </div>
      )}
      {redFlags.length > 0 && (
        <div>
          <h4 className="font-medium text-gray-800 dark:text-gray-200 mb-1">Red Flags</h4>
          <ul className="list-disc list-inside text-red-600 dark:text-red-400 space-y-1">
            {redFlags.map((s, idx) => (
              <li key={idx}>{s}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
