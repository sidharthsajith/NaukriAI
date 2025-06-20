import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/Layout/Layout';
import { Dashboard } from './pages/Dashboard';
import { AISearch } from './pages/AISearch';
import { AdvancedMatch } from './pages/AdvancedMatch';
import { CVAnalyzer } from './pages/CVAnalyzer';
import { CVComparator } from './pages/CVComparator';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<Dashboard />} />
              <Route path="search" element={<AISearch />} />
              <Route path="match" element={<AdvancedMatch />} />
              <Route path="cv-analyzer" element={<CVAnalyzer />} />
              <Route path="cv-compare" element={<CVComparator />} />
            </Route>
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;