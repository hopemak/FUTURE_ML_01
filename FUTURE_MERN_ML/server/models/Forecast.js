const mongoose = require('mongoose');

const forecastSchema = new mongoose.Schema({
  date: { type: String, required: true },
  predicted_sales: { type: Number, required: true },
  model_used: { type: String, default: 'Random Forest' },
  days_forecasted: { type: Number, default: 1 },
  timestamp: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Forecast', forecastSchema);
