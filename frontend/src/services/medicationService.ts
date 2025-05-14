import { apiService } from './api';
import { Medication, MedicationFormData } from '../types';

export const medicationService = {
  // Get all medications
  getMedications: async (): Promise<Medication[]> => {
    return apiService.get<Medication[]>('/medications');
  },

  // Get a single medication by ID
  getMedication: async (id: string): Promise<Medication> => {
    return apiService.get<Medication>(`/medications/${id}`);
  },

  // Create a new medication
  createMedication: async (data: MedicationFormData): Promise<Medication> => {
    return apiService.post<Medication>('/medications', data);
  },

  // Update an existing medication
  updateMedication: async (id: string, data: MedicationFormData): Promise<Medication> => {
    return apiService.put<Medication>(`/medications/${id}`, data);
  },

  // Delete a medication
  deleteMedication: async (id: string): Promise<void> => {
    return apiService.delete<void>(`/medications/${id}`);
  },
};