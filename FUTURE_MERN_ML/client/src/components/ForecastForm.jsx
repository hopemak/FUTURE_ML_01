import { useState } from 'react';
import { Calendar, TrendingUp, Loader2 } from 'lucide-react';
import { generateForecast } from '../utils/api';

export default function ForecastForm({ onForecast }) {
  const [startDate, setStartDate] = useState('2017-07-01');
  const [days, setDays] = useState(30);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await generateForecast(startDate, parseInt(days));
      onForecast(response.data.forecast);
    } catch (error) {
      alert('Error generating forecast: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Calendar className="w-6 h-6 text-blue-600" />
        Generate Forecast
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Start Date
          </label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="input-field"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Forecast Period (days)
          </label>
          <select
            value={days}
            onChange={(e) => setDays(e.target.value)}
            className="input-field"
          >
            <option value={7}>7 days</option>
            <option value={30}>30 days</option>
            <option value={90}>90 days</option>
          </select>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="btn-success w-full flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <TrendingUp className="w-5 h-5" />
              Generate Forecast
            </>
          )}
        </button>
      </form>
    </div>
  );
}
