import { apiService } from './api';
import { AiRecommendations, AiSuggestions, ChatMessage, MoodEntry, WeeklyReport } from '../types';

export const aiService = {
  // Send a message to the chatbot
  sendMessage: async (message: string): Promise<{ response: string }> => {
    return apiService.post<{ response: string }>('/ai/chat', { message });
  },

  // Get chat history
  getChatHistory: async (): Promise<ChatMessage[]> => {
    return apiService.get<ChatMessage[]>('/ai/chat/history');
  },

  // Get AI suggestions
  getAiSuggestions: async (): Promise<AiSuggestions> => {
    return apiService.get<AiSuggestions>('/ai/suggestions');
  },

  // Submit feedback on AI suggestions
  submitFeedback: async (feedback: string): Promise<{ message: string }> => {
    return apiService.post<{ message: string }>(`/ai/feedback?feedback=${feedback}`, {});
  },

  // Get visualization data
  getVisualizationData: async (dataType: 'mood' | 'medication' | 'journal'): Promise<any> => {
    return apiService.get<any>(`/ai/visualization_data?data_type=${dataType}`);
  },

  // Get personalized recommendations
  getRecommendations: async (): Promise<AiRecommendations> => {
    return apiService.get<AiRecommendations>('/ai/recommendations');
  },

  // Get weekly progress report
  getWeeklyReport: async (): Promise<WeeklyReport> => {
    return apiService.get<WeeklyReport>('/ai/weekly-report');
  },
};