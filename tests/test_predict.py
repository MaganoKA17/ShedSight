import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/home/wtc/Documents/ShedSight/pipeline')
from predict import engineer_features, generate_predictions, train_model

class TestEngineerFeatures:

    def test_extracts_hour_from_timestamp(self):
        """Test that hour is correctly extracted from timestamp"""
        df = pd.DataFrame({
            "datetime_hour_beginning": pd.to_datetime(["2026-06-21 18:00:00"]),
            "hourly_uclf_oclf": [10500.0]
        })
        result = engineer_features(df)
        assert result["hour"].iloc[0] == 18

    def test_extracts_day_of_week(self):
        """Test that day of week is correctly extracted"""
        df = pd.DataFrame({
            "datetime_hour_beginning": pd.to_datetime(["2026-06-21 00:00:00"]),
            "hourly_uclf_oclf": [9841.604]
        })
        result = engineer_features(df)
        assert result["day_of_week"].iloc[0] == 6

    def test_flags_peak_morning_hours(self):
        """Test that hours between 6am-9am are flagged as peak morning"""
        df = pd.DataFrame({
            "datetime_hour_beginning": pd.to_datetime(["2026-06-21 07:00:00"]),
            "hourly_uclf_oclf": [9841.604]
        })
        result = engineer_features(df)
        assert result["is_peak_morning"].iloc[0] == 1

    def test_flags_peak_evening_hours(self):
        """Test that hours between 5pm-9pm are flagged as peak evening"""
        df = pd.DataFrame({
            "datetime_hour_beginning": pd.to_datetime(["2026-06-21 19:00:00"]),
            "hourly_uclf_oclf": [9841.604]
        })
        result = engineer_features(df)
        assert result["is_peak_evening"].iloc[0] == 1

    def test_non_peak_hours_not_flagged(self):
        """Test that non-peak hours are not flagged"""
        df = pd.DataFrame({
            "datetime_hour_beginning": pd.to_datetime(["2026-06-21 12:00:00"]),
            "hourly_uclf_oclf": [9841.604]
        })
        result = engineer_features(df)
        assert result["is_peak_morning"].iloc[0] == 0
        assert result["is_peak_evening"].iloc[0] == 0

    def test_labels_high_stress_correctly(self):
        """Test that hours above 10500 MW are labelled as high stress"""
        df = pd.DataFrame({
            "datetime_hour_beginning": pd.to_datetime([
                "2026-06-21 00:00:00",
                "2026-06-21 01:00:00"
            ]),
            "hourly_uclf_oclf": [11000.0, 9000.0]
        })
        result = engineer_features(df)
        assert result["is_high_stress"].iloc[0] == 1
        assert result["is_high_stress"].iloc[1] == 0


