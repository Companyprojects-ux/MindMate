import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { ArrowLeft, Plus, X, Save, Trash2 } from 'lucide-react';
import { journalService } from '../../services/journalService';
import { JournalFormData, JournalEntry } from '../../types';
import Button from '../../components/ui/Button';
import FormInput from '../../components/ui/FormInput';
import Card from '../../components/ui/Card';

const commonTags = ['important', 'personal', 'health', 'work', 'family', 'friends', 'anxiety', 'depression', 'gratitude', 'goals'];

const JournalForm = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEditMode = !!id;
  
  const [isLoading, setIsLoading] = useState(isEditMode);
  const [submitLoading, setSubmitLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [newTag, setNewTag] = useState('');
  
  const { register, handleSubmit, formState: { errors }, reset } = useForm<JournalFormData>();

  useEffect(() => {
    if (isEditMode && id) {
      const fetchJournalEntry = async () => {
        try {
          // In a real implementation, we would have a specific API endpoint to get a single entry
          // For now, we'll get all entries and filter
          const entries = await journalService.getJournalEntries();
          const entry = entries.find(entry => entry.entry_id === id);
          
          if (entry) {
            reset({
              title: entry.title,
              content: entry.content,
            });
            setSelectedTags(entry.tags);
          } else {
            setError('Journal entry not found');
          }
        } catch (err) {
          setError('Failed to load journal entry');
          console.error(err);
        } finally {
          setIsLoading(false);
        }
      };

      fetchJournalEntry();
    }
  }, [id, isEditMode, reset]);

  const onSubmit = async (data: JournalFormData) => {
    setSubmitLoading(true);
    setError(null);
    
    const formData = {
      ...data,
      tags: selectedTags,
    };
    
    try {
      if (isEditMode) {
        // This would be an update endpoint in a real implementation
        // For now we're just creating a new entry
        await journalService.createJournalEntry(formData);
      } else {
        await journalService.createJournalEntry(formData);
      }
      navigate('/journal');
    } catch (err) {
      setError(`Failed to ${isEditMode ? 'update' : 'create'} journal entry`);
      console.error(err);
    } finally {
      setSubmitLoading(false);
    }
  };

  const handleTagToggle = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag) 
        : [...prev, tag]
    );
  };

  const handleAddCustomTag = () => {
    if (newTag.trim() && !selectedTags.includes(newTag.trim())) {
      setSelectedTags(prev => [...prev, newTag.trim()]);
      setNewTag('');
    }
  };

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-6"></div>
        <Card>
          <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-6">
            <div className="h-10 bg-gray-200 rounded"></div>
            <div className="h-40 bg-gray-200 rounded"></div>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div>
      <Link to="/journal" className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-6">
        <ArrowLeft size={16} className="mr-1" /> Back to journal
      </Link>
      
      <h1 className="text-2xl font-bold mb-6">
        {isEditMode ? 'Edit Journal Entry' : 'New Journal Entry'}
      </h1>

      {error && (
        <div className="bg-error-50 border border-error-200 text-error-700 px-4 py-3 rounded-md mb-6">
          <p>{error}</p>
        </div>
      )}

      <Card>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <FormInput
            id="title"
            label="Title"
            type="text"
            placeholder="What's on your mind today?"
            {...register('title', { required: 'Title is required' })}
            error={errors.title?.message}
          />
          
          <div className="form-group">
            <label htmlFor="content" className="form-label">Content</label>
            <textarea
              id="content"
              className="form-input min-h-[200px]"
              placeholder="Write your thoughts, feelings, or experiences here..."
              {...register('content', { 
                required: 'Content is required',
                minLength: { value: 10, message: 'Content should be at least 10 characters' }
              })}
            ></textarea>
            {errors.content && <p className="form-error">{errors.content.message}</p>}
          </div>
          
          <div className="form-group">
            <label className="form-label">Tags</label>
            <div className="flex flex-wrap gap-2 mb-3">
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
            
            <div className="flex items-center mt-2 mb-3">
              <input
                type="text"
                className="form-input flex-1"
                placeholder="Add custom tag..."
                value={newTag}
                onChange={(e) => setNewTag(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleAddCustomTag();
                  }
                }}
              />
              <Button
                type="button"
                variant="outline"
                className="ml-2"
                onClick={handleAddCustomTag}
                disabled={!newTag.trim()}
              >
                Add
              </Button>
            </div>
            
            {selectedTags.length > 0 && (
              <div>
                <label className="form-label">Selected Tags:</label>
                <div className="flex flex-wrap gap-2 mt-1">
                  {selectedTags.map((tag, index) => (
                    <div 
                      key={index} 
                      className="flex items-center bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm"
                    >
                      {tag}
                      <button
                        type="button"
                        className="ml-1 text-primary-600 hover:text-primary-800"
                        onClick={() => setSelectedTags(prev => prev.filter(t => t !== tag))}
                      >
                        <X size={14} />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          
          <div className="flex justify-end space-x-3">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/journal')}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              isLoading={submitLoading}
              leftIcon={<Save size={16} />}
            >
              {isEditMode ? 'Update Entry' : 'Save Entry'}
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default JournalForm;