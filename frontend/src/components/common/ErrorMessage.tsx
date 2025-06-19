import React from 'react';
import { AlertCircle, WifiOff } from 'lucide-react';
import { clsx } from 'clsx';
import { ApiError } from '../../types/api';

interface ErrorMessageProps {
  error: string | ApiError;
  className?: string;
  onRetry?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ 
  error, 
  className,
  onRetry 
}) => {
  const isApiError = typeof error === 'object';
  const message = isApiError ? error.message : error;
  const isNetworkError = isApiError && error.isNetworkError;

  return (
    <div className={clsx(
      'flex flex-col items-center justify-center p-8 text-center',
      className
    )}>
      {isNetworkError ? (
        <WifiOff className="h-12 w-12 text-orange-500 mb-4" />
      ) : (
        <AlertCircle className="h-12 w-12 text-red-500 mb-4" />
      )}
      
      <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
        {isNetworkError ? 'Connection Issue' : 'Something went wrong'}
      </h3>
      
      <p className="text-gray-500 dark:text-gray-400 mb-4 max-w-md">
        {message}
      </p>
      
      {isNetworkError && (
        <p className="text-sm text-gray-400 dark:text-gray-500 mb-4">
          The app is running in offline mode with sample data.
        </p>
      )}
      
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg hover:bg-gray-800 dark:hover:bg-gray-100 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  );
};