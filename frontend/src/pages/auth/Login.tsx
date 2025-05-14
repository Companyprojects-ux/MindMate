import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import Button from '../../components/ui/Button';
import FormInput from '../../components/ui/FormInput';
import Logo from '../../components/layout/Logo';
import { HeartPulse, Brain, Pill as Pills, BookHeart } from 'lucide-react';

type FormValues = {
  email: string;
  password: string;
};

const Login = () => {
  const { login, isLoading, error } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const [loginError, setLoginError] = useState<string | null>(null);

  const from = location.state?.from?.pathname || '/dashboard';

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>();

  const onSubmit = async (data: FormValues) => {
    try {
      await login(data.email, data.password);
      navigate(from, { replace: true });
    } catch (err) {
      setLoginError(err instanceof Error ? err.message : 'Failed to login');
    }
  };

  const features = [
    {
      icon: <HeartPulse className="w-6 h-6 text-rose-500" />,
      title: 'Comprehensive Health Tracking',
      description: 'Monitor your medications, mood, and overall well-being in one place.'
    },
    {
      icon: <Brain className="w-6 h-6 text-cyan-500" />,
      title: 'AI-Powered Support',
      description: 'Get personalized recommendations and insights from our advanced AI system.'
    },
    {
      icon: <Pills className="w-6 h-6 text-amber-500" />,
      title: 'Medication Management',
      description: 'Never miss a dose with our smart reminder system and medication tracker.'
    },
    {
      icon: <BookHeart className="w-6 h-6 text-emerald-500" />,
      title: 'Journal & Mood Tracking',
      description: 'Document your journey and track your emotional well-being over time.'
    }
  ];

  return (
    <div className="min-h-screen flex">
      {/* Left side - App information */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-indigo-700 to-purple-800 p-12 text-white">
        <div className="max-w-lg mx-auto">
          <div className="mb-12">
            <Logo className="h-12 w-auto" darkMode={true} />
          </div>
          
          <h1 className="text-4xl font-bold mb-6">Your Mental Health Companion</h1>
          <p className="text-lg mb-12 text-white/90">
            Take control of your mental health journey with MindMate+. 
            Our comprehensive platform helps you track, manage, and improve your well-being.
          </p>

          <div className="grid gap-8">
            {features.map((feature, index) => (
              <div key={index} className="flex items-start">
                <div className="p-2 bg-white/20 rounded-lg shadow-inner">
                  {feature.icon}
                </div>
                <div className="ml-4">
                  <h3 className="font-semibold text-lg">{feature.title}</h3>
                  <p className="text-white/80">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right side - Login form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="max-w-md w-full">
          <div className="text-center">
            <div className="lg:hidden flex justify-center mb-8">
              <Logo className="h-12 w-auto" darkMode={false} />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Welcome back</h2>
            <p className="mt-2 text-sm text-gray-600">
              Don't have an account?{' '}
              <Link to="/register" className="font-medium text-primary-600 hover:text-primary-500">
                Create one now
              </Link>
            </p>
          </div>

          <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
            {loginError && (
              <div className="bg-error-50 border border-error-200 text-error-700 px-4 py-3 rounded-md" role="alert">
                <p>{loginError}</p>
              </div>
            )}

            <FormInput
              id="email"
              label="Email address"
              type="email"
              autoComplete="email"
              {...register('email', {
                required: 'Email is required',
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: 'Invalid email address',
                },
              })}
              error={errors.email?.message}
            />

            <FormInput
              id="password"
              label="Password"
              type="password"
              autoComplete="current-password"
              {...register('password', {
                required: 'Password is required',
                minLength: {
                  value: 6,
                  message: 'Password must be at least 6 characters',
                },
              })}
              error={errors.password?.message}
            />

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                  Remember me
                </label>
              </div>
            </div>

            <Button
              type="submit"
              fullWidth
              isLoading={isLoading}
            >
              Sign in
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;