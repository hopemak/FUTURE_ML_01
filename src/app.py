"""
============================================================
FUTURE INTERNS - TASK 1: Sales Forecasting Web Dashboard
============================================================
"""

from flask import Flask, render_template, request
import pandas as pd
import numpy as np 
import joblib
import os

app = Flask(__name__)

# Load the saved model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'sales_forecast_model.pkl')
model = joblib.load(MODEL_PATH)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get inputs from the form
    year = int(request.form['year'])
    month = int(request.form['month'])
    day = int(request.form['day'])
    store_nbr = int(request.form['store_nbr'])
    onpromotion = int(request.form['onpromotion'])
    
    # Create feature vector
    from datetime import datetime
    date_obj = datetime(year, month, day)
    dayofweek = date_obj.weekday()
    dayofyear = date_obj.timetuple().tm_yday
    
    features = [[year, month, day, dayofweek, dayofyear, onpromotion]]
    
    # Make prediction
    prediction = model.predict(features)[0]
    
    return render_template('result.html', 
                           prediction=round(prediction, 2),
                           year=year,
                           month=month,
                           day=day,
                           store_nbr=store_nbr)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    """
============================================================
ML SERVICE - Flask API
Loads existing trained model, serves predictions
NO retraining - model already trained
============================================================
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Load existing trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'sales_forecast_model.pkl')
model = joblib.load(MODEL_PATH)
print(f"✅ Model loaded from {MODEL_PATH}")

@app.route('/health', methods=['GET'])
def health():
    """Check if service is running"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "service": "ML Prediction API"
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Single prediction endpoint
    Input: JSON with year, month, day, onpromotion
    Output: predicted sales
    """
    try:
        data = request.get_json()
        
        year = int(data['year'])
        month = int(data['month'])
        day = int(data['day'])
        onpromotion = int(data.get('onpromotion', 0))
        
        # Feature engineering (same as training)
        date_obj = datetime(year, month, day)
        dayofweek = date_obj.weekday()
        dayofyear = date_obj.timetuple().tm_yday
        
        features = [[year, month, day, dayofweek, dayofyear, onpromotion]]
        
        prediction = model.predict(features)[0]
        
        return jsonify({
            "success": True,
            "prediction": round(float(prediction), 2),
            "input": {
                "date": f"{year}-{month:02d}-{day:02d}",
                "dayofweek": dayofweek,
                "dayofyear": dayofyear,
                "onpromotion": onpromotion
            }
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/forecast', methods=['POST'])
def forecast():
    """
    Multi-day forecast endpoint
    Input: JSON with start_date, days (7, 30, or 90)
    Output: array of predictions
    """
    try:
        data = request.get_json()
        
        start_date_str = data['start_date']  # "2017-07-01"
        days = int(data['days'])
        
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        
        predictions = []
        dates = []
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            year = current_date.year
            month = current_date.month
            day = current_date.day
            dayofweek = current_date.weekday()
            dayofyear = current_date.timetuple().tm_yday
            onpromotion = 0  # Default assumption
            
            features = [[year, month, day, dayofweek, dayofyear, onpromotion]]
            pred = model.predict(features)[0]
            
            predictions.append(round(float(pred), 2))
            dates.append(current_date.strftime("%Y-%m-%d"))
        
        return jsonify({
            "success": True,
            "forecast": [
                {"date": d, "predicted_sales": p} 
                for d, p in zip(dates, predictions)
            ],
            "days": days,
            "start_date": start_date_str
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """
    Batch prediction from CSV data
    Input: JSON array of records
    """
    try:
        data = request.get_json()
        records = data['records']
        
        features_list = []
        for record in records:
            date_obj = datetime.strptime(record['date'], "%Y-%m-%d")
            features_list.append([
                date_obj.year,
                date_obj.month,
                date_obj.day,
                date_obj.weekday(),
                date_obj.timetuple().tm_yday,
                int(record.get('onpromotion', 0))
            ])
        
        predictions = model.predict(features_list)
        
        return jsonify({
            "success": True,
            "predictions": [round(float(p), 2) for p in predictions],
            "count": len(predictions)
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)