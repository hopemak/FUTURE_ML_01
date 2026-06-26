const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const connectDB = require('./config/db');
const uploadRoutes = require('./routes/upload');
const forecastRoutes = require('./routes/forecast');
const metricsRoutes = require('./routes/metrics');

const app = express();

app.use(cors());
app.use(express.json());

connectDB();

app.use('/api/upload', uploadRoutes);
app.use('/api/forecast', forecastRoutes);
app.use('/api/metrics', metricsRoutes);

app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'Node.js API Gateway',
    timestamp: new Date().toISOString()
  });
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📊 ML Service: ${process.env.ML_SERVICE_URL}`);
});
