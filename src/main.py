"""
============================================================
FUTURE INTERNS - TASK 1: Sales Forecasting Project
Author: Abdi Negash
Date: June 2025
============================================================
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import joblib

warnings.filterwarnings("ignore")

# Create output directories
os.makedirs("images", exist_ok=True)
os.makedirs("models", exist_ok=True)
os.makedirs("reports", exist_ok=True)

print("=" * 60)
print("  FUTURE INTERNS - MACHINE LEARNING INTERNSHIP")
print("  Task 1: Sales Forecasting Using Machine Learning")
print("=" * 60)

# ============================================================
# SECTION 1: LOAD DATASET
# ============================================================
print("\n" + "=" * 60)
print("STEP 1: LOADING DATASET")
print("=" * 60)

df = pd.read_csv("data/sales.csv", sep='\t')
print(f"\nDataset loaded successfully!")
print(f"Total Rows: {df.shape[0]:,}")
print(f"Total Columns: {df.shape[1]}")
print(f"\nColumn Names: {df.columns.tolist()}")

# ============================================================
# SECTION 2: DATA UNDERSTANDING
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: DATA UNDERSTANDING")
print("=" * 60)

print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Basic Statistics ---")
print(df.describe())

print("\n--- Sample Data (First 5 Rows) ---")
print(df.head())

# ============================================================
# SECTION 3: DATA CLEANING
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: DATA CLEANING")
print("=" * 60)

print("\nWhy Data Cleaning?")
print("Dirty data (missing values, duplicates, wrong formats)")
print("causes poor model predictions. We clean it first.")

# Check for missing values
missing_before = df.isnull().sum().sum()
print(f"\nMissing values before cleaning: {missing_before}")

# Remove duplicates
duplicates_before = df.duplicated().sum()
df = df.drop_duplicates()
print(f"Duplicate rows removed: {duplicates_before}")

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])
print(f"Date column converted to datetime format")

# Check for missing values after
missing_after = df.isnull().sum().sum()
print(f"Missing values after cleaning: {missing_after}")

print("\nData Cleaning Complete!")

# ============================================================
# SECTION 4: FEATURE ENGINEERING
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: FEATURE ENGINEERING")
print("=" * 60)

print("\nWhy Feature Engineering?")
print("ML models cannot understand dates directly.")
print("We extract numbers (Year, Month, Day) from dates.")

df['Year'] = df['date'].dt.year
df['Month'] = df['date'].dt.month
df['Day'] = df['date'].dt.day
df['DayOfWeek'] = df['date'].dt.dayofweek
df['DayOfYear'] = df['date'].dt.dayofyear

print("\nNew Features Created:")
print("- Year")
print("- Month")
print("- Day")
print("- DayOfWeek")
print("- DayOfYear")

print("\nSample after Feature Engineering:")
print(df[['date', 'Year', 'Month', 'Day', 'DayOfWeek', 'sales']].head())

# ============================================================
# SECTION 5: EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 60)

print("\nWhy EDA?")
print("EDA helps us understand patterns in the data before modeling.")

# Focus on one store and one product family for fast training
STORE_NBR = 1
FAMILY = "GROCERY I"

print(f"\n--- Filtering Data for Store {STORE_NBR}, Family '{FAMILY}' ---")
df_filtered = df[(df['store_nbr'] == STORE_NBR) & (df['family'] == FAMILY)].copy()
print(f"Filtered rows: {len(df_filtered)}")

if len(df_filtered) == 0:
    FAMILY = df[df['store_nbr'] == STORE_NBR]['family'].iloc[0]
    df_filtered = df[(df['store_nbr'] == STORE_NBR) & (df['family'] == FAMILY)].copy()
    print(f"Using fallback family: '{FAMILY}'")
    print(f"Filtered rows: {len(df_filtered)}")

df_filtered = df_filtered.sort_values('date')

# --- Chart 1: Sales Trend Over Time ---
print("\nGenerating Chart 1: Sales Trend Over Time...")
plt.figure(figsize=(14, 5))
plt.plot(df_filtered['date'], df_filtered['sales'], linewidth=0.8, color='steelblue')
plt.title(f'Sales Trend Over Time\nStore {STORE_NBR} - {FAMILY}', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sales ($)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("images/sales_trend.png", dpi=150)
plt.close()
print("Saved: images/sales_trend.png")

# --- Chart 2: Monthly Sales Distribution ---
print("\nGenerating Chart 2: Monthly Sales Distribution...")
monthly_sales = df_filtered.groupby('Month')['sales'].mean()
plt.figure(figsize=(10, 5))
monthly_sales.plot(kind='bar', color='coral', edgecolor='black')
plt.title(f'Average Monthly Sales\nStore {STORE_NBR} - {FAMILY}', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Average Sales ($)', fontsize=12)
plt.xticks(rotation=0)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig("images/monthly_sales.png", dpi=150)
plt.close()
print("Saved: images/monthly_sales.png")

# --- Chart 3: Sales by Day of Week ---
print("\nGenerating Chart 3: Sales by Day of Week...")
dow_sales = df_filtered.groupby('DayOfWeek')['sales'].mean()
day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
plt.figure(figsize=(10, 5))
plt.bar(day_names, dow_sales.values, color='mediumseagreen', edgecolor='black')
plt.title(f'Average Sales by Day of Week\nStore {STORE_NBR} - {FAMILY}', fontsize=14, fontweight='bold')
plt.xlabel('Day of Week', fontsize=12)
plt.ylabel('Average Sales ($)', fontsize=12)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig("images/weekly_sales.png", dpi=150)
plt.close()
print("Saved: images/weekly_sales.png")

print("\nEDA Complete!")

# ============================================================
# SECTION 6: PREPARE DATA FOR MACHINE LEARNING
# ============================================================
print("\n" + "=" * 60)
print("STEP 6: PREPARING DATA FOR ML")
print("=" * 60)

features = ['Year', 'Month', 'Day', 'DayOfWeek', 'DayOfYear', 'onpromotion']
print(f"\nFeatures (X): {features}")
print("Target (y): sales")

X = df_filtered[features]
y = df_filtered['sales']

print(f"\nFeature matrix shape: {X.shape}")
print(f"Target vector shape: {y.shape}")

# ============================================================
# SECTION 7: TRAIN-TEST SPLIT
# ============================================================
print("\n" + "=" * 60)
print("STEP 7: TRAIN-TEST SPLIT")
print("=" * 60)

print("\nWhy Train-Test Split?")
print("We train on 80% of data and test on 20% to evaluate fairly.")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=False
)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Testing set: {X_test.shape[0]} samples")

# ============================================================
# SECTION 8: LINEAR REGRESSION MODEL
# ============================================================
print("\n" + "=" * 60)
print("STEP 8: LINEAR REGRESSION MODEL")
print("=" * 60)

print("\nWhat is Linear Regression?")
print("It finds a straight-line relationship between features and sales.")

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_predictions = lr_model.predict(X_test)

print("\nLinear Regression trained successfully!")

# ============================================================
# SECTION 9: RANDOM FOREST MODEL
# ============================================================
print("\n" + "=" * 60)
print("STEP 9: RANDOM FOREST MODEL")
print("=" * 60)

print("\nWhat is Random Forest?")
print("It combines many decision trees for stronger predictions.")

rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)

print("\nRandom Forest trained successfully!")

# ============================================================
# SECTION 10: MODEL EVALUATION
# ============================================================
print("\n" + "=" * 60)
print("STEP 10: MODEL EVALUATION")
print("=" * 60)

print("\nEvaluation Metrics Explained:")
print("-" * 40)
print("MAE  = Mean Absolute Error (average mistake in dollars)")
print("RMSE = Root Mean Squared Error (penalizes big mistakes)")
print("R2   = R-squared (1.0 = perfect, 0.0 = no better than guessing)")

def evaluate_model(name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    return mae, rmse, r2

lr_mae, lr_rmse, lr_r2 = evaluate_model("Linear Regression", y_test, lr_predictions)
rf_mae, rf_rmse, rf_r2 = evaluate_model("Random Forest", y_test, rf_predictions)

print("\n" + "-" * 50)
print(f"{'Metric':<20} {'Linear Regression':<18} {'Random Forest':<18}")
print("-" * 50)
print(f"{'MAE':<20} {lr_mae:<18.4f} {rf_mae:<18.4f}")
print(f"{'RMSE':<20} {lr_rmse:<18.4f} {rf_rmse:<18.4f}")
print(f"{'R2 Score':<20} {lr_r2:<18.4f} {rf_r2:<18.4f}")
print("-" * 50)

if rf_r2 > lr_r2:
    best_model = rf_model
    best_name = "Random Forest"
    print(f"\nBest Model: {best_name} (higher R2 score)")
else:
    best_model = lr_model
    best_name = "Linear Regression"
    print(f"\nBest Model: {best_name} (higher R2 score)")

# ============================================================
# SECTION 11: VISUALIZATION - ACTUAL VS PREDICTED
# ============================================================
print("\n" + "=" * 60)
print("STEP 11: ACTUAL VS PREDICTED VISUALIZATION")
print("=" * 60)

# --- Chart 4: Actual vs Predicted (Scatter) ---
plt.figure(figsize=(10, 6))
plt.scatter(y_test, rf_predictions, alpha=0.5, color='darkgreen', s=20)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
         'r--', linewidth=2, label='Perfect Prediction')
plt.xlabel('Actual Sales ($)', fontsize=12)
plt.ylabel('Predicted Sales ($)', fontsize=12)
plt.title(f'Actual vs Predicted Sales\n{best_name} Model', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("images/actual_vs_predicted.png", dpi=150)
plt.close()
print("Saved: images/actual_vs_predicted.png")

# --- Chart 5: Time Series Comparison ---
test_dates = df_filtered.iloc[-len(y_test):]['date']
plt.figure(figsize=(14, 6))
plt.plot(test_dates, y_test.values, label='Actual Sales', color='blue', linewidth=1.5)
plt.plot(test_dates, rf_predictions, label='Predicted Sales', color='red', linewidth=1.5, alpha=0.8)
plt.title(f'Sales Prediction Over Time\n{best_name} Model', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sales ($)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("images/prediction_timeline.png", dpi=150)
plt.close()
print("Saved: images/prediction_timeline.png")

# ============================================================
# SECTION 12: FEATURE IMPORTANCE
# ============================================================
print("\n" + "=" * 60)
print("STEP 12: FEATURE IMPORTANCE")
print("=" * 60)

importance = pd.DataFrame({
    'Feature': features,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n" + str(importance))

plt.figure(figsize=(10, 5))
plt.barh(importance['Feature'], importance['Importance'], color='teal', edgecolor='black')
plt.xlabel('Importance Score', fontsize=12)
plt.title('Feature Importance (Random Forest)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig("images/feature_importance.png", dpi=150)
plt.close()
print("Saved: images/feature_importance.png")

# ============================================================
# SECTION 13: FUTURE SALES FORECASTING
# ============================================================
print("\n" + "=" * 60)
print("STEP 13: FUTURE SALES FORECASTING")
print("=" * 60)

print("\nPredicting sales for the next 3 months (July - September 2017)...")

future_dates = pd.DataFrame({
    'date': pd.date_range(start='2017-07-01', periods=90, freq='D')
})
future_dates['Year'] = future_dates['date'].dt.year
future_dates['Month'] = future_dates['date'].dt.month
future_dates['Day'] = future_dates['date'].dt.day
future_dates['DayOfWeek'] = future_dates['date'].dt.dayofweek
future_dates['DayOfYear'] = future_dates['date'].dt.dayofyear
future_dates['onpromotion'] = 0

future_X = future_dates[features]
future_predictions = best_model.predict(future_X)

print(f"\nForecasted {len(future_predictions)} days")

# --- Chart 6: Future Forecast ---
plt.figure(figsize=(12, 5))
plt.plot(future_dates['date'], future_predictions, color='purple', linewidth=2, marker='o', markersize=3)
plt.title('Future Sales Forecast (July - September 2017)', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Predicted Sales ($)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("images/future_forecast.png", dpi=150)
plt.close()
print("Saved: images/future_forecast.png")

# Save predictions to CSV
forecast_df = pd.DataFrame({
    'Date': future_dates['date'],
    'Predicted_Sales': future_predictions
})
forecast_df.to_csv("reports/future_sales_forecast.csv", index=False)
print("Saved: reports/future_sales_forecast.csv")

# ============================================================
# SECTION 14: SAVE THE BEST MODEL
# ============================================================
print("\n" + "=" * 60)
print("STEP 14: SAVE THE BEST MODEL")
print("=" * 60)

joblib.dump(best_model, "models/sales_forecast_model.pkl")
print(f"Model saved: models/sales_forecast_model.pkl")
print(f"Model type: {best_name}")

# ============================================================
# SECTION 15: PROJECT SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("STEP 15: PROJECT SUMMARY & BUSINESS INSIGHTS")
print("=" * 60)

print(f"""
PROJECT SUMMARY
================
This project predicts future sales using historical data.
Workflow: Data Loading -> Cleaning -> EDA -> Feature Engineering 
-> Model Training -> Evaluation -> Future Forecasting

