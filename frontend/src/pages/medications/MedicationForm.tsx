import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import { ArrowLeft, Plus, X } from 'lucide-react';
import { medicationService } from '../../services/medicationService';
import { MedicationFormData, Medication } from '../../types';
import Button from '../../components/ui/Button';
import FormInput from '../../components/ui/FormInput';
import Card from '../../components/ui/Card';

const initialFormData: MedicationFormData = {
  name: '',
  dosage: '',
  frequency: 'daily',
  time_of_day: 'morning',
  specific_times: ['08:00'],
  start_date: new Date().toISOString().split('T')[0],
  medication_type: 'pill',
};

const MedicationForm = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEditMode = !!id;
  
  const [isLoading, setIsLoading] = useState(isEditMode);
  const [error, setError] = useState<string | null>(null);
  const [submitLoading, setSubmitLoading] = useState(false);
  
  const { 
    register, 
    handleSubmit, 
    formState: { errors }, 
    reset,
    control,
    setValue,
    watch
  } = useForm<MedicationFormData>({
    defaultValues: initialFormData
  });

  const specificTimes = watch('specific_times') || [];

  useEffect(() => {
    if (isEditMode && id) {
      const fetchMedication = async () => {
        setIsLoading(true);
        setError(null);
        try {
          const data = await medicationService.getMedication(id);
          // Convert data to form format
          const formData: MedicationFormData = {
            name: data.name,
            dosage: data.dosage,
            frequency: data.frequency,
            time_of_day: data.time_of_day,
            specific_times: data.specific_times,
            start_date: data.start_date,
            end_date: data.end_date || undefined,
            medication_type: data.medication_type,
            notes: data.notes || undefined,
          };
          reset(formData);
        } catch (err) {
          setError('Failed to load medication data');
          console.error(err);
        } finally {
          setIsLoading(false);
        }
      };

      fetchMedication();
    }
  }, [id, isEditMode, reset]);

  const onSubmit = async (data: MedicationFormData) => {
    setSubmitLoading(true);
    setError(null);
    try {
      if (isEditMode && id) {
        await medicationService.updateMedication(id, data);
      } else {
        await medicationService.createMedication(data);
      }
      navigate('/medications');
    } catch (err) {
      setError(`Failed to ${isEditMode ? 'update' : 'create'} medication`);
      console.error(err);
    } finally {
      setSubmitLoading(false);
    }
  };

  const addTimeSlot = () => {
    setValue('specific_times', [...specificTimes, '12:00']);
  };

  const removeTimeSlot = (index: number) => {
    const newTimes = [...specificTimes];
    newTimes.splice(index, 1);
    setValue('specific_times', newTimes);
  };

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-6"></div>
        <Card>
          <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-6">
            <div className="h-10 bg-gray-200 rounded"></div>
            <div className="h-10 bg-gray-200 rounded"></div>
            <div className="h-10 bg-gray-200 rounded"></div>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div>
      <Link to="/medications" className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-6">
        <ArrowLeft size={16} className="mr-1" /> Back to medications
      </Link>
      
      <h1 className="text-2xl font-bold mb-6">
        {isEditMode ? 'Edit Medication' : 'Add New Medication'}
      </h1>

      {error && (
        <div className="bg-error-50 border border-error-200 text-error-700 px-4 py-3 rounded-md mb-6">
          <p>{error}</p>
        </div>
      )}

      <Card>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <FormInput
              id="name"
              label="Medication Name"
              type="text"
              placeholder="e.g., Aspirin"
              {...register('name', { required: 'Medication name is required' })}
              error={errors.name?.message}
            />
            
            <FormInput
              id="dosage"
              label="Dosage"
              type="text"
              placeholder="e.g., 100mg"
              {...register('dosage', { required: 'Dosage is required' })}
              error={errors.dosage?.message}
            />
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <div className="form-group">
              <label htmlFor="frequency" className="form-label">Frequency</label>
              <select
                id="frequency"
                className="form-input"
                {...register('frequency', { required: 'Frequency is required' })}
              >
                <option value="daily">Daily</option>
                <option value="twice_daily">Twice Daily</option>
                <option value="three_times_daily">Three Times Daily</option>
                <option value="four_times_daily">Four Times Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="as_needed">As Needed</option>
              </select>
              {errors.frequency && <p className="form-error">{errors.frequency.message}</p>}
            </div>
            
            <div className="form-group">
              <label htmlFor="time_of_day" className="form-label">Time of Day</label>
              <select
                id="time_of_day"
                className="form-input"
                {...register('time_of_day', { required: 'Time of day is required' })}
              >
                <option value="morning">Morning</option>
                <option value="afternoon">Afternoon</option>
                <option value="evening">Evening</option>
                <option value="night">Night</option>
                <option value="with_food">With Food</option>
                <option value="before_food">Before Food</option>
                <option value="after_food">After Food</option>
                <option value="multiple">Multiple Times</option>
              </select>
              {errors.time_of_day && <p className="form-error">{errors.time_of_day.message}</p>}
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Specific Times</label>
            <div className="space-y-3">
              {specificTimes.map((time, index) => (
                <div key={index} className="flex items-center">
                  <input
                    type="time"
                    className="form-input"
                    value={time}
                    onChange={(e) => {
                      const newTimes = [...specificTimes];
                      newTimes[index] = e.target.value;
                      setValue('specific_times', newTimes);
                    }}
                  />
                  {index > 0 && (
                    <button
                      type="button"
                      onClick={() => removeTimeSlot(index)}
                      className="ml-2 p-1 text-gray-500 hover:text-error-600"
                    >
                      <X size={16} />
                    </button>
                  )}
                </div>
              ))}
              <Button
                type="button"
                variant="outline"
                size="sm"
                leftIcon={<Plus size={16} />}
                onClick={addTimeSlot}
              >
                Add Time
              </Button>
            </div>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <FormInput
              id="start_date"
              label="Start Date"
              type="date"
              {...register('start_date', { required: 'Start date is required' })}
              error={errors.start_date?.message}
            />
            
            <FormInput
              id="end_date"
              label="End Date (Optional)"
              type="date"
              {...register('end_date')}
            />
          </div>

          <div className="form-group">
            <label htmlFor="medication_type" className="form-label">Medication Type</label>
            <select
              id="medication_type"
              className="form-input"
              {...register('medication_type', { required: 'Medication type is required' })}
            >
              <option value="pill">Pill</option>
              <option value="tablet">Tablet</option>
              <option value="capsule">Capsule</option>
              <option value="liquid">Liquid</option>
              <option value="injection">Injection</option>
              <option value="topical">Topical</option>
              <option value="inhaler">Inhaler</option>
              <option value="other">Other</option>
            </select>
            {errors.medication_type && <p className="form-error">{errors.medication_type.message}</p>}
          </div>

          <div className="form-group">
            <label htmlFor="notes" className="form-label">Notes (Optional)</label>
            <textarea
              id="notes"
              className="form-input min-h-[100px]"
              placeholder="Any special instructions or additional information"
              {...register('notes')}
            ></textarea>
          </div>

          <div className="flex justify-end space-x-3">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/medications')}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              isLoading={submitLoading}
            >
              {isEditMode ? 'Update Medication' : 'Add Medication'}
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default MedicationForm;