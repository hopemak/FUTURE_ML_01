const express = require('express');
const router = express.Router();
const axios = require('axios');
const Forecast = require('../models/Forecast');

router.post('/', async (req, res) => {
  try {
    const { start_date, days } = req.body;
    
    const mlResponse = await axios.post(`${process.env.ML_SERVICE_URL}/forecast`, {
      start_date,
      days
    });
    
    if (!mlResponse.data.success) {
      return res.status(400).json(mlResponse.data);
    }
    
    const forecastData = mlResponse.data.forecast;
    
    try {
      await Forecast.insertMany(
        forecastData.map(f => ({
          date: f.date,
          predicted_sales: f.predicted_sales,
          days_forecasted: days
        }))
      );
    } catch (dbError) {
      console.log('DB save skipped (MongoDB may not be running)');
    }
    
    res.json({
      success: true,
      forecast: forecastData,
      saved_count: forecastData.length,
      message: `Forecast generated for ${days} days`
    });
    
  } catch (error) {
    console.error('Forecast error:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

router.get('/history', async (req, res) => {
  try {
    const forecasts = await Forecast.find().sort({ timestamp: -1 }).limit(100);
    res.json({
      success: true,
      count: forecasts.length,
      forecasts
    });
  } catch (error) {
    res.json({
      success: true,
      count: 0,
      forecasts: []
    });
  }
});

module.exports = router;
