import React from 'react';
import { Search } from 'lucide-react';
import { clsx } from 'clsx';

interface EmptyStateProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
  action?: React.ReactNode;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  description,
  icon,
  action,
  className,
}) => {
  return (
    <div className={clsx(
      'flex flex-col items-center justify-center p-8 text-center',
      className
    )}>
      {icon || <Search className="h-12 w-12 text-gray-400 mb-4" />}
      <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
        {title}
      </h3>
      <p className="text-gray-500 dark:text-gray-400 mb-4 max-w-md">
        {description}
      </p>
      {action}
    </div>
  );
};