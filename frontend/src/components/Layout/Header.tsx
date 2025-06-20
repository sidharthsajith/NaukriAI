import React from 'react';
import { Menu } from 'lucide-react';

import { OfflineIndicator } from '../common/OfflineIndicator';

interface HeaderProps {
  onMenuClick: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {


  return (
    <>
      <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 h-16">
        <div className="flex items-center justify-between h-full px-6">
          <button
            onClick={onMenuClick}
            className="p-2 rounded-md lg:hidden hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            <Menu className="h-5 w-5 text-gray-500 dark:text-gray-400" />
          </button>

          
        </div>
      </header>
      <OfflineIndicator />
    </>
  );
};