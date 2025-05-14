import { HeartPulse } from 'lucide-react';

interface LogoProps {
  className?: string;
}

const Logo: React.FC<LogoProps> = ({ className = 'h-8 w-auto' }) => {
  return (
    <div className="flex items-center">
      <HeartPulse className="text-primary-600" size={24} />
      <div className="ml-2 font-bold text-xl text-primary-800">
        <span>Mind</span>
        <span className="text-secondary-600">Mate+</span>
      </div>
    </div>
  );
};

export default Logo;