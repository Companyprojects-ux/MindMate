import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import Button from '../../components/ui/Button';
import FormInput from '../../components/ui/FormInput';
import Logo from '../../components/layout/Logo';
import { Shield, Lock, UserCheck, Bell } from 'lucide-react';

type FormValues = {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
};

const Register = () => {
  const { register: registerUser, isLoading } = useAuthStore();
  const navigate = useNavigate();
  const [registerError, setRegisterError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<FormValues>();

  const password = watch('password');

  const onSubmit = async (data: FormValues) => {
    try {
      await registerUser(data.name, data.email, data.password);
      navigate('/dashboard', { replace: true });
    } catch (err) {
      setRegisterError(err instanceof Error ? err.message : 'Failed to register');
    }
  };

  const benefits = [
    {
      icon: <Shield className="w-6 h-6 text-rose-500" />,
      title: 'Secure & Private',
      description: 'Your health data is encrypted and protected with the highest security standards.'
    },
    {
      icon: <Lock className="w-6 h-6 text-cyan-500" />,
      title: 'HIPAA Compliant',
      description: 'We follow strict healthcare privacy guidelines to protect your information.'
    },
    {
      icon: <UserCheck className="w-6 h-6 text-amber-500" />,
      title: 'Personalized Care',
      description: 'Get customized recommendations based on your unique health journey.'
    },
    {
      icon: <Bell className="w-6 h-6 text-emerald-500" />,
      title: 'Smart Reminders',
      description: 'Stay on track with intelligent notifications and reminders.'
    }
  ];

  return (
    <div className="min-h-screen flex">
      {/* Left side - Registration form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="max-w-md w-full">
          <div className="text-center">
            <div className="lg:hidden flex justify-center mb-8">
              <Logo className="h-12 w-auto" darkMode={false} />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Create your account</h2>
            <p className="mt-2 text-sm text-gray-600">
              Already have an account?{' '}
              <Link to="/login" className="font-medium text-primary-600 hover:text-primary-500">
                Sign in instead
              </Link>
            </p>
          </div>

          <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
            {registerError && (
              <div className="bg-error-50 border border-error-200 text-error-700 px-4 py-3 rounded-md" role="alert">
                <p>{registerError}</p>
              </div>
            )}

            <FormInput
              id="name"
              label="Full name"
              type="text"
              autoComplete="name"
              {...register('name', {
                required: 'Name is required',
                minLength: {
                  value: 2,
                  message: 'Name must be at least 2 characters',
                },
              })}
              error={errors.name?.message}
            />

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
              autoComplete="new-password"
              {...register('password', {
                required: 'Password is required',
                minLength: {
                  value: 6,
                  message: 'Password must be at least 6 characters',
                },
              })}
              error={errors.password?.message}
            />

            <FormInput
              id="confirmPassword"
              label="Confirm password"
              type="password"
              autoComplete="new-password"
              {...register('confirmPassword', {
                required: 'Please confirm your password',
                validate: (value) => value === password || 'Passwords do not match',
              })}
              error={errors.confirmPassword?.message}
            />

            <Button
              type="submit"
              fullWidth
              isLoading={isLoading}
            >
              Create account
            </Button>
          </form>
        </div>
      </div>

      {/* Right side - App benefits */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-purple-800 to-indigo-700 p-12 text-white">
        <div className="max-w-lg mx-auto">
          <div className="mb-12">
            <Logo className="h-12 w-auto" darkMode={true} />
          </div>

          <h1 className="text-4xl font-bold mb-6">Join MindMate+ Today</h1>
          <p className="text-lg mb-12 text-white/90">
            Start your journey to better mental health with our comprehensive platform. 
            Join thousands of users who trust MindMate+ for their mental wellness needs.
          </p>

          <div className="grid gap-8">
            {benefits.map((benefit, index) => (
              <div key={index} className="flex items-start">
                <div className="p-2 bg-white/20 rounded-lg shadow-inner">
                  {benefit.icon}
                </div>
                <div className="ml-4">
                  <h3 className="font-semibold text-lg">{benefit.title}</h3>
                  <p className="text-white/80">{benefit.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;