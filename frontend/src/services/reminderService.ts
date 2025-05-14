import { apiService } from './api';
import { Reminder, ReminderFormData, ReminderStatusUpdate } from '../types';

export const reminderService = {
  // Get all reminders
  getReminders: async (): Promise<Reminder[]> => {
    return apiService.get<Reminder[]>('/reminders');
  },

  // Create a new reminder
  createReminder: async (data: ReminderFormData): Promise<Reminder> => {
    return apiService.post<Reminder>('/reminders', data);
  },

  // Update reminder status
  updateReminderStatus: async (id: string, data: ReminderStatusUpdate): Promise<Reminder> => {
    return apiService.put<Reminder>(`/reminders/${id}/status`, data);
  },
};