MODEL COMPARISON
================
Linear Regression:
  - MAE:  {lr_mae:.4f}
  - RMSE: {lr_rmse:.4f}
  - R2:   {lr_r2:.4f}

Random Forest:
  - MAE:  {rf_mae:.4f}
  - RMSE: {rf_rmse:.4f}
  - R2:   {rf_r2:.4f}

Winner: {best_name}

BUSINESS INSIGHTS
=================
1. Sales show clear seasonal patterns
2. Certain days of the week have higher average sales
3. {best_name} model provides the most accurate predictions
4. Future forecast helps plan inventory and staffing
5. Promotions influence sales volume

POSSIBLE IMPROVEMENTS
=====================
1. Use all stores and product families for better generalization
2. Add lag features (sales from previous days)
3. Try XGBoost or LightGBM for higher accuracy
4. Include external data (holidays, oil prices)
5. Build a web dashboard for real-time forecasting

FILES GENERATED
===============
- images/sales_trend.png
- images/monthly_sales.png
- images/weekly_sales.png
- images/actual_vs_predicted.png
- images/prediction_timeline.png
- images/feature_importance.png
- images/future_forecast.png
- models/sales_forecast_model.pkl
- reports/future_sales_forecast.csv
""")

print("=" * 60)
print("  TASK 1 COMPLETE!")
print("=" * 60)