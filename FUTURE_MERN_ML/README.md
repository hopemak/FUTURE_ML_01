# Sales Forecasting - MERN + Python ML Stack

## Architecture
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   React     │────▶│  Node.js    │────▶│   Python    │
│  Frontend   │◄────│   Express   │◄────│   Flask ML  │
│  (Port 3000)│     │  (Port 5000)│     │  (Port 5001)│
└─────────────┘     └──────┬──────┘     └─────────────┘
│
┌──────▼──────┐
│  MongoDB    │
│   Atlas     │
└─────────────┘
plain

## Quick Start

### 1. Start ML Service
```bash
cd ml-service
pip install -r requirements.txt
python app.py
# Runs on http://localhost:5001