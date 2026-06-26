import { useState, useEffect } from 'react';
import { History, Calendar, DollarSign } from 'lucide-react';
import { getForecastHistory } from '../utils/api';

export default function ForecastHistory() {
  const [forecasts, setForecasts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await getForecastHistory();
      setForecasts(response.data.forecasts);
    } catch (error) {
      console.error('Failed to load history:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8 flex items-center gap-3">
        <History className="w-8 h-8 text-blue-600" />
        Forecast History
      </h1>

      {loading ? (
        <div className="text-center py-12 text-gray-500">Loading...</div>
      ) : forecasts.length === 0 ? (
        <div className="card text-center py-12 text-gray-500">
          No forecasts generated yet.
        </div>
      ) : (
        <div className="space-y-4">
          {forecasts.map((forecast, idx) => (
            <div key={idx} className="card flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-blue-100 rounded-lg">
                  <Calendar className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <p className="font-semibold text-gray-800">
                    {new Date(forecast.date).toLocaleDateString()}
                  </p>
                  <p className="text-sm text-gray-500">
                    Model: {forecast.model_used}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <DollarSign className="w-5 h-5 text-green-600" />
                <span className="text-xl font-bold text-green-600">
                  ${forecast.predicted_sales?.toFixed(2)}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
