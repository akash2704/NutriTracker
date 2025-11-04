import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { userAPI } from '../services/api';
import { User, Save, Edit } from 'lucide-react';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [success, setSuccess] = useState(false);
  const { register, handleSubmit, reset, formState: { errors } } = useForm();

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    setLoading(true);
    try {
      const response = await userAPI.getUserProfile();
      setProfile(response.data);
      reset(response.data);
      setEditing(false);
    } catch (error) {
      if (error.response?.status === 404) {
        setEditing(true);
      }
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      const response = await userAPI.createProfile({
        ...data,
        height_cm: parseFloat(data.height_cm),
        weight_kg: parseFloat(data.weight_kg)
      });
      setProfile(response.data);
      setSuccess(true);
      setEditing(false);
      setTimeout(() => setSuccess(false), 3000);
    } catch (error) {
      console.error('Failed to save profile:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !profile) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Profile</h1>
        {profile && !editing && (
          <button
            onClick={() => setEditing(true)}
            className="btn-secondary flex items-center space-x-2"
          >
            <Edit size={16} />
            <span>Edit Profile</span>
          </button>
        )}
      </div>

      {success && (
        <div className="bg-success-50 border border-success-200 text-success-600 px-4 py-3 rounded-lg">
          Profile saved successfully!
        </div>
      )}

      <div className="card">
        {!profile || editing ? (
          <div>
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <User size={20} className="mr-2" />
              {profile ? 'Edit Profile' : 'Create Your Profile'}
            </h3>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Birth Date</label>
                <input
                  {...register('birth_date', { required: 'Birth date is required' })}
                  type="date"
                  className="input-field mt-1"
                />
                {errors.birth_date && <p className="mt-1 text-sm text-danger-600">{errors.birth_date.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Gender</label>
                <select
                  {...register('gender', { required: 'Gender is required' })}
                  className="input-field mt-1"
                >
                  <option value="">Select gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
                {errors.gender && <p className="mt-1 text-sm text-danger-600">{errors.gender.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Activity Level</label>
                <select
                  {...register('activity_level', { required: 'Activity level is required' })}
                  className="input-field mt-1"
                >
                  <option value="">Select activity level</option>
                  <option value="sedentary">Sedentary</option>
                  <option value="moderate">Moderate</option>
                  <option value="heavy">Heavy</option>
                  <option value="pregnant">Pregnant</option>
                  <option value="lactating_0-6">Lactating (0-6 months)</option>
                  <option value="lactating_6-12">Lactating (6-12 months)</option>
                </select>
                {errors.activity_level && <p className="mt-1 text-sm text-danger-600">{errors.activity_level.message}</p>}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Height (cm)</label>
                  <input
                    {...register('height_cm', { 
                      required: 'Height is required',
                      min: { value: 50, message: 'Height must be at least 50 cm' },
                      max: { value: 300, message: 'Height must be less than 300 cm' }
                    })}
                    type="number"
                    step="0.1"
                    className="input-field mt-1"
                    placeholder="175"
                  />
                  {errors.height_cm && <p className="mt-1 text-sm text-danger-600">{errors.height_cm.message}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Weight (kg)</label>
                  <input
                    {...register('weight_kg', { 
                      required: 'Weight is required',
                      min: { value: 20, message: 'Weight must be at least 20 kg' },
                      max: { value: 500, message: 'Weight must be less than 500 kg' }
                    })}
                    type="number"
                    step="0.1"
                    className="input-field mt-1"
                    placeholder="70"
                  />
                  {errors.weight_kg && <p className="mt-1 text-sm text-danger-600">{errors.weight_kg.message}</p>}
                </div>
              </div>

              <div className="border-t pt-4">
                <h4 className="text-md font-medium text-gray-900 mb-3">Dietary Preferences</h4>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">Dietary Preference</label>
                  <select
                    {...register('dietary_preference')}
                    className="input-field mt-1"
                  >
                    <option value="">Select preference</option>
                    <option value="vegetarian">Vegetarian</option>
                    <option value="non-vegetarian">Non-Vegetarian</option>
                    <option value="vegan">Vegan</option>
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Budget Range</label>
                    <select
                      {...register('budget_range')}
                      className="input-field mt-1"
                    >
                      <option value="">Select budget</option>
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">Preferred Cuisine</label>
                    <select
                      {...register('preferred_cuisine')}
                      className="input-field mt-1"
                    >
                      <option value="">Select cuisine</option>
                      <option value="indian">Indian</option>
                      <option value="continental">Continental</option>
                      <option value="mixed">Mixed</option>
                    </select>
                  </div>
                </div>
              </div>

              <div className="flex space-x-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary flex items-center space-x-2 disabled:opacity-50"
                >
                  <Save size={16} />
                  <span>{loading ? 'Saving...' : 'Save Profile'}</span>
                </button>
                {profile && (
                  <button
                    type="button"
                    onClick={() => {
                      setEditing(false);
                      reset(profile);
                    }}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                )}
              </div>
            </form>
          </div>
        ) : (
          <div>
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <User size={20} className="mr-2" />
              Your Profile
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Birth Date</label>
                  <p className="mt-1 text-gray-900">{profile.birth_date}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Gender</label>
                  <p className="mt-1 text-gray-900 capitalize">{profile.gender}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Activity Level</label>
                  <p className="mt-1 text-gray-900 capitalize">{profile.activity_level.replace('_', ' ')}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Dietary Preference</label>
                  <p className="mt-1 text-gray-900 capitalize">{profile.dietary_preference || 'Not specified'}</p>
                </div>
              </div>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Height</label>
                  <p className="mt-1 text-gray-900">{profile.height_cm} cm</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Weight</label>
                  <p className="mt-1 text-gray-900">{profile.weight_kg} kg</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">BMI</label>
                  <p className="mt-1 text-gray-900">
                    {((profile.weight_kg / (profile.height_cm / 100) ** 2)).toFixed(1)}
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Budget & Cuisine</label>
                  <p className="mt-1 text-gray-900 capitalize">
                    {profile.budget_range || 'Not specified'} • {profile.preferred_cuisine || 'Not specified'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;
