const mongoose = require('mongoose');

const metricSchema = new mongoose.Schema({
  model_name: { type: String, required: true },
  mae: { type: Number, required: true },
  rmse: { type: Number, required: true },
  r2: { type: Number, required: true },
  timestamp: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Metric', metricSchema);
