import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X } from 'lucide-react';

interface FileUploaderProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  onClearFile: () => void;
  isLoading: boolean;
}

export const FileUploader: React.FC<FileUploaderProps> = ({
  onFileSelect,
  selectedFile,
  onClearFile,
  isLoading,
}) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    multiple: false,
    disabled: isLoading,
  });

  if (selectedFile) {
    return (
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <FileText className="h-8 w-8 text-gray-600 dark:text-gray-300 mr-3" />
            <div>
              <div className="font-medium text-gray-900 dark:text-white">
                {selectedFile.name}
              </div>
              <div className="text-sm text-gray-500 dark:text-gray-400">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </div>
            </div>
          </div>
          {!isLoading && (
            <button
              onClick={onClearFile}
              className="p-2 text-gray-400 hover:text-red-500 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        CV Analysis
      </h2>
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        Upload a CV/Resume to extract key information and get insights about the candidate.
      </p>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-gray-400 bg-gray-50 dark:bg-gray-700/50'
            : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
        } ${isLoading ? 'cursor-not-allowed opacity-50' : ''}`}
      >
        <input {...getInputProps()} />
        <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        {isDragActive ? (
          <p className="text-gray-600 dark:text-gray-400">
            Drop the CV file here...
          </p>
        ) : (
          <div>
            <p className="text-gray-600 dark:text-gray-400 mb-2">
              Drag & drop a CV here, or click to select
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-500">
              Supports PDF, DOC, and DOCX files
            </p>
          </div>
        )}
      </div>
    </div>
  );
};