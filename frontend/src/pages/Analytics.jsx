import { useState, useEffect } from 'react';
import { logAPI } from '../services/api';
import { Calendar, TrendingUp, Award, Target } from 'lucide-react';

const Analytics = () => {
  const [analytics, setAnalytics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dateRange, setDateRange] = useState({
    start: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0]
  });

  useEffect(() => {
    fetchAnalytics();
  }, [dateRange]);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const promises = [];
      const startDate = new Date(dateRange.start);
      const endDate = new Date(dateRange.end);
      
      for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
        const dateStr = d.toISOString().split('T')[0];
        promises.push(
          logAPI.getDashboard(dateStr).catch(() => null)
        );
      }
      
      const results = await Promise.all(promises);
      const validResults = results.filter(r => r && r.data);
      setAnalytics(validResults.map(r => r.data));
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateAverages = () => {
    if (analytics.length === 0) return null;
    
    const totals = analytics.reduce((acc, day) => ({
      calories: acc.calories + day.total_calories_consumed,
      protein: acc.protein + day.total_protein_consumed,
      fat: acc.fat + day.total_fat_consumed,
      carbs: acc.carbs + day.total_carbs_consumed,
    }), { calories: 0, protein: 0, fat: 0, carbs: 0 });

    return {
      calories: Math.round(totals.calories / analytics.length),
      protein: Math.round(totals.protein / analytics.length * 10) / 10,
      fat: Math.round(totals.fat / analytics.length * 10) / 10,
      carbs: Math.round(totals.carbs / analytics.length * 10) / 10,
    };
  };

  const getGoalAchievementRate = () => {
    if (analytics.length === 0) return 0;
    
    const achievedDays = analytics.filter(day => 
      day.total_calories_consumed >= day.total_calories_goal * 0.8
    ).length;
    
    return Math.round((achievedDays / analytics.length) * 100);
  };

  const averages = calculateAverages();
  const achievementRate = getGoalAchievementRate();

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Date Range</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Start Date</label>
            <input
              type="date"
              value={dateRange.start}
              onChange={(e) => setDateRange(prev => ({ ...prev, start: e.target.value }))}
              className="input-field mt-1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">End Date</label>
            <input
              type="date"
              value={dateRange.end}
              onChange={(e) => setDateRange(prev => ({ ...prev, end: e.target.value }))}
              className="input-field mt-1"
            />
          </div>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      ) : analytics.length > 0 ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="card text-center">
              <TrendingUp className="mx-auto mb-2 text-primary-600" size={24} />
              <div className="text-2xl font-bold text-gray-900">{averages?.calories}</div>
              <div className="text-sm text-gray-600">Avg Calories/Day</div>
            </div>
            <div className="card text-center">
              <Target className="mx-auto mb-2 text-success-600" size={24} />
              <div className="text-2xl font-bold text-gray-900">{averages?.protein}g</div>
              <div className="text-sm text-gray-600">Avg Protein/Day</div>
            </div>
            <div className="card text-center">
              <Award className="mx-auto mb-2 text-warning-600" size={24} />
              <div className="text-2xl font-bold text-gray-900">{achievementRate}%</div>
              <div className="text-sm text-gray-600">Goal Achievement</div>
            </div>
            <div className="card text-center">
              <Calendar className="mx-auto mb-2 text-purple-600" size={24} />
              <div className="text-2xl font-bold text-gray-900">{analytics.length}</div>
              <div className="text-sm text-gray-600">Days Tracked</div>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Daily Breakdown</h3>
            <div className="space-y-4">
              {analytics.map((day, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="font-medium">{day.log_date}</h4>
                    <span className={`px-2 py-1 rounded text-xs ${
                      day.total_calories_consumed >= day.total_calories_goal * 0.8
                        ? 'bg-success-100 text-success-800'
                        : 'bg-warning-100 text-warning-800'
                    }`}>
                      {Math.round((day.total_calories_consumed / day.total_calories_goal) * 100)}% of goal
                    </span>
                  </div>
                  <div className="grid grid-cols-4 gap-4 text-sm">
                    <div>
                      <div className="text-gray-600">Calories</div>
                      <div className="font-medium">{Math.round(day.total_calories_consumed)}</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Protein</div>
                      <div className="font-medium">{Math.round(day.total_protein_consumed * 10) / 10}g</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Fat</div>
                      <div className="font-medium">{Math.round(day.total_fat_consumed * 10) / 10}g</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Carbs</div>
                      <div className="font-medium">{Math.round(day.total_carbs_consumed * 10) / 10}g</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      ) : (
        <div className="card text-center py-12">
          <Calendar size={48} className="mx-auto mb-4 text-gray-300" />
          <p className="text-gray-600">No data available for the selected date range.</p>
          <p className="text-sm text-gray-500 mt-2">Start logging your meals to see analytics!</p>
        </div>
      )}
    </div>
  );
};

export default Analytics;
