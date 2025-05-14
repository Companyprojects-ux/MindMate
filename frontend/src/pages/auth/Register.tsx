import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import Button from '../../components/ui/Button';
import FormInput from '../../components/ui/FormInput';
import Logo from '../../components/layout/Logo';

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

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-6 md:p-8 rounded-xl shadow-card">
        <div className="text-center">
          <div className="flex justify-center">
            <Logo className="h-12 w-auto" />
          </div>
          <h2 className="mt-6 text-2xl font-bold text-gray-900">Create a new account</h2>
          <p className="mt-2 text-sm text-gray-600">
            Or{' '}
            <Link to="/login" className="font-medium text-primary-600 hover:text-primary-500">
              sign in to your existing account
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
  );
};

export default Register;