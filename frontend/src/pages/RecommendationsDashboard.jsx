import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Target, Clock, TrendingDown, Activity } from 'lucide-react';

const RecommendationsDashboard = () => {
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { user } = useAuth();

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      const token = localStorage.getItem('token');
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ;
      const response = await fetch(`${API_BASE_URL}/recommendations/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }

      const data = await response.json();
      setRecommendations(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const parseRecommendations = (text) => {
    try {
      // Clean the text and extract JSON
      const jsonMatch = text.match(/```json\s*([\s\S]*?)\s*```/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[1]);
      }
      // Try to parse directly
      return JSON.parse(text);
    } catch {
      // If not JSON, return as formatted text
      return { text: text };
    }
  };

  if (loading) {
    return (
      <div className="recommendations-dashboard">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Generating your personalized recommendations...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="recommendations-dashboard">
        <div className="error text-center py-12">
          <p className="text-red-600 text-lg">Error: {error}</p>
          <button 
            onClick={fetchRecommendations}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const parsedRecs = parseRecommendations(recommendations.recommendations);

  return (
    <div className="recommendations-dashboard">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Weight Loss Plan</h1>
        <p className="text-gray-600">Personalized recommendations based on your profile</p>
        {recommendations.preferences && (
          <div className="flex gap-2 mt-3">
            <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
              {recommendations.preferences.dietary}
            </span>
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
              {recommendations.preferences.budget} budget
            </span>
            <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
              {recommendations.preferences.cuisine} cuisine
            </span>
          </div>
        )}
      </div>
      
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="flex items-center mb-2">
            <Target className="h-5 w-5 text-red-500 mr-2" />
            <h3>Current BMI</h3>
          </div>
          <div className="metric-value text-red-600">{recommendations.bmi}</div>
          <div className="metric-label">Overweight</div>
        </div>
        
        <div className="metric-card">
          <div className="flex items-center mb-2">
            <TrendingDown className="h-5 w-5 text-green-500 mr-2" />
            <h3>Target Calories</h3>
          </div>
          <div className="metric-value text-green-600">{recommendations.target_calories}</div>
          <div className="metric-label">Daily for weight loss</div>
        </div>
        
        <div className="metric-card">
          <div className="flex items-center mb-2">
            <Clock className="h-5 w-5 text-blue-500 mr-2" />
            <h3>BMR</h3>
          </div>
          <div className="metric-value text-blue-600">{recommendations.bmr}</div>
          <div className="metric-label">Base metabolic rate</div>
        </div>
        
        <div className="metric-card">
          <div className="flex items-center mb-2">
            <Activity className="h-5 w-5 text-purple-500 mr-2" />
            <h3>TDEE</h3>
          </div>
          <div className="metric-value text-purple-600">{recommendations.tdee}</div>
          <div className="metric-label">Total daily expenditure</div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6 mt-8">
        {parsedRecs.calorie_breakdown && (
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h3 className="text-lg font-semibold mb-4 text-gray-900">Daily Meal Plan</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-orange-50 rounded-lg">
                <span className="font-medium">Breakfast</span>
                <span className="text-orange-600 font-semibold">{parsedRecs.calorie_breakdown.breakfast}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                <span className="font-medium">Lunch</span>
                <span className="text-green-600 font-semibold">{parsedRecs.calorie_breakdown.lunch}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                <span className="font-medium">Dinner</span>
                <span className="text-blue-600 font-semibold">{parsedRecs.calorie_breakdown.dinner}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
                <span className="font-medium">Snacks</span>
                <span className="text-purple-600 font-semibold">{parsedRecs.calorie_breakdown.snacks}</span>
              </div>
            </div>
          </div>
        )}

        {parsedRecs.macros && (
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h3 className="text-lg font-semibold mb-4 text-gray-900">Macronutrients</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-red-50 rounded-lg">
                <span className="font-medium">Protein</span>
                <span className="text-red-600 font-semibold">{parsedRecs.macros.protein_grams}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-yellow-50 rounded-lg">
                <span className="font-medium">Carbs</span>
                <span className="text-yellow-600 font-semibold">{parsedRecs.macros.carbs_grams}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-indigo-50 rounded-lg">
                <span className="font-medium">Fats</span>
                <span className="text-indigo-600 font-semibold">{parsedRecs.macros.fat_grams}</span>
              </div>
            </div>
          </div>
        )}

        {parsedRecs.foods && (
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h3 className="text-lg font-semibold mb-4 text-gray-900">Recommended Foods</h3>
            <div className="space-y-2">
              {parsedRecs.foods.map((food, index) => (
                <div key={index} className="flex items-center p-2 bg-gray-50 rounded-lg">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                  <span className="text-gray-700">{food}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {parsedRecs.exercise && (
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h3 className="text-lg font-semibold mb-4 text-gray-900">Exercise Plan</h3>
            <div className="space-y-3">
              {parsedRecs.exercise.map((exercise, index) => (
                <div key={index} className="p-3 bg-blue-50 rounded-lg">
                  <p className="text-gray-700 text-sm leading-relaxed">{exercise}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {parsedRecs.weekly_goal && (
        <div className="mt-6 bg-gradient-to-r from-green-50 to-blue-50 rounded-xl p-6 border border-green-200">
          <h3 className="text-lg font-semibold mb-2 text-gray-900">Weekly Goal</h3>
          <p className="text-gray-700">{parsedRecs.weekly_goal}</p>
        </div>
      )}

      {parsedRecs.text && (
        <div className="mt-6 bg-white rounded-xl p-6 shadow-sm border">
          <h3 className="text-lg font-semibold mb-4 text-gray-900">AI Recommendations</h3>
          <div className="prose prose-sm max-w-none">
            <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed">
              {parsedRecs.text}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecommendationsDashboard;
