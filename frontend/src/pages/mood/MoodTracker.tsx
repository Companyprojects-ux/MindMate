import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { SmilePlus, BarChart3 } from 'lucide-react';
import { moodService } from '../../services/moodService';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';
import FormInput from '../../components/ui/FormInput';

type FormValues = {
  mood_rating: number;
  notes: string;
};

const moodEmojis = ['😞', '😟', '😐', '🙂', '😊', '😄', '😃', '😁', '🤩', '😍'];
const commonTags = ['happy', 'relaxed', 'tired', 'stressed', 'anxious', 'calm', 'energetic', 'sad', 'angry', 'focused'];

const MoodTracker = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [selectedRating, setSelectedRating] = useState<number | null>(null);

  const { register, handleSubmit, reset, setValue, formState: { errors } } = useForm<FormValues>({
    defaultValues: {
      mood_rating: 5,
      notes: '',
    }
  });

  const handleTagToggle = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag) 
        : [...prev, tag]
    );
  };

  const handleRatingSelect = (rating: number) => {
    setSelectedRating(rating);
    setValue('mood_rating', rating);
  };

  const onSubmit = async (data: FormValues) => {
    setIsLoading(true);
    setError(null);
    setSuccess(false);
    
    try {
      await moodService.createMoodEntry({
        mood_rating: data.mood_rating,
        tags: selectedTags,
        notes: data.notes,
      });
      
      setSuccess(true);
      reset();
      setSelectedTags([]);
      setSelectedRating(null);
      
      // Reset form after 3 seconds
      setTimeout(() => {
        setSuccess(false);
      }, 3000);
    } catch (err) {
      setError('Failed to save mood entry');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Mood Tracker</h1>
        <Link to="/mood/stats">
          <Button leftIcon={<BarChart3 size={16} />}>View Statistics</Button>
        </Link>
      </div>

      {error && (
        <div className="bg-error-50 border border-error-200 text-error-700 px-4 py-3 rounded-md mb-6">
          <p>{error}</p>
        </div>
      )}

      {success && (
        <div className="bg-success-50 border border-success-200 text-success-700 px-4 py-3 rounded-md mb-6 animate-fadeIn">
          <p>Mood entry saved successfully!</p>
        </div>
      )}

      <Card>
        <h2 className="text-lg font-semibold mb-6">How are you feeling today?</h2>
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="form-group">
            <label className="form-label">Mood Rating (1-10)</label>
            <div className="flex justify-between items-center mt-2 mb-4">
              <span className="text-gray-500 text-sm">Low</span>
              <span className="text-gray-500 text-sm">High</span>
            </div>
            <div className="grid grid-cols-10 gap-1 mb-2">
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((rating) => (
                <button
                  key={rating}
                  type="button"
                  className={`flex flex-col items-center p-3 rounded-md transition-colors ${
                    selectedRating === rating
                      ? 'bg-primary-100 text-primary-800 border-2 border-primary-400'
                      : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                  }`}
                  onClick={() => handleRatingSelect(rating)}
                >
                  <span className="text-xl mb-1">{moodEmojis[rating - 1]}</span>
                  <span className="text-sm font-medium">{rating}</span>
                </button>
              ))}
            </div>
            <input 
              type="hidden" 
              {...register('mood_rating', { 
                required: 'Please select a mood rating',
                min: { value: 1, message: 'Rating must be at least 1' },
                max: { value: 10, message: 'Rating must not exceed 10' }
              })} 
            />
            {errors.mood_rating && <p className="form-error">{errors.mood_rating.message}</p>}
          </div>
          
          <div className="form-group">
            <label className="form-label">How would you describe your mood? (Select tags)</label>
            <div className="flex flex-wrap gap-2 mt-2">
              {commonTags.map((tag) => (
                <button
                  key={tag}
                  type="button"
                  className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                    selectedTags.includes(tag)
                      ? 'bg-primary-100 text-primary-800 border border-primary-300'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200 border border-transparent'
                  }`}
                  onClick={() => handleTagToggle(tag)}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="notes" className="form-label">Additional Notes (Optional)</label>
            <textarea
              id="notes"
              className="form-input min-h-[100px]"
              placeholder="How are you feeling? What happened today that affected your mood?"
              {...register('notes')}
            ></textarea>
          </div>
          
          <div className="flex justify-end">
            <Button
              type="submit"
              isLoading={isLoading}
              leftIcon={<SmilePlus size={18} />}
            >
              Save Mood Entry
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default MoodTracker;