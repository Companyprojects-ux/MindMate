import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import Button from '../../components/ui/Button';
import FormInput from '../../components/ui/FormInput';
import Logo from '../../components/layout/Logo';

type FormValues = {
  email: string;
  password: string;
};

const Login = () => {
  const { login, isLoading, error } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const [loginError, setLoginError] = useState<string | null>(null);

  // Get the location user was trying to access
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

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-6 md:p-8 rounded-xl shadow-card">
        <div className="text-center">
          <div className="flex justify-center">
            <Logo className="h-12 w-auto" />
          </div>
          <h2 className="mt-6 text-2xl font-bold text-gray-900">Sign in to your account</h2>
          <p className="mt-2 text-sm text-gray-600">
            Or{' '}
            <Link to="/register" className="font-medium text-primary-600 hover:text-primary-500">
              create a new account
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
  );
};

export default Login;