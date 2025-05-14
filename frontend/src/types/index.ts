// User types
export interface User {
  user_id: string;
  email: string;
  name: string;
  created_at: number;
  updated_at: number;
  preferences: {
    theme?: string;
    notifications_enabled?: boolean;
  };
  notification_settings: {
    email?: boolean;
    push?: boolean;
  };
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  name: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// Medication types
export interface Medication {
  medication_id: string;
  user_id: string;
  name: string;
  dosage: string;
  frequency: string;
  time_of_day: string;
  specific_times: string[];
  start_date: string;
  end_date: string | null;
  notes: string | null;
  medication_type: string;
  image_url: string | null;
  created_at: number;
  updated_at: number;
}

export interface MedicationFormData {
  name: string;
  dosage: string;
  frequency: string;
  time_of_day: string;
  specific_times: string[];
  start_date: string;
  end_date?: string;
  notes?: string;
  medication_type: string;
  image_url?: string;
}

// Reminder types
export interface Reminder {
  reminder_id: string;
  user_id: string;
  medication_id: string;
  medication_name: string;
  scheduled_time: string;
  status: 'pending' | 'completed' | 'missed';
  created_at: number;
  updated_at: number;
}

export interface ReminderFormData {
  medication_id: string;
  scheduled_time: string;
  status: 'pending' | 'completed' | 'missed';
}

export interface ReminderStatusUpdate {
  status: 'pending' | 'completed' | 'missed';
}

// Mood types
export interface MoodEntry {
  entry_id: string;
  user_id: string;
  mood_rating: number;
  tags: string[];
  notes: string;
  timestamp: string;
  created_at: number;
  updated_at: number;
}

export interface MoodFormData {
  mood_rating: number;
  tags: string[];
  notes: string;
}

export interface MoodStatistics {
  average_rating: number;
  highest_rating: number;
  lowest_rating: number;
  most_common_tags: { tag: string; count: number }[];
  mood_trend: { date: string; average_rating: number }[];
  total_entries: number;
}

// Journal types
export interface JournalEntry {
  entry_id: string;
  user_id: string;
  title: string;
  content: string;
  tags: string[];
  timestamp: string;
  created_at: number;
  updated_at: number;
}

export interface JournalFormData {
  title: string;
  content: string;
  tags: string[];
}

// AI Chat types
export interface ChatMessage {
  message_id: string;
  message: string;
  is_user: boolean;
  timestamp: string;
}

export interface AiSuggestions {
  journal_prompt: string;
  coping_tip: string;
  motivational_content: string;
  medication_tip: string;
}

export interface AiRecommendations {
  journal_prompts: {
    title: string;
    prompt: string;
  }[];
  coping_strategies: {
    title: string;
    description: string;
  }[];
  timestamp: string;
  user_id: string;
}

export interface WeeklyReport {
  report: string;
}