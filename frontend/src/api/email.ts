import apiClient from './client';
import { OutreachEmailRequest, OutreachEmailResponse } from '../types/api';

/**
 * Generate a personalised outreach email for a candidate.
 */
export const emailApi = {
  generateEmail: async (payload: OutreachEmailRequest): Promise<OutreachEmailResponse> => {
    const response = await apiClient.post('/generate-outreach-email', payload);
    // FastAPI returns { email: "..." }
    const data = typeof response.data === 'string' ? JSON.parse(response.data) : response.data;
    return {
      email: data.email || '',
    };
  },
};
