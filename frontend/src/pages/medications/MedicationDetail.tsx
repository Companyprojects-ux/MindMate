import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Edit, Trash2, Calendar, Clock, FileText } from 'lucide-react';
import { medicationService } from '../../services/medicationService';
import { Medication } from '../../types';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';

const MedicationDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [medication, setMedication] = useState<Medication | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMedication = async () => {
      if (!id) return;
      
      setIsLoading(true);
      setError(null);
      try {
        const data = await medicationService.getMedication(id);
        setMedication(data);
      } catch (err) {
        setError('Failed to load medication details');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMedication();
  }, [id]);

  const handleDelete = async () => {
    if (!medication || !confirm('Are you sure you want to delete this medication?')) {
      return;
    }
    
    try {
      await medicationService.deleteMedication(medication.medication_id);
      navigate('/medications');
    } catch (err) {
      setError('Failed to delete medication');
      console.error(err);
    }
  };

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-6"></div>
        <Card>
          <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            <div className="h-4 bg-gray-200 rounded w-5/6"></div>
          </div>
        </Card>
      </div>
    );
  }

  if (error || !medication) {
    return (
      <div>
        <Link to="/medications" className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-6">
          <ArrowLeft size={16} className="mr-1" /> Back to medications
        </Link>
        
        <Card className="text-center py-6">
          <h2 className="text-xl font-medium text-gray-700 mb-4">
            {error || 'Medication not found'}
          </h2>
          <Button onClick={() => navigate('/medications')}>
            Go to Medications
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <Link to="/medications" className="inline-flex items-center text-primary-600 hover:text-primary-700">
          <ArrowLeft size={16} className="mr-1" /> Back to medications
        </Link>
        
        <div className="flex space-x-3">
          <Link to={`/medications/edit/${medication.medication_id}`}>
            <Button variant="primary" leftIcon={<Edit size={16} />}>
              Edit
            </Button>
          </Link>
          <Button 
            variant="outline" 
            leftIcon={<Trash2 size={16} />} 
            onClick={handleDelete}
            className="text-error-600 hover:bg-error-50 border-error-200"
          >
            Delete
          </Button>
        </div>
      </div>

      <h1 className="text-2xl font-bold mb-6">{medication.name}</h1>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <h2 className="text-lg font-semibold mb-4">Medication Details</h2>
          
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-medium text-gray-500">Dosage</h3>
              <p className="mt-1">{medication.dosage}</p>
            </div>
            
            <div>
              <h3 className="text-sm font-medium text-gray-500">Type</h3>
              <p className="mt-1">{medication.medication_type}</p>
            </div>
            
            <div>
              <h3 className="text-sm font-medium text-gray-500">Notes</h3>
              <p className="mt-1">{medication.notes || 'No notes'}</p>
            </div>
          </div>
        </Card>

        <Card>
          <h2 className="text-lg font-semibold mb-4">Schedule</h2>
          
          <div className="space-y-4">
            <div className="flex items-start">
              <Calendar size={18} className="text-gray-500 mr-2 mt-0.5" />
              <div>
                <h3 className="text-sm font-medium text-gray-500">Frequency</h3>
                <p className="mt-1">{medication.frequency}</p>
              </div>
            </div>
            
            <div className="flex items-start">
              <Clock size={18} className="text-gray-500 mr-2 mt-0.5" />
              <div>
                <h3 className="text-sm font-medium text-gray-500">Time of Day</h3>
                <p className="mt-1">{medication.time_of_day}</p>
              </div>
            </div>
            
            {medication.specific_times.length > 0 && (
              <div className="flex items-start">
                <Clock size={18} className="text-gray-500 mr-2 mt-0.5" />
                <div>
                  <h3 className="text-sm font-medium text-gray-500">Specific Times</h3>
                  <div className="mt-1 flex flex-wrap gap-2">
                    {medication.specific_times.map((time, i) => (
                      <span key={i} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                        {time}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}
            
            <div className="flex items-start">
              <Calendar size={18} className="text-gray-500 mr-2 mt-0.5" />
              <div>
                <h3 className="text-sm font-medium text-gray-500">Date Range</h3>
                <p className="mt-1">
                  Started: {new Date(medication.start_date).toLocaleDateString()}
                  {medication.end_date && ` · Ends: ${new Date(medication.end_date).toLocaleDateString()}`}
                </p>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Additional Actions */}
      <div className="mt-6">
        <Link to="/reminders">
          <Button variant="outline" leftIcon={<Clock size={16} />}>
            View Reminders
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default MedicationDetail;