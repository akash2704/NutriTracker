import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { ChefHat, Zap, Plus } from 'lucide-react';
import api from '../services/api';

const Recipe = () => {
  const [ingredients, setIngredients] = useState([]);
  const [totalCalories, setTotalCalories] = useState(0);
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit, watch } = useForm();

  const recipeText = watch('recipe_text', '');

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      const response = await api.post('/recipe/parse', {
        recipe_text: data.recipe_text
      });
      setIngredients(response.data.ingredients);
      setTotalCalories(response.data.total_calories);
    } catch (error) {
      console.error('Failed to parse recipe:', error);
    } finally {
      setLoading(false);
    }
  };

  const logRecipe = async () => {
    // Log all ingredients as a meal
    for (const ingredient of ingredients) {
      if (ingredient.food_id) {
        try {
          await api.post('/food-logs/', {
            food_id: ingredient.food_id,
            quantity_grams: ingredient.grams,
            log_date: new Date().toISOString().split('T')[0],
            meal_type: 'Lunch'
          });
        } catch (error) {
          console.error('Failed to log ingredient:', error);
        }
      }
    }
    alert('Recipe logged successfully!');
  };

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-900">Recipe Parser</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <div className="card">
          <h3 className="text-base sm:text-lg font-semibold mb-4 flex items-center">
            <ChefHat size={20} className="mr-2" />
            Enter Recipe
          </h3>
          
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Recipe (Natural Language)
              </label>
              <textarea
                {...register('recipe_text', { required: true })}
                className="input-field h-32 sm:h-40 resize-none"
                placeholder="Example:
2 cups rice
1 tbsp oil
200g chicken
1 tsp salt
3 tomatoes"
              />
            </div>
            
            <button
              type="submit"
              disabled={loading || !recipeText.trim()}
              className="w-full btn-primary disabled:opacity-50 text-sm sm:text-base"
            >
              {loading ? 'Parsing...' : 'Parse Recipe'}
            </button>
          </form>
        </div>

        <div className="card">
          <h3 className="text-base sm:text-lg font-semibold mb-4 flex items-center">
            <Zap size={20} className="mr-2" />
            Parsed Ingredients
          </h3>
          
          {ingredients.length > 0 ? (
            <div className="space-y-4">
              <div className="bg-primary-50 p-3 sm:p-4 rounded-lg">
                <div className="text-lg sm:text-xl font-bold text-primary-600">
                  ~{Math.round(totalCalories)} calories
                </div>
                <div className="text-xs sm:text-sm text-primary-700">Estimated total</div>
              </div>
              
              <div className="space-y-2 max-h-48 sm:max-h-64 overflow-y-auto">
                {ingredients.map((ing, index) => (
                  <div key={index} className="border rounded-lg p-3">
                    <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2">
                      <div className="flex-1">
                        <h4 className="font-medium text-sm sm:text-base">{ing.ingredient}</h4>
                        <p className="text-xs sm:text-sm text-gray-600">
                          {ing.quantity} {ing.unit} ({Math.round(ing.grams)}g)
                        </p>
                      </div>
                      <div className="text-right">
                        {ing.food_name ? (
                          <span className="text-xs bg-success-100 text-success-800 px-2 py-1 rounded">
                            Found: {ing.food_name}
                          </span>
                        ) : (
                          <span className="text-xs bg-warning-100 text-warning-800 px-2 py-1 rounded">
                            Not found
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              <button
                onClick={logRecipe}
                className="w-full btn-primary flex items-center justify-center space-x-2 text-sm sm:text-base"
              >
                <Plus size={16} />
                <span>Log Recipe</span>
              </button>
            </div>
          ) : (
            <div className="text-center py-8 sm:py-12 text-gray-500">
              <ChefHat size={32} sm:size={48} className="mx-auto mb-4 text-gray-300" />
              <p className="text-sm sm:text-base">Enter a recipe to see parsed ingredients</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Recipe;
