import os

from flask import Flask, jsonify
from datetime import datetime, timedelta
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load trained XGBoost model
model = joblib.load("models/xgb_model.pkl")

# Load feature-engineered dataset
df = pd.read_excel(
    "data/final_feature_engineered_data.xlsx"
)

# Home route
@app.route('/')
def home():

    return "Forecasting API Running!"

# Help route
@app.route('/help')
def help_route():

    return jsonify({

        "message": "Available API Routes",

        "routes": {

            "/": "Home Route",

            "/help": "API Documentation Route",

            "/predict/<state>":
            "Forecast next 8 weeks sales forecast for a state"

        }
    })


# State list route
@app.route('/states')
def states():

    state_list = sorted(
        df['State'].dropna().astype(str).str.strip().unique().tolist()
    )

    return jsonify({
        "states": state_list
    })

# Prediction route
@app.route('/predict/<state>')
def predict(state):

    # Filter state data
    state_df = df[
        df['State'].astype(str).str.strip().str.lower()
        == state.strip().lower()
    ].copy()

    # Check state exists
    if state_df.empty:

        return jsonify({
            "error": f"State '{state}' not found"
        }), 404

    # Get latest row for selected state using the actual date order
    latest_state_date = None
    if 'Date' in state_df.columns:
        state_df['Date'] = pd.to_datetime(state_df['Date'], errors='coerce')
        state_df = state_df.sort_values('Date')
        latest_state_date = state_df['Date'].dropna().iloc[-1] if not state_df['Date'].dropna().empty else None

    latest_row = state_df.iloc[-1]

    # Extract latest feature values
    lag_1 = latest_row['lag_1']
    lag_7 = latest_row['lag_7']
    lag_30 = latest_row['lag_30']

    rolling_mean = latest_row['rolling_mean_7']
    rolling_std = latest_row['rolling_std_7']

    month = latest_row['month']

    # NEW: state encoded feature
    state_encoded = latest_row['state_encoded']

    # Store predictions
    predictions = []

    forecast_anchor_date = latest_state_date if pd.notna(latest_state_date) else datetime.now()

    # Generate 8-week forecast
    for week in range(8):

        sample_features = np.array([[

            lag_1,
            lag_7,
            lag_30,
            rolling_mean,
            rolling_std,
            week % 7,
            month,
            0,
            state_encoded

        ]])

        # Predict
        pred = model.predict(sample_features)[0]

        # Generate future date
        future_date_obj = (
            forecast_anchor_date + timedelta(weeks=week + 1)
        )

        future_date = future_date_obj.strftime(
            "%Y-%m-%d"
        )

        # Dynamically update month
        month = future_date_obj.month

        # Store prediction
        predictions.append({

            "forecast_horizon": week + 1,

            "forecast_date": future_date,

            "prediction": round(float(pred), 2)

        })

        # Update lag values dynamically
        lag_30 = lag_7
        lag_7 = lag_1
        lag_1 = pred

        # Update rolling statistics
        rolling_mean = (
            lag_1 + lag_7 + lag_30
        ) / 3

        rolling_std = np.std([
            lag_1,
            lag_7,
            lag_30
        ])

    # Final API response
    return jsonify({

        "state": state,

        "best_model": "XGBoost",

        "forecast_next_8_weeks": predictions

    })

# Run Flask app
if __name__ == '__main__':

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)