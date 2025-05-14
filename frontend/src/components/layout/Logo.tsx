import { HeartPulse } from 'lucide-react';

interface LogoProps {
  className?: string;
  darkMode?: boolean;
}

const Logo: React.FC<LogoProps> = ({ className = 'h-8 w-auto', darkMode = false }) => {
  return (
    <div className="flex items-center">
      <HeartPulse className="text-rose-500" size={24} />
      <div className="ml-2 font-bold text-xl">
        <span className={darkMode ? 'text-white' : 'text-gray-800'}>Mind</span>
        <span className="text-amber-500">Mate+</span>
      </div>
    </div>
  );
};

export default Logo;