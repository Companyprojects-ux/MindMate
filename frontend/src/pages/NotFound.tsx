import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import Button from '../components/ui/Button';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
        <h2 className="text-2xl font-medium text-gray-700 mb-6">Page not found</h2>
        <p className="text-gray-600 mb-8">
          The page you are looking for doesn't exist or has been moved.
        </p>
        <Button 
          onClick={() => navigate(-1)} 
          leftIcon={<ArrowLeft size={16} />}
        >
          Go back
        </Button>
      </div>
    </div>
  );
};

export default NotFound;