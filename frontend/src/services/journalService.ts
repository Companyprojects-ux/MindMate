import { apiService } from './api';
import { JournalEntry, JournalFormData } from '../types';

export const journalService = {
  // Get all journal entries
  getJournalEntries: async (): Promise<JournalEntry[]> => {
    return apiService.get<JournalEntry[]>('/journal');
  },

  // Create a new journal entry
  createJournalEntry: async (data: JournalFormData): Promise<JournalEntry> => {
    return apiService.post<JournalEntry>('/journal', data);
  },

  // Search journal entries
  searchJournalEntries: async (query: string): Promise<JournalEntry[]> => {
    return apiService.get<JournalEntry[]>(`/journal/search?query=${query}`);
  },
};