import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Copy, Check } from 'lucide-react';
import { emailApi } from '../api/email';
import { OutreachEmailRequest } from '../types/api';


export const OutreachEmail: React.FC = () => {
  const [form, setForm] = useState<OutreachEmailRequest>({
    candidate_name: '',
    recruiter_name: '',
    company_name: '',
    job_title: '',
    work_location: '',
    key_requirements: '',
  });

  const emailMutation = useMutation({
    mutationFn: emailApi.generateEmail,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const [copied, setCopied] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    emailMutation.mutate(form);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Outreach Email Generator</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">Compose personalised candidate outreach emails quickly.</p>
      </div>
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Generate Email</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="text"
            name="candidate_name"
            placeholder="Candidate Name"
            value={form.candidate_name}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
          <input
            type="text"
            name="recruiter_name"
            placeholder="Your Name"
            value={form.recruiter_name}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
          <input
            type="text"
            name="company_name"
            placeholder="Company Name"
            value={form.company_name}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
          <input
            type="text"
            name="job_title"
            placeholder="Job Title"
            value={form.job_title}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
          <input
            type="text"
            name="work_location"
            placeholder="Work Location"
            value={form.work_location}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
        </div>
        <textarea
          name="key_requirements"
          placeholder="Key Requirements (comma separated)"
          value={form.key_requirements}
          onChange={handleChange}
          rows={3}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          required
        />
        <button
          type="submit"
          disabled={emailMutation.isPending}
          className="w-full flex items-center justify-center px-6 py-3 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg hover:bg-gray-800 dark:hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {emailMutation.isPending ? 'Generating...' : 'Generate Email'}
        </button>
      </form>
      </div>

      {emailMutation.error && (
        <p className="text-red-600 mt-4">{(emailMutation.error as Error)?.message || 'Failed to generate email'}</p>
      )}

      {emailMutation.data?.email && (
        <div className="mt-8 bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700 relative space-y-4">
          <h2 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">Generated Email</h2>
          <pre className="whitespace-pre-wrap break-words text-gray-800 dark:text-gray-100 max-h-64 overflow-y-auto">{emailMutation.data?.email}</pre>
          <button
            type="button"
            onClick={() => {
              if (!emailMutation.data?.email) return;
              navigator.clipboard.writeText(emailMutation.data.email);
              setCopied(true);
              setTimeout(() => setCopied(false), 2000);
            }}
            aria-label="Copy email"
            className="absolute top-4 right-4 flex items-center px-3 py-2 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg hover:bg-gray-800 dark:hover:bg-gray-100 transition-all transform active:scale-95"
          >
            {copied ? <Check className="h-4 w-4 text-green-400 transition-opacity" /> : <Copy className="h-4 w-4" />}
          </button>
        </div>
      )}
    </div>
  );
};
