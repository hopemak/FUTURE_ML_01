const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {
  const metrics = {
    model_name: "Random Forest Regressor",
    mae: 217.7041,
    rmse: 336.5636,
    r2: 0.6671,
    comparison: {
      linear_regression: { mae: 393.8454, rmse: 503.0614, r2: 0.2562 },
      random_forest: { mae: 217.7041, rmse: 336.5636, r2: 0.6671 }
    },
    features: [
      { name: "DayOfWeek", importance: 0.5856 },
      { name: "DayOfYear", importance: 0.2445 },
      { name: "Day", importance: 0.1180 },
      { name: "Month", importance: 0.0288 },
      { name: "Year", importance: 0.0230 },
      { name: "OnPromotion", importance: 0.0000 }
    ]
  };
  
  res.json({ success: true, metrics });
});

module.exports = router;
