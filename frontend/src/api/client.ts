import axios from 'axios';
import { ApiError, FastAPIError } from '../types/api';

// Configure base URL - fallback to localhost if env var not set
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 10000, // Reduced timeout for faster failure detection
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor with FastAPI error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    let apiError: ApiError;
    
    if (error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK' || !error.response) {
      // Network or timeout error
      apiError = {
        message: 'Unable to connect to server. Please check your connection or try again later.',
        status: 0,
        isNetworkError: true,
      };
    } else if (error.response) {
      // Handle FastAPI validation errors (422)
      if (error.response.status === 422 && error.response.data?.detail) {
        const fastApiError = error.response.data as FastAPIError;
        const validationMessages = fastApiError.detail.map(err => 
          `${err.loc.join('.')}: ${err.msg}`
        ).join(', ');
        
        apiError = {
          message: `Validation Error: ${validationMessages}`,
          status: error.response.status,
        };
      } else {
        // Other server errors
        apiError = {
          message: error.response.data?.message || error.message || 'An error occurred',
          status: error.response.status,
        };
      }
    } else {
      // Other errors
      apiError = {
        message: error.message || 'An unexpected error occurred',
        status: undefined,
      };
    }
    
    return Promise.reject(apiError);
  }
);

// Health check function
export const checkHealth = async (): Promise<boolean> => {
  try {
    await apiClient.get('/health');
    return true;
  } catch {
    return false;
  }
};

export default apiClient;