import { useState, useEffect } from 'react';
import { logAPI } from '../services/api';
import { Calendar, TrendingUp, TrendingDown, Minus, Target, Zap } from 'lucide-react';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);

  useEffect(() => {
    fetchDashboard();
  }, [selectedDate]);

  const fetchDashboard = async () => {
    setLoading(true);
    try {
      const response = await logAPI.getDashboard(selectedDate);
      setDashboardData(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const getProgressColor = (consumed, goal) => {
    const percentage = (consumed / goal) * 100;
    if (percentage >= 90) return 'bg-success-500';
    if (percentage >= 70) return 'bg-warning-500';
    return 'bg-danger-500';
  };

  const getGapIcon = (gap) => {
    if (gap > 0) return <TrendingUp className="text-success-500" size={16} />;
    if (gap < 0) return <TrendingDown className="text-danger-500" size={16} />;
    return <Minus className="text-gray-500" size={16} />;
  };

  const CircularProgress = ({ percentage, size = 80, strokeWidth = 8, color = 'text-primary-600' }) => {
    const radius = (size - strokeWidth) / 2;
    const circumference = radius * 2 * Math.PI;
    const strokeDasharray = `${circumference} ${circumference}`;
    const strokeDashoffset = circumference - (percentage / 100) * circumference;

    return (
      <div className="relative inline-flex items-center justify-center">
        <svg width={size} height={size} className="transform -rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            fill="transparent"
            className="text-gray-200"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            fill="transparent"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            className={color}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-xs sm:text-sm font-semibold">{Math.round(percentage)}%</span>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-900">Dashboard</h1>
        <div className="flex items-center space-x-2">
          <Calendar size={20} className="text-gray-500" />
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="input-field text-sm"
          />
        </div>
      </div>

      {dashboardData ? (
        <>
          {/* Calorie Progress Circle */}
          <div className="card text-center">
            <h3 className="text-base sm:text-lg font-semibold mb-4 flex items-center justify-center">
              <Zap size={20} className="mr-2" />
              Daily Calorie Goal
            </h3>
            <div className="flex flex-col items-center space-y-4">
              <CircularProgress 
                percentage={Math.min((dashboardData.total_calories_consumed / dashboardData.total_calories_goal) * 100, 100)}
                size={120}
                strokeWidth={12}
                color="text-primary-600"
              />
              <div className="text-center">
                <div className="text-xl sm:text-2xl font-bold text-primary-600">
                  {Math.round(dashboardData.total_calories_consumed)}
                </div>
                <div className="text-sm text-gray-600">
                  of {dashboardData.total_calories_goal} kcal
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {Math.round(dashboardData.total_calories_goal - dashboardData.total_calories_consumed)} kcal remaining
                </div>
              </div>
            </div>
          </div>

          {/* Macros Overview */}
          <div className="card">
            <h3 className="text-base sm:text-lg font-semibold mb-4">Macronutrients</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-success-50 rounded-lg">
                <CircularProgress 
                  percentage={Math.min((dashboardData.total_protein_consumed / dashboardData.total_protein_goal) * 100, 100)}
                  size={60}
                  strokeWidth={6}
                  color="text-success-600"
                />
                <div className="mt-2">
                  <div className="text-sm font-semibold text-success-800">Protein</div>
                  <div className="text-xs text-success-600">
                    {Math.round(dashboardData.total_protein_consumed)}g / {dashboardData.total_protein_goal}g
                  </div>
                </div>
              </div>
              
              <div className="text-center p-4 bg-warning-50 rounded-lg">
                <CircularProgress 
                  percentage={dashboardData.total_fat_goal > 0 ? Math.min((dashboardData.total_fat_consumed / dashboardData.total_fat_goal) * 100, 100) : 0}
                  size={60}
                  strokeWidth={6}
                  color="text-warning-600"
                />
                <div className="mt-2">
                  <div className="text-sm font-semibold text-warning-800">Fat</div>
                  <div className="text-xs text-warning-600">
                    {Math.round(dashboardData.total_fat_consumed)}g / {dashboardData.total_fat_goal}g
                  </div>
                </div>
              </div>
              
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <div className="flex items-center justify-center h-[60px]">
                  <Target size={24} className="text-purple-600" />
                </div>
                <div className="mt-2">
                  <div className="text-sm font-semibold text-purple-800">Carbs</div>
                  <div className="text-xs text-purple-600">
                    {Math.round(dashboardData.total_carbs_consumed)}g
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Analysis */}
          <div className="card">
            <h3 className="text-base sm:text-lg font-semibold mb-4">Nutrient Analysis</h3>
            <div className="space-y-3 sm:space-y-4">
              {dashboardData.detailed_analysis.slice(0, 6).map((nutrient, index) => {
                const percentage = Math.min((nutrient.consumed / nutrient.goal) * 100, 100);
                return (
                  <div key={index} className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="font-medium text-sm sm:text-base">{nutrient.nutrient_name}</span>
                      <div className="flex items-center space-x-2">
                        {getGapIcon(nutrient.gap)}
                        <span className="text-xs sm:text-sm text-gray-600">
                          {Math.round(nutrient.consumed * 100) / 100} / {nutrient.goal} {nutrient.unit}
                        </span>
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${getProgressColor(nutrient.consumed, nutrient.goal)}`}
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <div className="text-xs text-gray-500">
                      {Math.round(percentage)}% of daily goal
                      {nutrient.gap !== 0 && (
                        <span className={`ml-2 ${nutrient.gap > 0 ? 'text-success-600' : 'text-danger-600'}`}>
                          ({nutrient.gap > 0 ? '+' : ''}{Math.round(nutrient.gap * 100) / 100} {nutrient.unit})
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="card">
            <h3 className="text-base sm:text-lg font-semibold mb-2">Profile</h3>
            <p className="text-sm sm:text-base text-gray-600">{dashboardData.matched_demographic_group}</p>
          </div>
        </>
      ) : (
        <div className="card text-center py-8 sm:py-12">
          <Target size={32} className="mx-auto mb-4 text-gray-300" />
          <p className="text-sm sm:text-base text-gray-600">No data for this date. Start logging meals!</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