class TestTrainModel:

    def test_model_trains_and_returns_accuracy(self):
        """Test that model trains and returns an accuracy score"""
        dates = pd.date_range("2026-06-01", periods=200, freq="h")
        df = pd.DataFrame({
            "datetime_hour_beginning": dates,
            "hourly_uclf_oclf": np.random.uniform(8000, 12000, 200)
        })
        df = engineer_features(df)
        model = train_model(df)
        assert model is not None

    def test_model_accuracy_is_reasonable(self):
        """Test that model accuracy is between 0 and 1"""
        dates = pd.date_range("2026-06-01", periods=200, freq="h")
        df = pd.DataFrame({
            "datetime_hour_beginning": dates,
            "hourly_uclf_oclf": np.random.uniform(8000, 12000, 200)
        })
        df = engineer_features(df)
        from sklearn.model_selection import train_test_split
        features = ["hour", "day_of_week", "is_peak_morning", "is_peak_evening"]
        X = df[features]
        y = df["is_high_stress"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = train_model(df)
        accuracy = model.score(X_test, y_test)
        assert 0 <= accuracy <= 1


class TestGeneratePredictions:

    def test_generates_24_predictions(self):
        """Test that exactly 24 predictions are generated"""
        dates = pd.date_range("2026-06-01", periods=200, freq="h")
        df = pd.DataFrame({
            "datetime_hour_beginning": dates,
            "hourly_uclf_oclf": np.random.uniform(8000, 12000, 200)
        })
        df = engineer_features(df)
        model = train_model(df)
        predictions = generate_predictions(model)
        assert len(predictions) == 24

    def test_predictions_have_required_keys(self):
        """Test that each prediction has predicted_hour, risk_level and probability"""
        dates = pd.date_range("2026-06-01", periods=200, freq="h")
        df = pd.DataFrame({
            "datetime_hour_beginning": dates,
            "hourly_uclf_oclf": np.random.uniform(8000, 12000, 200)
        })
        df = engineer_features(df)
        model = train_model(df)
        predictions = generate_predictions(model)
        for p in predictions:
            assert "predicted_hour" in p
            assert "risk_level" in p
            assert "probability" in p

    def test_risk_levels_are_valid(self):
        """Test that risk levels are only High, Medium or Low"""
        dates = pd.date_range("2026-06-01", periods=200, freq="h")
        df = pd.DataFrame({
            "datetime_hour_beginning": dates,
            "hourly_uclf_oclf": np.random.uniform(8000, 12000, 200)
        })
        df = engineer_features(df)
        model = train_model(df)
        predictions = generate_predictions(model)
        valid_levels = {"High", "Medium", "Low"}
        for p in predictions:
            assert p["risk_level"] in valid_levels

    def test_probabilities_are_between_0_and_1(self):
        """Test that all probabilities are between 0 and 1"""
        dates = pd.date_range("2026-06-01", periods=200, freq="h")
        df = pd.DataFrame({
            "datetime_hour_beginning": dates,
            "hourly_uclf_oclf": np.random.uniform(8000, 12000, 200)
        })
        df = engineer_features(df)
        model = train_model(df)
        predictions = generate_predictions(model)
        for p in predictions:
            assert 0 <= p["probability"] <= 1

class TestFetchHistoricalData:

    @patch("predict.supabase")
    def test_fetches_data_from_supabase(self, mock_supabase):
        """Test that fetch_historical_data returns a DataFrame"""
        from predict import fetch_historical_data
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"datetime_hour_beginning": "2026-06-21 00:00:00", "hourly_uclf_oclf": 9841.604},
            {"datetime_hour_beginning": "2026-06-21 01:00:00", "hourly_uclf_oclf": 9889.649},
        ]
        df = fetch_historical_data()
        assert len(df) == 2
        assert "datetime_hour_beginning" in df.columns
        assert "hourly_uclf_oclf" in df.columns

    @patch("predict.supabase")
    def test_drops_null_values(self, mock_supabase):
        """Test that null values are dropped"""
        from predict import fetch_historical_data
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"datetime_hour_beginning": "2026-06-21 00:00:00", "hourly_uclf_oclf": 9841.604},
            {"datetime_hour_beginning": None, "hourly_uclf_oclf": None},
        ]
        df = fetch_historical_data()
        assert len(df) == 1


class TestSavePredictions:

    @patch("predict.supabase")
    def test_clears_old_predictions(self, mock_supabase):
        """Test that old predictions are cleared before saving new ones"""
        from predict import save_predictions
        mock_supabase.table.return_value.delete.return_value.neq.return_value.execute.return_value = None
        mock_supabase.table.return_value.insert.return_value.execute.return_value = None
        predictions = [
            {"predicted_hour": "2026-09-08T15:00:00", "risk_level": "High", "probability": 0.95}
        ]
        save_predictions(predictions)
        mock_supabase.table.return_value.delete.assert_called()

    @patch("predict.supabase")
    def test_inserts_all_predictions(self, mock_supabase):
        """Test that all predictions are inserted into Supabase"""
        from predict import save_predictions
        mock_supabase.table.return_value.delete.return_value.neq.return_value.execute.return_value = None
        mock_supabase.table.return_value.insert.return_value.execute.return_value = None
        predictions = [
            {"predicted_hour": "2026-09-08T15:00:00", "risk_level": "High", "probability": 0.95},
            {"predicted_hour": "2026-09-08T16:00:00", "risk_level": "Low", "probability": 0.15},
            {"predicted_hour": "2026-09-08T17:00:00", "risk_level": "Medium", "probability": 0.55},
        ]
        save_predictions(predictions)
        assert mock_supabase.table.return_value.insert.call_count == 3