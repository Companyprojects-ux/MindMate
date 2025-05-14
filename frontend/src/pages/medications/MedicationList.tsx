import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Pill, Edit, Trash2 } from 'lucide-react';
import { medicationService } from '../../services/medicationService';
import { Medication } from '../../types';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';

const MedicationList = () => {
  const [medications, setMedications] = useState<Medication[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMedications = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await medicationService.getMedications();
        setMedications(data);
      } catch (err) {
        setError('Failed to load medications');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMedications();
  }, []);

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this medication?')) {
      return;
    }
    
    try {
      await medicationService.deleteMedication(id);
      setMedications(medications.filter(med => med.medication_id !== id));
    } catch (err) {
      setError('Failed to delete medication');
      console.error(err);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Medications</h1>
        <Link to="/medications/new">
          <Button leftIcon={<Plus size={16} />}>Add Medication</Button>
        </Link>
      </div>

      {error && (
        <div className="bg-error-50 border border-error-200 text-error-700 px-4 py-3 rounded-md mb-6">
          <p>{error}</p>
        </div>
      )}

      {isLoading ? (
        <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="animate-pulse bg-white rounded-lg shadow-card p-6">
              <div className="flex items-center space-x-4">
                <div className="rounded-full bg-gray-200 h-12 w-12"></div>
                <div className="flex-1 space-y-2">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : medications.length === 0 ? (
        <Card className="text-center py-8">
          <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <Pill size={24} className="text-gray-400" />
          </div>
          <h2 className="text-xl font-medium text-gray-700 mb-2">No medications found</h2>
          <p className="text-gray-500 mb-6">Add your first medication to start tracking</p>
          <Link to="/medications/new">
            <Button leftIcon={<Plus size={16} />}>Add Medication</Button>
          </Link>
        </Card>
      ) : (
        <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          {medications.map((medication) => (
            <Card key={medication.medication_id} className="animate-fadeIn">
              <div className="flex items-start">
                <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center text-primary-600">
                  <Pill size={20} />
                </div>
                <div className="ml-4 flex-1">
                  <h3 className="font-medium text-lg">{medication.name}</h3>
                  <p className="text-gray-500">{medication.dosage}</p>
                  <div className="flex flex-wrap gap-2 mt-2 mb-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                      {medication.frequency}
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                      {medication.medication_type}
                    </span>
                  </div>
                  
                  <div className="border-t border-gray-100 pt-3 mt-2 flex space-x-2">
                    <Link to={`/medications/${medication.medication_id}`}>
                      <Button variant="outline" size="sm">View Details</Button>
                    </Link>
                    <Link to={`/medications/edit/${medication.medication_id}`}>
                      <Button variant="outline" size="sm" leftIcon={<Edit size={14} />}>Edit</Button>
                    </Link>
                    <Button 
                      variant="outline" 
                      size="sm" 
                      leftIcon={<Trash2 size={14} />}
                      onClick={() => handleDelete(medication.medication_id)}
                      className="text-error-600 hover:bg-error-50"
                    >
                      Delete
                    </Button>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default MedicationList;