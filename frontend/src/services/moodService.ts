import { apiService } from './api';
import { MoodEntry, MoodFormData, MoodStatistics } from '../types';

export const moodService = {
  // Get all mood entries
  getMoodEntries: async (): Promise<MoodEntry[]> => {
    return apiService.get<MoodEntry[]>('/moods');
  },

  // Create a new mood entry
  createMoodEntry: async (data: MoodFormData): Promise<MoodEntry> => {
    return apiService.post<MoodEntry>('/moods', data);
  },

  // Get mood statistics
  getMoodStatistics: async (): Promise<MoodStatistics> => {
    return apiService.get<MoodStatistics>('/moods/stats');
  },
};