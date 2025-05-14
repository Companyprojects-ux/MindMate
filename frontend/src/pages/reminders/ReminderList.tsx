import { useEffect, useState } from 'react';
import { reminderService } from '../../services/reminderService';
import { medicationService } from '../../services/medicationService';
import { Reminder, Medication } from '../../types';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';
import { Bell, Check, X, Plus, Calendar } from 'lucide-react';
import { format, isToday, isTomorrow, parseISO } from 'date-fns';
import { useForm } from 'react-hook-form';

type NewReminderForm = {
  medication_id: string;
  scheduled_time: string;
};

const ReminderList = () => {
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [medications, setMedications] = useState<Medication[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [formLoading, setFormLoading] = useState(false);

  const { register, handleSubmit, reset, formState: { errors } } = useForm<NewReminderForm>({
    defaultValues: {
      scheduled_time: new Date().toISOString().slice(0, 16),
    }
  });

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const [remindersData, medicationsData] = await Promise.all([
          reminderService.getReminders(),
          medicationService.getMedications()
        ]);
        setReminders(remindersData);
        setMedications(medicationsData);
      } catch (err) {
        setError('Failed to load reminders data');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleStatusUpdate = async (id: string, status: 'completed' | 'missed') => {
    try {
      await reminderService.updateReminderStatus(id, { status });
      setReminders(reminders.map(reminder => 
        reminder.reminder_id === id 
          ? { ...reminder, status } 
          : reminder
      ));
    } catch (err) {
      setError('Failed to update reminder status');
      console.error(err);
    }
  };

  const onSubmit = async (data: NewReminderForm) => {
    setFormLoading(true);
    try {
      const newReminder = await reminderService.createReminder({
        ...data,
        status: 'pending'
      });
      setReminders([newReminder, ...reminders]);
      setShowAddForm(false);
      reset();
    } catch (err) {
      setError('Failed to create reminder');
      console.error(err);
    } finally {
      setFormLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = parseISO(dateString);
    if (isToday(date)) {
      return `Today at ${format(date, 'h:mm a')}`;
    } else if (isTomorrow(date)) {
      return `Tomorrow at ${format(date, 'h:mm a')}`;
    }
    return format(date, 'MMM d, yyyy - h:mm a');
  };

  // Group reminders by date
  const groupedReminders = reminders.reduce((groups, reminder) => {
    const date = parseISO(reminder.scheduled_time);
    const dateKey = format(date, 'yyyy-MM-dd');
    if (!groups[dateKey]) {
      groups[dateKey] = [];
    }
    groups[dateKey].push(reminder);
    return groups;
  }, {} as Record<string, Reminder[]>);

  // Sort dates
  const sortedDates = Object.keys(groupedReminders).sort((a, b) => 
    new Date(a).getTime() - new Date(b).getTime()
  );

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Medication Reminders</h1>
        <Button 
          leftIcon={<Plus size={16} />}
          onClick={() => setShowAddForm(!showAddForm)}
        >
          Add Reminder
        </Button>
      </div>

      {error && (
        <div className="bg-error-50 border border-error-200 text-error-700 px-4 py-3 rounded-md mb-6">
          <p>{error}</p>
        </div>
      )}

      {showAddForm && (
        <Card className="mb-6 animate-slideIn">
          <h2 className="text-lg font-semibold mb-4">Create New Reminder</h2>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="form-group">
              <label htmlFor="medication_id" className="form-label">Medication</label>
              <select
                id="medication_id"
                className="form-input"
                {...register('medication_id', { required: 'Please select a medication' })}
              >
                <option value="">Select a medication</option>
                {medications.map(med => (
                  <option key={med.medication_id} value={med.medication_id}>
                    {med.name} ({med.dosage})
                  </option>
                ))}
              </select>
              {errors.medication_id && <p className="form-error">{errors.medication_id.message}</p>}
            </div>
            
            <div className="form-group">
              <label htmlFor="scheduled_time" className="form-label">Scheduled Time</label>
              <input
                id="scheduled_time"
                type="datetime-local"
                className="form-input"
                {...register('scheduled_time', { required: 'Scheduled time is required' })}
              />
              {errors.scheduled_time && <p className="form-error">{errors.scheduled_time.message}</p>}
            </div>
            
            <div className="flex justify-end space-x-3">
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowAddForm(false)}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                isLoading={formLoading}
              >
                Create Reminder
              </Button>
            </div>
          </form>
        </Card>
      )}

      {isLoading ? (
        <div className="space-y-6">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="animate-pulse">
              <div className="h-6 bg-gray-200 rounded w-1/3 mb-3"></div>
              <div className="space-y-3">
                {[...Array(2)].map((_, j) => (
                  <div key={j} className="bg-white rounded-lg shadow-card p-4 flex">
                    <div className="w-10 h-10 bg-gray-200 rounded-full"></div>
                    <div className="ml-3 flex-1">
                      <div className="h-4 bg-gray-200 rounded w-1/3 mb-2"></div>
                      <div className="h-3 bg-gray-200 rounded w-1/4"></div>
                    </div>
                    <div className="w-20 h-8 bg-gray-200 rounded"></div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : reminders.length === 0 ? (
        <Card className="text-center py-8">
          <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <Bell size={24} className="text-gray-400" />
          </div>
          <h2 className="text-xl font-medium text-gray-700 mb-2">No reminders found</h2>
          <p className="text-gray-500 mb-6">Create your first reminder to stay on track with your medications</p>
          <Button leftIcon={<Plus size={16} />} onClick={() => setShowAddForm(true)}>
            Add Reminder
          </Button>
        </Card>
      ) : (
        <div className="space-y-6">
          {sortedDates.map(dateKey => {
            const dateReminders = groupedReminders[dateKey];
            const date = parseISO(dateKey);
            const isDateToday = isToday(date);
            const isDateTomorrow = isTomorrow(date);
            
            let dateHeading = format(date, 'EEEE, MMMM d, yyyy');
            if (isDateToday) dateHeading = 'Today';
            if (isDateTomorrow) dateHeading = 'Tomorrow';
            
            return (
              <div key={dateKey} className="animate-fadeIn">
                <div className="flex items-center mb-3">
                  <Calendar size={18} className="text-gray-500 mr-2" />
                  <h2 className="text-lg font-semibold text-gray-800">{dateHeading}</h2>
                </div>
                <div className="space-y-3">
                  {dateReminders.map(reminder => (
                    <Card key={reminder.reminder_id} className="p-4 flex items-center">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                        reminder.status === 'completed' 
                          ? 'bg-success-100 text-success-700' 
                          : reminder.status === 'missed' 
                            ? 'bg-error-100 text-error-700' 
                            : 'bg-warning-100 text-warning-700'
                      }`}>
                        <Bell size={20} />
                      </div>
                      <div className="ml-3 flex-1">
                        <h3 className="font-medium">{reminder.medication_name}</h3>
                        <p className="text-sm text-gray-500">{formatDate(reminder.scheduled_time)}</p>
                      </div>
                      
                      {reminder.status === 'pending' && (
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            variant="outline"
                            className="text-success-700 hover:bg-success-50"
                            leftIcon={<Check size={16} />}
                            onClick={() => handleStatusUpdate(reminder.reminder_id, 'completed')}
                          >
                            Taken
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            className="text-error-700 hover:bg-error-50"
                            leftIcon={<X size={16} />}
                            onClick={() => handleStatusUpdate(reminder.reminder_id, 'missed')}
                          >
                            Missed
                          </Button>
                        </div>
                      )}
                      
                      {reminder.status !== 'pending' && (
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          reminder.status === 'completed' 
                            ? 'bg-success-100 text-success-800' 
                            : 'bg-error-100 text-error-800'
                        }`}>
                          {reminder.status === 'completed' ? 'Taken' : 'Missed'}
                        </span>
                      )}
                    </Card>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default ReminderList;