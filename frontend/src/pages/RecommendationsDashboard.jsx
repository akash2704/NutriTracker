import { useState, useEffect } from 'react';
import { Target, Clock, TrendingDown, Activity, Utensils, Dumbbell, Lightbulb, AlertCircle, Heart } from 'lucide-react';

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
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
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
      console.log('Recommendations data:', data); // Debug log
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

  const recs = recommendations?.recommendations;
  const hasError = recs?.error;
  const hasValidData = recs && !hasError && (recs.greeting || recs.meal_plan);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-3">Your Weight Loss Plan</h1>
          <p className="text-gray-600 text-lg">Personalized recommendations based on your profile</p>
          {recommendations?.preferences && (
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
            <div className="text-3xl font-bold text-red-600 mb-1">{recommendations?.bmi || 'N/A'}</div>
            <div className="text-sm text-gray-500">{recommendations?.bmi_category || 'Calculate required'}</div>
          </div>
          
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center mb-3">
              <TrendingDown className="h-6 w-6 text-green-500 mr-3" />
              <h3 className="font-semibold text-gray-700">Target Calories</h3>
            </div>
            <div className="text-3xl font-bold text-green-600 mb-1">{recommendations?.target_calories || 'N/A'}</div>
            <div className="text-sm text-gray-500">Daily for weight loss</div>
          </div>
          
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center mb-3">
              <Clock className="h-6 w-6 text-blue-500 mr-3" />
              <h3 className="font-semibold text-gray-700">BMR</h3>
            </div>
            <div className="text-3xl font-bold text-blue-600 mb-1">{recommendations?.bmr || 'N/A'}</div>
            <div className="text-sm text-gray-500">Base metabolic rate</div>
          </div>
          
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center mb-3">
              <Activity className="h-6 w-6 text-purple-500 mr-3" />
              <h3 className="font-semibold text-gray-700">TDEE</h3>
            </div>
            <div className="text-3xl font-bold text-purple-600 mb-1">{recommendations?.tdee || 'N/A'}</div>
            <div className="text-sm text-gray-500">Total daily expenditure</div>
          </div>
        </div>

        {hasValidData ? (
          <>
            {/* Greeting */}
            {recs.greeting && (
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 shadow-lg border border-blue-200 mb-6">
                <div className="flex items-start">
                  <Heart className="h-6 w-6 text-blue-600 mr-3 mt-1 flex-shrink-0" />
                  <p className="text-gray-800 text-lg leading-relaxed">{recs.greeting}</p>
                </div>
              </div>
            )}

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

            {/* Meal Plan */}
            {recs.meal_plan && (
              <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 mb-6">
                <div className="flex items-center mb-5">
                  <Utensils className="h-6 w-6 text-orange-500 mr-3" />
                  <h3 className="text-xl font-bold text-gray-900">Today's Meal Plan</h3>
                </div>
                <div className="grid md:grid-cols-2 gap-4">
                  {recs.meal_plan.breakfast && (
                    <div className="p-4 bg-gradient-to-r from-orange-50 to-orange-100 rounded-lg">
                      <h4 className="font-semibold text-gray-800 mb-2">🌅 Breakfast</h4>
                      <p className="text-gray-700 text-sm leading-relaxed">{recs.meal_plan.breakfast}</p>
                    </div>
                  )}
                  {recs.meal_plan.lunch && (
                    <div className="p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-lg">
                      <h4 className="font-semibold text-gray-800 mb-2">☀️ Lunch</h4>
                      <p className="text-gray-700 text-sm leading-relaxed">{recs.meal_plan.lunch}</p>
                    </div>
                  )}
                  {recs.meal_plan.dinner && (
                    <div className="p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg">
                      <h4 className="font-semibold text-gray-800 mb-2">🌙 Dinner</h4>
                      <p className="text-gray-700 text-sm leading-relaxed">{recs.meal_plan.dinner}</p>
                    </div>
                  )}
                  {recs.meal_plan.snack && (
                    <div className="p-4 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg">
                      <h4 className="font-semibold text-gray-800 mb-2">🍎 Snack</h4>
                      <p className="text-gray-700 text-sm leading-relaxed">{recs.meal_plan.snack}</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Exercise Plan */}
            {recs.exercise_plan && Array.isArray(recs.exercise_plan) && (
              <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 mb-6">
                <div className="flex items-center mb-5">
                  <Dumbbell className="h-6 w-6 text-blue-500 mr-3" />
                  <h3 className="text-xl font-bold text-gray-900">Exercise Plan</h3>
                </div>
                <div className="space-y-3">
                  {recs.exercise_plan.map((exercise, index) => (
                    <div key={index} className="p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg flex items-start">
                      <span className="text-blue-600 font-bold mr-3">{index + 1}.</span>
                      <p className="text-gray-700 leading-relaxed">{exercise}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Pro Tips */}
            {recs.pro_tips && Array.isArray(recs.pro_tips) && (
              <div className="bg-gradient-to-r from-yellow-50 to-amber-50 rounded-xl p-6 shadow-lg border border-yellow-200">
                <div className="flex items-start mb-4">
                  <Lightbulb className="h-6 w-6 text-yellow-600 mr-3 mt-1 flex-shrink-0" />
                  <h3 className="text-xl font-bold text-gray-900">Pro Tips</h3>
                </div>
                <ul className="space-y-3">
                  {recs.pro_tips.map((tip, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-yellow-600 mr-3 text-xl">•</span>
                      <span className="text-gray-700 leading-relaxed">{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Fallback Plan (if present) */}
            {recs.fallback_plan && (
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-6 mt-6">
                <div className="flex items-start mb-4">
                  <AlertCircle className="h-6 w-6 text-amber-600 mr-3 mt-1 flex-shrink-0" />
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 mb-2">Basic Plan (Fallback)</h3>
                    <p className="text-sm text-gray-600 mb-4">AI service had an issue, here's a basic plan to get started:</p>
                    <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed bg-white p-4 rounded-lg text-sm">
                      {JSON.stringify(recs.fallback_plan, null, 2)}
                    </pre>
                  </div>
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="bg-white rounded-xl p-8 shadow-lg border border-gray-100">
            <div className="flex items-start mb-4">
              <AlertCircle className="h-6 w-6 text-amber-500 mr-3 mt-1 flex-shrink-0" />
              <div className="flex-1">
                <h3 className="text-xl font-bold text-gray-900 mb-3">Unable to Load Recommendations</h3>
                {hasError ? (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-800 mb-2">{recs.error}</p>
                    {recs.raw_text && (
                      <details className="mt-3">
                        <summary className="cursor-pointer text-sm text-red-700 hover:text-red-900">
                          Show raw response
                        </summary>
                        <pre className="mt-2 whitespace-pre-wrap font-mono text-xs text-gray-700 bg-white p-3 rounded border">
                          {recs.raw_text}
                        </pre>
                      </details>
                    )}
                  </div>
                ) : (
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <p className="text-gray-600 mb-2">No recommendation data available.</p>
                    <pre className="whitespace-pre-wrap font-mono text-xs text-gray-700 max-h-96 overflow-auto">
                      {JSON.stringify(recs, null, 2)}
                    </pre>
                  </div>
                )}
                <button 
                  onClick={fetchRecommendations}
                  className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                >
                  Regenerate Plan
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecommendationsDashboard;