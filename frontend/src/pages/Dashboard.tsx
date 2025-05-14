import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Pill, Bell, BookHeart, SmilePlus, Brain, ChevronRight } from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { useAuthStore } from '../store/authStore';
import { medicationService } from '../services/medicationService';
import { reminderService } from '../services/reminderService';
import { moodService } from '../services/moodService';
import { journalService } from '../services/journalService';
import { aiService } from '../services/aiService';
import { Medication, Reminder, MoodEntry, JournalEntry, AiSuggestions } from '../types';

const Dashboard = () => {
  const { user } = useAuthStore();
  const [isLoading, setIsLoading] = useState(true);
  const [medications, setMedications] = useState<Medication[]>([]);
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [moodEntries, setMoodEntries] = useState<MoodEntry[]>([]);
  const [journalEntries, setJournalEntries] = useState<JournalEntry[]>([]);
  const [suggestions, setSuggestions] = useState<AiSuggestions | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        // Fetch data in parallel
        const [medsData, remindersData, moodData, journalData, suggestionsData] = await Promise.all([
          medicationService.getMedications(),
          reminderService.getReminders(),
          moodService.getMoodEntries(),
          journalService.getJournalEntries(),
          aiService.getAiSuggestions()
        ]);

        setMedications(medsData);
        setReminders(remindersData);
        setMoodEntries(moodData);
        setJournalEntries(journalData);
        setSuggestions(suggestionsData);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  // Filter reminders to only show today's reminders
  const todayReminders = reminders.filter(reminder => {
    const reminderDate = new Date(reminder.scheduled_time).toDateString();
    const today = new Date().toDateString();
    return reminderDate === today;
  });

  // Get the most recent mood entry
  const latestMood = moodEntries.length > 0 
    ? moodEntries.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())[0] 
    : null;

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Welcome back, {user?.name?.split(' ')[0] || 'User'}
        </h1>
        <p className="text-gray-600">
          Here's an overview of your health journey
        </p>
      </div>

      {error && (
        <div className="bg-error-50 border border-error-200 text-error-700 px-4 py-3 rounded-md mb-6">
          <p>{error}</p>
        </div>
      )}

      {isLoading ? (
        <div className="grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="bg-white rounded-lg shadow-card p-6 animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-5/6 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3 mb-4"></div>
              <div className="h-8 bg-gray-200 rounded w-1/3"></div>
            </div>
          ))}
        </div>
      ) : (
        <>
          {/* First row: Medications and Reminders */}
          <div className="grid gap-6 grid-cols-1 md:grid-cols-2 mb-6">
            <Card className="animate-fadeIn">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <Pill className="text-primary-600 mr-2" size={20} />
                  <h2 className="text-lg font-semibold">Medications</h2>
                </div>
                <Link to="/medications" className="text-primary-600 hover:text-primary-700 text-sm flex items-center">
                  View all <ChevronRight size={16} />
                </Link>
              </div>
              
              {medications.length === 0 ? (
                <div className="text-center py-4">
                  <p className="text-gray-500 mb-4">No medications added yet</p>
                  <Link to="/medications/new">
                    <Button variant="primary" size="sm">Add medication</Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-3">
                  {medications.slice(0, 3).map(med => (
                    <div key={med.medication_id} className="flex items-center p-3 rounded-md border border-gray-100 hover:bg-gray-50">
                      <div className="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center text-primary-600">
                        <Pill size={20} />
                      </div>
                      <div className="ml-3">
                        <h3 className="font-medium">{med.name}</h3>
                        <p className="text-sm text-gray-500">{med.dosage}, {med.frequency}</p>
                      </div>
                    </div>
                  ))}
                  
                  {medications.length > 0 && (
                    <Link to="/medications/new" className="inline-block mt-2">
                      <Button variant="outline" size="sm">Add medication</Button>
                    </Link>
                  )}
                </div>
              )}
            </Card>
            
            <Card className="animate-fadeIn" style={{ animationDelay: '100ms' }}>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <Bell className="text-secondary-600 mr-2" size={20} />
                  <h2 className="text-lg font-semibold">Today's Reminders</h2>
                </div>
                <Link to="/reminders" className="text-primary-600 hover:text-primary-700 text-sm flex items-center">
                  View all <ChevronRight size={16} />
                </Link>
              </div>
              
              {todayReminders.length === 0 ? (
                <div className="text-center py-4">
                  <p className="text-gray-500">No reminders for today</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {todayReminders.slice(0, 3).map(reminder => (
                    <div key={reminder.reminder_id} className="flex items-center justify-between p-3 rounded-md border border-gray-100 hover:bg-gray-50">
                      <div className="flex items-center">
                        <div className={`w-3 h-3 rounded-full mr-3 ${
                          reminder.status === 'completed' 
                            ? 'bg-success-500' 
                            : reminder.status === 'missed' 
                              ? 'bg-error-500' 
                              : 'bg-warning-500'
                        }`}></div>
                        <div>
                          <h3 className="font-medium">{reminder.medication_name}</h3>
                          <p className="text-sm text-gray-500">
                            {new Date(reminder.scheduled_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </p>
                        </div>
                      </div>
                      {reminder.status === 'pending' && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={async () => {
                            try {
                              await reminderService.updateReminderStatus(reminder.reminder_id, { status: 'completed' });
                              setReminders(
                                reminders.map(r => 
                                  r.reminder_id === reminder.reminder_id 
                                    ? { ...r, status: 'completed' } 
                                    : r
                                )
                              );
                            } catch (err) {
                              console.error(err);
                            }
                          }}
                        >
                          Mark as taken
                        </Button>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </Card>
          </div>
          
          {/* Second row: Mood, Journal, and AI */}
          <div className="grid gap-6 grid-cols-1 md:grid-cols-3">
            <Card className="animate-fadeIn" style={{ animationDelay: '200ms' }}>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <SmilePlus className="text-accent-600 mr-2" size={20} />
                  <h2 className="text-lg font-semibold">Mood</h2>
                </div>
                <Link to="/mood" className="text-primary-600 hover:text-primary-700 text-sm flex items-center">
                  Track <ChevronRight size={16} />
                </Link>
              </div>
              
              {!latestMood ? (
                <div className="text-center py-4">
                  <p className="text-gray-500 mb-4">No mood entries yet</p>
                  <Link to="/mood">
                    <Button variant="primary" size="sm">Track mood</Button>
                  </Link>
                </div>
              ) : (
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 text-2xl font-bold mb-2">
                    {latestMood.mood_rating}
                  </div>
                  <p className="text-sm text-gray-500 mb-2">
                    {new Date(latestMood.timestamp).toLocaleDateString()}
                  </p>
                  <div className="flex flex-wrap justify-center gap-2 mb-3">
                    {latestMood.tags.map((tag, i) => (
                      <span key={i} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                        {tag}
                      </span>
                    ))}
                  </div>
                  <Link to="/mood/stats">
                    <Button variant="outline" size="sm">View statistics</Button>
                  </Link>
                </div>
              )}
            </Card>
            
            <Card className="animate-fadeIn" style={{ animationDelay: '300ms' }}>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <BookHeart className="text-primary-600 mr-2" size={20} />
                  <h2 className="text-lg font-semibold">Journal</h2>
                </div>
                <Link to="/journal" className="text-primary-600 hover:text-primary-700 text-sm flex items-center">
                  View all <ChevronRight size={16} />
                </Link>
              </div>
              
              {journalEntries.length === 0 ? (
                <div className="text-center py-4">
                  <p className="text-gray-500 mb-4">No journal entries yet</p>
                  <Link to="/journal/new">
                    <Button variant="primary" size="sm">Write entry</Button>
                  </Link>
                </div>
              ) : (
                <div>
                  <div className="mb-3">
                    <h3 className="font-medium text-gray-900">
                      {journalEntries[0].title.length > 25 
                        ? `${journalEntries[0].title.substring(0, 25)}...` 
                        : journalEntries[0].title}
                    </h3>
                    <p className="text-sm text-gray-500 mb-1">
                      {new Date(journalEntries[0].timestamp).toLocaleDateString()}
                    </p>
                    <p className="text-sm text-gray-700 line-clamp-2">
                      {journalEntries[0].content}
                    </p>
                  </div>
                  <Link to="/journal/new">
                    <Button variant="outline" size="sm">New entry</Button>
                  </Link>
                </div>
              )}
            </Card>
            
            <Card className="animate-fadeIn" style={{ animationDelay: '400ms' }}>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <Brain className="text-secondary-600 mr-2" size={20} />
                  <h2 className="text-lg font-semibold">AI Support</h2>
                </div>
                <Link to="/ai-chat" className="text-primary-600 hover:text-primary-700 text-sm flex items-center">
                  Chat <ChevronRight size={16} />
                </Link>
              </div>
              
              {!suggestions ? (
                <div className="text-center py-4">
                  <p className="text-gray-500">Loading AI suggestions...</p>
                </div>
              ) : (
                <div>
                  <div className="mb-3 p-3 bg-secondary-50 rounded-md">
                    <h3 className="text-sm font-medium text-secondary-800 mb-1">Journal Prompt</h3>
                    <p className="text-sm text-gray-700">{suggestions.journal_prompt}</p>
                  </div>
                  <div className="mb-3 p-3 bg-primary-50 rounded-md">
                    <h3 className="text-sm font-medium text-primary-800 mb-1">Coping Tip</h3>
                    <p className="text-sm text-gray-700">{suggestions.coping_tip}</p>
                  </div>
                  <Link to="/ai-chat">
                    <Button variant="outline" size="sm" fullWidth>Ask AI something</Button>
                  </Link>
                </div>
              )}
            </Card>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;