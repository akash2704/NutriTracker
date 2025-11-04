import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { authAPI } from '../services/api';
import { Eye, EyeOff } from 'lucide-react';

const Register = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [otpInput, setOtpInput] = useState('');
  const [showVerification, setShowVerification] = useState(false);
  const [email, setEmail] = useState('');
  const [showOtp, setShowOtp] = useState('');
  const navigate = useNavigate();
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = async (data) => {
    setLoading(true);
    setError('');
    try {
      const response = await authAPI.register(data);
      console.log('Registration response:', response.data);
      setEmail(data.email);
      setShowOtp(response.data.otp || '');
      setShowVerification(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const handleVerification = async () => {
    setLoading(true);
    try {
      await authAPI.verify({ email, otp: otpInput });
      navigate('/login');
    } catch (err) {
      setError('Invalid or expired OTP');
    } finally {
      setLoading(false);
    }
  };

  if (showVerification) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Verify your account
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              {showOtp ? (
                <>We've sent an OTP to your email. For demo purposes, your OTP is: <strong>{showOtp}</strong></>
              ) : (
                <>We've sent an OTP to your email. Please check your inbox and enter it below.</>
              )}
            </p>
          </div>
          <div className="mt-8 space-y-6">
            {error && (
              <div className="bg-danger-50 border border-danger-200 text-danger-600 px-4 py-3 rounded-lg">
                {error}
              </div>
            )}
            <div>
              <label className="block text-sm font-medium text-gray-700">Enter OTP</label>
              <input
                type="text"
                value={otpInput}
                onChange={(e) => setOtpInput(e.target.value)}
                className="input-field mt-1"
                placeholder="Enter 6-digit OTP"
                maxLength="6"
              />
            </div>
            <button
              onClick={handleVerification}
              disabled={loading || !otpInput}
              className="w-full btn-primary disabled:opacity-50"
            >
              {loading ? 'Verifying...' : 'Verify Account'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Or{' '}
            <Link to="/login" className="font-medium text-primary-600 hover:text-primary-500">
              sign in to your existing account
            </Link>
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          {error && (
            <div className="bg-danger-50 border border-danger-200 text-danger-600 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">First Name</label>
              <input
                {...register('first_name', { required: 'First name is required' })}
                className="input-field mt-1"
                placeholder="First name"
              />
              {errors.first_name && <p className="mt-1 text-sm text-danger-600">{errors.first_name.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Last Name</label>
              <input
                {...register('last_name', { required: 'Last name is required' })}
                className="input-field mt-1"
                placeholder="Last name"
              />
              {errors.last_name && <p className="mt-1 text-sm text-danger-600">{errors.last_name.message}</p>}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              {...register('email', { required: 'Email is required', pattern: { value: /^\S+@\S+$/i, message: 'Invalid email' } })}
              type="email"
              className="input-field mt-1"
              placeholder="Enter your email"
            />
            {errors.email && <p className="mt-1 text-sm text-danger-600">{errors.email.message}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <div className="relative mt-1">
              <input
                {...register('password', { required: 'Password is required', minLength: { value: 6, message: 'Password must be at least 6 characters' } })}
                type={showPassword ? 'text' : 'password'}
                className="input-field pr-10"
                placeholder="Enter your password"
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
            {errors.password && <p className="mt-1 text-sm text-danger-600">{errors.password.message}</p>}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary disabled:opacity-50"
          >
            {loading ? 'Creating account...' : 'Create account'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;
