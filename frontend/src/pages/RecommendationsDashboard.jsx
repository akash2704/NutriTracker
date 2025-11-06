import { useState, useEffect } from 'react';
import { Target, Clock, TrendingDown, Activity, Utensils, Dumbbell, Lightbulb, AlertCircle } from 'lucide-react';

const RecommendationsDashboard = () => {
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
            <span className="ml-4 text-lg text-gray-700">Generating your personalized plan...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-6">
        <div className="max-w-6xl mx-auto">
          <div className="bg-red-50 border border-red-200 rounded-xl p-8 text-center">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <p className="text-red-800 text-lg mb-4">Error: {error}</p>
            <button 
              onClick={fetchRecommendations}
              className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  const recs = recommendations.recommendations;
  const hasStructuredData = recs && !recs.error && !recs.raw_text;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-3">Your Weight Loss Plan</h1>
          <p className="text-gray-600 text-lg">Personalized recommendations based on your profile</p>
          {recommendations.preferences && (
            <div className="flex flex-wrap gap-2 mt-4">
              <span className="px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                {recommendations.preferences.dietary}
              </span>
              <span className="px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                {recommendations.preferences.budget} budget
              </span>
              <span className="px-4 py-2 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
                {recommendations.preferences.cuisine} cuisine
              </span>
            </div>
          )}
        </div>
        
        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center mb-3">
              <Target className="h-6 w-6 text-red-500 mr-3" />
              <h3 className="font-semibold text-gray-700">Current BMI</h3>
            </div>
            <div className="text-3xl font-bold text-red-600 mb-1">{recommendations.bmi}</div>
            <div className="text-sm text-gray-500">Overweight range</div>
          </div>
          
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center mb-3">
              <TrendingDown className="h-6 w-6 text-green-500 mr-3" />
              <h3 className="font-semibold text-gray-700">Target Calories</h3>
            </div>
            <div className="text-3xl font-bold text-green-600 mb-1">{recommendations.target_calories}</div>
            <div className="text-sm text-gray-500">Daily for weight loss</div>
          </div>
          
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center mb-3">
              <Clock className="h-6 w-6 text-blue-500 mr-3" />
              <h3 className="font-semibold text-gray-700">BMR</h3>
            </div>
            <div className="text-3xl font-bold text-blue-600 mb-1">{recommendations.bmr}</div>
            <div className="text-sm text-gray-500">Base metabolic rate</div>
          </div>
          
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center mb-3">
              <Activity className="h-6 w-6 text-purple-500 mr-3" />
              <h3 className="font-semibold text-gray-700">TDEE</h3>
            </div>
            <div className="text-3xl font-bold text-purple-600 mb-1">{recommendations.tdee}</div>
            <div className="text-sm text-gray-500">Total daily expenditure</div>
          </div>
        </div>

        {hasStructuredData ? (
          <>
            {/* Meal Plan & Macros */}
            <div className="grid md:grid-cols-2 gap-6 mb-6">
              {recs.calorie_breakdown && (
                <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
                  <div className="flex items-center mb-5">
                    <Utensils className="h-6 w-6 text-orange-500 mr-3" />
                    <h3 className="text-xl font-bold text-gray-900">Daily Meal Plan</h3>
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center p-4 bg-gradient-to-r from-orange-50 to-orange-100 rounded-lg">
                      <span className="font-semibold text-gray-700">Breakfast</span>
                      <span className="text-orange-700 font-bold text-lg">{recs.calorie_breakdown.breakfast}</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-lg">
                      <span className="font-semibold text-gray-700">Lunch</span>
                      <span className="text-green-700 font-bold text-lg">{recs.calorie_breakdown.lunch}</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg">
                      <span className="font-semibold text-gray-700">Dinner</span>
                      <span className="text-blue-700 font-bold text-lg">{recs.calorie_breakdown.dinner}</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg">
                      <span className="font-semibold text-gray-700">Snacks</span>
                      <span className="text-purple-700 font-bold text-lg">{recs.calorie_breakdown.snacks}</span>
                    </div>
                  </div>
                </div>
              )}

              {recs.macros && (
                <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
                  <div className="flex items-center mb-5">
                    <Target className="h-6 w-6 text-indigo-500 mr-3" />
                    <h3 className="text-xl font-bold text-gray-900">Macronutrients</h3>
                  </div>
                  <div className="space-y-3">
                    <div className="p-4 bg-gradient-to-r from-red-50 to-red-100 rounded-lg">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-semibold text-gray-700">Protein</span>
                        <span className="text-red-700 font-bold text-lg">{recs.macros.protein_grams}</span>
                      </div>
                      <p className="text-xs text-gray-600 mt-1">Muscle preservation</p>
                    </div>
                    <div className="p-4 bg-gradient-to-r from-yellow-50 to-yellow-100 rounded-lg">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-semibold text-gray-700">Carbs</span>
                        <span className="text-yellow-700 font-bold text-lg">{recs.macros.carbs_grams}</span>
                      </div>
                      <p className="text-xs text-gray-600 mt-1">Energy source</p>
                    </div>
                    <div className="p-4 bg-gradient-to-r from-indigo-50 to-indigo-100 rounded-lg">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-semibold text-gray-700">Fats</span>
                        <span className="text-indigo-700 font-bold text-lg">{recs.macros.fat_grams}</span>
                      </div>
                      <p className="text-xs text-gray-600 mt-1">Hormone production</p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Foods & Exercise */}
            <div className="grid md:grid-cols-2 gap-6 mb-6">
              {recs.foods && (
                <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
                  <div className="flex items-center mb-5">
                    <Utensils className="h-6 w-6 text-green-500 mr-3" />
                    <h3 className="text-xl font-bold text-gray-900">Recommended Foods</h3>
                  </div>
                  <div className="space-y-3">
                    {recs.foods.map((food, index) => (
                      <div key={index} className="flex items-start p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
                        <div className="w-2 h-2 bg-green-500 rounded-full mr-3 mt-2 flex-shrink-0"></div>
                        <span className="text-gray-700 leading-relaxed">{food}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {recs.exercise && (
                <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
                  <div className="flex items-center mb-5">
                    <Dumbbell className="h-6 w-6 text-blue-500 mr-3" />
                    <h3 className="text-xl font-bold text-gray-900">Exercise Plan</h3>
                  </div>
                  <div className="space-y-3">
                    {recs.exercise.map((exercise, index) => (
                      <div key={index} className="p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg">
                        <p className="text-gray-700 leading-relaxed">{exercise}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Weekly Goal */}
            {recs.weekly_goal && (
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 shadow-lg border border-green-200 mb-6">
                <div className="flex items-start">
                  <Target className="h-6 w-6 text-green-600 mr-3 mt-1 flex-shrink-0" />
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 mb-2">Weekly Goal</h3>
                    <p className="text-gray-700 leading-relaxed">{recs.weekly_goal}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Tips */}
            {recs.tips && (
              <div className="bg-gradient-to-r from-yellow-50 to-amber-50 rounded-xl p-6 shadow-lg border border-yellow-200">
                <div className="flex items-start mb-4">
                  <Lightbulb className="h-6 w-6 text-yellow-600 mr-3 mt-1 flex-shrink-0" />
                  <h3 className="text-xl font-bold text-gray-900">Pro Tips</h3>
                </div>
                <ul className="space-y-2">
                  {recs.tips.map((tip, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-yellow-600 mr-2">•</span>
                      <span className="text-gray-700">{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        ) : (
          <div className="bg-white rounded-xl p-8 shadow-lg border border-gray-100">
            <div className="flex items-start mb-4">
              <AlertCircle className="h-6 w-6 text-amber-500 mr-3 mt-1 flex-shrink-0" />
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">AI Recommendations</h3>
                {recs?.error ? (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-800">{recs.error}</p>
                  </div>
                ) : (
                  <div className="prose prose-sm max-w-none">
                    <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-lg">
                      {recs?.raw_text || JSON.stringify(recs, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecommendationsDashboard;