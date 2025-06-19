import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { cvApi } from '../api/cv';
import { FileUploader } from '../components/CVAnalyzer/FileUploader';
import { AnalysisResults } from '../components/CVAnalyzer/AnalysisResults';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { CVAnalysisResult } from '../types/api';

export const CVAnalyzer: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [analysisResult, setAnalysisResult] = useState<CVAnalysisResult | null>(null);

  const analysisMutation = useMutation({
    mutationFn: cvApi.analyzeCV,
    onSuccess: (data) => {
      setAnalysisResult(data);
    },
  });

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setAnalysisResult(null);
    analysisMutation.mutate(file);
  };

  const handleClearFile = () => {
    setSelectedFile(null);
    setAnalysisResult(null);
    analysisMutation.reset();
  };

  const handleRetry = () => {
    if (selectedFile) {
      analysisMutation.mutate(selectedFile);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          CV Analyzer
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Extract key information and insights from candidate CVs
        </p>
      </div>

      <FileUploader
        onFileSelect={handleFileSelect}
        selectedFile={selectedFile}
        onClearFile={handleClearFile}
        isLoading={analysisMutation.isPending}
      />

      {analysisMutation.isPending && (
        <div className="bg-white dark:bg-gray-800 p-8 rounded-lg border border-gray-200 dark:border-gray-700">
          <LoadingSpinner size="lg" className="mb-4" />
          <div className="text-center">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Analyzing CV...
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Our AI is extracting information from the uploaded document.
            </p>
          </div>
        </div>
      )}

      {analysisMutation.error && (
        <ErrorMessage 
          message={analysisMutation.error.message} 
          onRetry={handleRetry} 
        />
      )}

      {analysisResult && (
        <AnalysisResults result={analysisResult} />
      )}
    </div>
  );
};