import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useSearchParams } from 'react-router-dom';
import { foodAPI, logAPI } from '../services/api';
import { Search, Plus, Check } from 'lucide-react';

const LogFood = () => {
  const [searchParams] = useSearchParams();
  const [foods, setFoods] = useState([]);
  const [selectedFood, setSelectedFood] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const { register, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      log_date: new Date().toISOString().split('T')[0],
      meal_type: 'Lunch',
      quantity_grams: 100
    }
  });

  useEffect(() => {
    const foodId = searchParams.get('foodId');
    if (foodId) {
      loadFoodById(foodId);
    }
  }, [searchParams]);

  useEffect(() => {
    if (searchQuery.trim()) {
      searchFoods();
    }
  }, [searchQuery]);

  const loadFoodById = async (foodId) => {
    try {
      const response = await foodAPI.getFood(foodId);
      setSelectedFood(response.data);
    } catch (error) {
      console.error('Failed to load food:', error);
    }
  };

  const searchFoods = async () => {
    setLoading(true);
    try {
      const response = await foodAPI.searchFoods(searchQuery, 10);
      setFoods(response.data);
    } catch (error) {
      console.error('Failed to search foods:', error);
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = async (data) => {
    if (!selectedFood) return;
    
    setLoading(true);
    try {
      await logAPI.createLog({
        ...data,
        food_id: selectedFood.id,
        quantity_grams: parseFloat(data.quantity_grams)
      });
      setSuccess(true);
      reset();
      setSelectedFood(null);
      setTimeout(() => setSuccess(false), 3000);
    } catch (error) {
      console.error('Failed to log food:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Log Food</h1>
      </div>

      {success && (
        <div className="bg-success-50 border border-success-200 text-success-600 px-4 py-3 rounded-lg flex items-center">
          <Check size={20} className="mr-2" />
          Food logged successfully!
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Search & Select Food</h3>
          
          <div className="space-y-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search for foods..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="input-field pl-10"
              />
            </div>

            {selectedFood && (
              <div className="p-3 bg-primary-50 border border-primary-200 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium text-primary-900">{selectedFood.name}</h4>
                    <p className="text-sm text-primary-700">{selectedFood.category.name}</p>
                  </div>
                  <Check size={20} className="text-primary-600" />
                </div>
              </div>
            )}

            {searchQuery && (
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {loading ? (
                  <div className="flex items-center justify-center h-16">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
                  </div>
                ) : (
                  foods.map((food) => (
                    <div
                      key={food.id}
                      onClick={() => setSelectedFood(food)}
                      className="p-3 rounded-lg border border-gray-200 hover:border-gray-300 hover:bg-gray-50 cursor-pointer"
                    >
                      <h4 className="font-medium text-gray-900">{food.name}</h4>
                      <p className="text-sm text-gray-600">{food.category.name}</p>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Log Details</h3>
          
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Date</label>
              <input
                {...register('log_date', { required: 'Date is required' })}
                type="date"
                className="input-field mt-1"
              />
              {errors.log_date && <p className="mt-1 text-sm text-danger-600">{errors.log_date.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Meal Type</label>
              <select
                {...register('meal_type', { required: 'Meal type is required' })}
                className="input-field mt-1"
              >
                <option value="Breakfast">Breakfast</option>
                <option value="Lunch">Lunch</option>
                <option value="Dinner">Dinner</option>
                <option value="Snack">Snack</option>
              </select>
              {errors.meal_type && <p className="mt-1 text-sm text-danger-600">{errors.meal_type.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Quantity (grams)</label>
              <input
                {...register('quantity_grams', { 
                  required: 'Quantity is required',
                  min: { value: 1, message: 'Quantity must be at least 1 gram' }
                })}
                type="number"
                step="0.1"
                className="input-field mt-1"
                placeholder="100"
              />
              {errors.quantity_grams && <p className="mt-1 text-sm text-danger-600">{errors.quantity_grams.message}</p>}
            </div>

            <button
              type="submit"
              disabled={!selectedFood || loading}
              className="w-full btn-primary disabled:opacity-50"
            >
              {loading ? 'Logging...' : 'Log Food'}
            </button>

            {!selectedFood && (
              <p className="text-sm text-gray-500 text-center">
                Please select a food item first
              </p>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};

export default LogFood;
