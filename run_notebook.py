import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
print("TASK 1: SALES & DEMAND FORECASTING")
print("CIN: FIT/JUN26/ML9423 | Author: Abdi Negash")
print("=" * 60)

# Load dataset
print("\n[1/9] Loading dataset...")
df = pd.read_csv("data/sales.csv", sep='\t')
print(f"Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")

# Data cleaning
print("\n[2/9] Cleaning data...")
df = df.drop_duplicates()
df['date'] = pd.to_datetime(df['date'])
print(f"Duplicates removed. Data cleaned.")

# Feature engineering
print("\n[3/9] Engineering features...")
df['Year'] = df['date'].dt.year
df['Month'] = df['date'].dt.month
df['Day'] = df['date'].dt.day
df['DayOfWeek'] = df['date'].dt.dayofweek
df['DayOfYear'] = df['date'].dt.dayofyear
print("Features created: Year, Month, Day, DayOfWeek, DayOfYear")

# Filter data
print("\n[4/9] Filtering data...")
STORE_NBR = 1
FAMILY = "GROCERY I"
df_filtered = df[(df['store_nbr'] == STORE_NBR) & (df['family'] == FAMILY)].copy()
df_filtered = df_filtered.sort_values('date')
print(f"Filtered: {len(df_filtered)} rows for Store {STORE_NBR}, {FAMILY}")

# Generate charts
print("\n[5/9] Generating charts...")

# Chart 1: Sales Trend
plt.figure(figsize=(14, 5))
plt.plot(df_filtered['date'], df_filtered['sales'], linewidth=0.8, color='steelblue')
plt.title(f'Sales Trend Over Time - Store {STORE_NBR}, {FAMILY}', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Sales ($)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("images/sales_trend.png", dpi=150)
plt.close()
print("  ✓ images/sales_trend.png")

# Chart 2: Monthly Sales
monthly_sales = df_filtered.groupby('Month')['sales'].mean()
plt.figure(figsize=(10, 5))
monthly_sales.plot(kind='bar', color='coral', edgecolor='black')
plt.title(f'Average Monthly Sales - Store {STORE_NBR}, {FAMILY}', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Average Sales ($)')
plt.xticks(rotation=0)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig("images/monthly_sales.png", dpi=150)
plt.close()
print("  ✓ images/monthly_sales.png")

# Prepare ML data
features = ['Year', 'Month', 'Day', 'DayOfWeek', 'DayOfYear', 'onpromotion']
X = df_filtered[features]
y = df_filtered['sales']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

# Train models
print("\n[6/9] Training models...")
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_predictions = lr_model.predict(X_test)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)
print("  ✓ Linear Regression trained")
print("  ✓ Random Forest trained")

# Evaluate
print("\n[7/9] Evaluating models...")
def evaluate(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    return mae, rmse, r2

lr_mae, lr_rmse, lr_r2 = evaluate(y_test, lr_predictions)
rf_mae, rf_rmse, rf_r2 = evaluate(y_test, rf_predictions)

print(f"\n  Linear Regression: MAE={lr_mae:.2f}, RMSE={lr_rmse:.2f}, R²={lr_r2:.4f}")
print(f"  Random Forest:     MAE={rf_mae:.2f}, RMSE={rf_rmse:.2f}, R²={rf_r2:.4f}")

best_model = rf_model if rf_r2 > lr_r2 else lr_model
best_name = "Random Forest" if rf_r2 > lr_r2 else "Linear Regression"
print(f"\n  🏆 Best Model: {best_name}")

# Chart 3: Actual vs Predicted
plt.figure(figsize=(10, 6))
plt.scatter(y_test, rf_predictions, alpha=0.5, color='darkgreen', s=20)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2, label='Perfect Prediction')
plt.xlabel('Actual Sales ($)')
plt.ylabel('Predicted Sales ($)')
plt.title(f'Actual vs Predicted Sales - {best_name}', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("images/actual_vs_predicted.png", dpi=150)
plt.close()
print("  ✓ images/actual_vs_predicted.png")

# Chart 4: Future Forecast
print("\n[8/9] Generating future forecast...")
from datetime import datetime, timedelta

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

plt.figure(figsize=(12, 5))
plt.plot(future_dates['date'], future_predictions, color='purple', linewidth=2, marker='o', markersize=3)
plt.title('Future Sales Forecast (July - September 2017)', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Predicted Sales ($)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("images/future_forecast.png", dpi=150)
plt.close()
print("  ✓ images/future_forecast.png")

# Save forecast CSV
forecast_df = pd.DataFrame({
    'Date': future_dates['date'],
    'Predicted_Sales': future_predictions
})
forecast_df.to_csv("reports/future_sales_forecast.csv", index=False)
print("  ✓ reports/future_sales_forecast.csv")

# Chart 5: Feature Importance
print("\n[9/9] Generating feature importance...")
importances = rf_model.feature_importances_
feature_names = features

plt.figure(figsize=(10, 6))
indices = np.argsort(importances)[::-1]
plt.bar(range(len(importances)), importances[indices], color='teal', edgecolor='black')
plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
plt.title('Feature Importance - Random Forest', fontsize=14, fontweight='bold')
plt.ylabel('Importance')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig("images/feature_importance.png", dpi=150)
plt.close()
print("  ✓ images/feature_importance.png")

# Print feature importance
print("\nFeature Importance:")
for i in indices:
    print(f"  {feature_names[i]}: {importances[i]*100:.2f}%")

# Save model
joblib.dump(best_model, "models/sales_forecast_model.pkl")
print("\n  ✓ models/sales_forecast_model.pkl")

print("\n" + "=" * 60)
print("ALL DONE! Generated files:")
print("  images/sales_trend.png")
print("  images/monthly_sales.png")
print("  images/actual_vs_predicted.png")
print("  images/future_forecast.png")
print("  images/feature_importance.png")
print("  reports/future_sales_forecast.csv")
print("  models/sales_forecast_model.pkl")
print("=" * 60)
