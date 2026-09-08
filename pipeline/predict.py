import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from supabase import create_client
from datetime import datetime, timedelta
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

HIGH_STRESS_THRESHOLD = 10500

print("predict.py started")

def fetch_historical_data():
    """Fetch all hourly data from Supabase"""
    print("⏳ Fetching historical data...")
    result = supabase.table("raw_hourly_outages").select("*").execute()
    df = pd.DataFrame(result.data)
    df["datetime_hour_beginning"] = pd.to_datetime(df["datetime_hour_beginning"])
    df["hourly_uclf_oclf"] = pd.to_numeric(df["hourly_uclf_oclf"], errors="coerce")
    df = df.dropna()
    print(f"{len(df)} rows fetched")
    return df

def engineer_features(df):
    """Extract time-based features for the model"""
    df["hour"] = df["datetime_hour_beginning"].dt.hour
    df["day_of_week"] = df["datetime_hour_beginning"].dt.dayofweek
    df["is_peak_morning"] = df["hour"].between(6, 9).astype(int)
    df["is_peak_evening"] = df["hour"].between(17, 21).astype(int)
    df["is_high_stress"] = (df["hourly_uclf_oclf"] > HIGH_STRESS_THRESHOLD).astype(int)
    return df

def train_model(df):
    """Train a Random Forest model on historical data"""
    print(" Training model...")
    features = ["hour", "day_of_week", "is_peak_morning", "is_peak_evening"]
    X = df[features]
    y = df["is_high_stress"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"Model trained — accuracy: {round(accuracy * 100, 2)}%")
    return model

def generate_predictions(model):
    """Generate predictions for the next 24 hours"""
    print("Generating predictions for next 24 hours...")
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    next_24_hours = [now + timedelta(hours=i) for i in range(1, 25)]

    predictions = []
    for hour in next_24_hours:
        features = {
            "hour": hour.hour,
            "day_of_week": hour.weekday(),
            "is_peak_morning": 1 if 6 <= hour.hour <= 9 else 0,
            "is_peak_evening": 1 if 17 <= hour.hour <= 21 else 0
        }
        df_features = pd.DataFrame([features])
        probability = model.predict_proba(df_features)[0][1]

        if probability >= 0.7:
            risk_level = "High"
        elif probability >= 0.4:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        predictions.append({
            "predicted_hour": hour.isoformat(),
            "risk_level": risk_level,
            "probability": round(float(probability), 4)
        })

    return predictions

def save_predictions(predictions):
    """Clear old predictions and save new ones to Supabase"""
    print("Clearing old predictions...")
    supabase.table("predictions").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()

    print("Saving new predictions...")
    for p in predictions:
        supabase.table("predictions").insert(p).execute()

    print(f"{len(predictions)} predictions saved")

if __name__ == "__main__":
    df = fetch_historical_data()
    df = engineer_features(df)
    model = train_model(df)
    predictions = generate_predictions(model)
    save_predictions(predictions)
    print("Predictions complete!")