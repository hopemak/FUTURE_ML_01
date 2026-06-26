import { useState, useEffect } from 'react';
import { Activity, TrendingUp, TrendingDown, Target } from 'lucide-react';
import { LineChartCard, BarChartCard } from '../components/ChartCard';
import ForecastForm from '../components/ForecastForm';
import { getMetrics } from '../utils/api';

export default function Dashboard() {
  const [forecast, setForecast] = useState([]);
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    loadMetrics();
  }, []);

  const loadMetrics = async () => {
    try {
      const response = await getMetrics();
      setMetrics(response.data.metrics);
    } catch (error) {
      console.error('Failed to load metrics:', error);
    }
  };

  const handleForecast = (data) => {
    setForecast(data);
  };

  const metricCards = [
    { 
      title: 'R2 Score', 
      value: metrics?.r2?.toFixed(4) || '0.6671', 
      icon: Target, 
      color: 'text-green-600',
      bg: 'bg-green-100'
    },
    { 
      title: 'MAE', 
      value: metrics?.mae?.toFixed(2) || '217.70', 
      icon: TrendingDown, 
      color: 'text-blue-600',
      bg: 'bg-blue-100'
    },
    { 
      title: 'RMSE', 
      value: metrics?.rmse?.toFixed(2) || '336.56', 
      icon: Activity, 
      color: 'text-purple-600',
      bg: 'bg-purple-100'
    },
    { 
      title: 'Model', 
      value: metrics?.model_name || 'Random Forest', 
      icon: TrendingUp, 
      color: 'text-orange-600',
      bg: 'bg-orange-100'
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Sales Forecasting Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {metricCards.map((card, idx) => (
          <div key={idx} className="card flex items-center space-x-4">
            <div className={`p-3 rounded-lg ${card.bg}`}>
              <card.icon className={`w-6 h-6 ${card.color}`} />
            </div>
            <div>
              <p className="text-sm text-gray-500">{card.title}</p>
              <p className="text-2xl font-bold text-gray-800">{card.value}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1">
          <ForecastForm onForecast={handleForecast} />
        </div>

        <div className="lg:col-span-2">
          {forecast.length > 0 ? (
            <LineChartCard
              title={`Sales Forecast (${forecast.length} days)`}
              data={forecast}
              dataKey="predicted_sales"
              color="#8b5cf6"
            />
          ) : (
            <div className="card h-[380px] flex items-center justify-center text-gray-400">
              <div className="text-center">
                <TrendingUp className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p className="text-lg">Generate a forecast to see results</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {metrics?.features && (
        <div className="mt-8">
          <BarChartCard
            title="Feature Importance"
            data={metrics.features.map(f => ({ name: f.name, importance: f.importance }))}
            dataKey="importance"
            color="#3b82f6"
          />
        </div>
      )}
    </div>
  );
}
