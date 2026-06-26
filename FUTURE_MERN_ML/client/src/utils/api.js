import axios from 'axios';

const API_URL = 'http://localhost:8080/api';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const generateForecast = (startDate, days) => 
  api.post('/forecast', { start_date: startDate, days });

export const getForecastHistory = () => 
  api.get('/forecast/history');

export const getMetrics = () => 
  api.get('/metrics');

export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};
