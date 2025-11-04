import { useState, useEffect } from 'react';
import { foodAPI } from '../services/api';
import { Search, Plus } from 'lucide-react';

const Foods = () => {
  const [foods, setFoods] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedFood, setSelectedFood] = useState(null);

  useEffect(() => {
    if (searchQuery.trim()) {
      searchFoods();
    } else {
      loadFoods();
    }
  }, [searchQuery]);

  const loadFoods = async () => {
    setLoading(true);
    try {
      const response = await foodAPI.getFoods(0, 20);
      setFoods(response.data);
    } catch (error) {
      console.error('Failed to load foods:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchFoods = async () => {
    setLoading(true);
    try {
      const response = await foodAPI.searchFoods(searchQuery, 20);
      setFoods(response.data);
    } catch (error) {
      console.error('Failed to search foods:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFoodSelect = (food) => {
    setSelectedFood(food);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Food Database</h1>
      </div>

      <div className="card">
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
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">
            {searchQuery ? `Search Results (${foods.length})` : `All Foods (${foods.length})`}
          </h3>
          
          {loading ? (
            <div className="flex items-center justify-center h-32">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
            </div>
          ) : (
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {foods.map((food) => (
                <div
                  key={food.id}
                  onClick={() => handleFoodSelect(food)}
                  className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                    selectedFood?.id === food.id
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <h4 className="font-medium text-gray-900">{food.name}</h4>
                      <p className="text-sm text-gray-600">{food.category.name}</p>
                    </div>
                    <Plus size={16} className="text-gray-400" />
                  </div>
                </div>
              ))}
              {foods.length === 0 && !loading && (
                <p className="text-center text-gray-500 py-8">
                  {searchQuery ? 'No foods found matching your search.' : 'No foods available.'}
                </p>
              )}
            </div>
          )}
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Food Details</h3>
          {selectedFood ? (
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-gray-900">{selectedFood.name}</h4>
                <p className="text-sm text-gray-600">{selectedFood.category.name}</p>
              </div>
              
              <div className="border-t pt-4">
                <p className="text-sm text-gray-600 mb-2">Food ID: {selectedFood.id}</p>
                <p className="text-sm text-gray-600">Category ID: {selectedFood.category_id}</p>
              </div>

              <div className="border-t pt-4">
                <button
                  onClick={() => {
                    // Navigate to log page with pre-selected food
                    window.location.href = `/log?foodId=${selectedFood.id}`;
                  }}
                  className="btn-primary w-full"
                >
                  Log This Food
                </button>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              <Search size={48} className="mx-auto mb-4 text-gray-300" />
              <p>Select a food item to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Foods;
