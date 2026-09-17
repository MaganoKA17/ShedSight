import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/home/wtc/Documents/ShedSight/pipeline')
from transform import transform_hourly_to_daily

class TestTransformHourlyToDaily:

    @patch("transform.supabase")
    def test_aggregates_hourly_to_daily(self, mock_supabase):
        """Test that hourly data aggregates into daily summaries"""
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"datetime_hour_beginning": "2026-06-21 00:00:00", "hourly_uclf_oclf": 9841.604},
            {"datetime_hour_beginning": "2026-06-21 01:00:00", "hourly_uclf_oclf": 9889.649},
            {"datetime_hour_beginning": "2026-06-21 02:00:00", "hourly_uclf_oclf": 10327.454},
            {"datetime_hour_beginning": "2026-06-22 00:00:00", "hourly_uclf_oclf": 10500.000},
            {"datetime_hour_beginning": "2026-06-22 01:00:00", "hourly_uclf_oclf": 10800.000},
        ]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = None
        transform_hourly_to_daily()
        assert mock_supabase.table.return_value.insert.call_count == 2

    @patch("transform.supabase")
    def test_converts_mw_to_percentage(self, mock_supabase):
        """Test that MW values are converted to percentage of 44000 MW"""
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"datetime_hour_beginning": "2026-06-21 00:00:00", "hourly_uclf_oclf": 44000.0},
        ]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = None
        transform_hourly_to_daily()
        inserted_data = mock_supabase.table.return_value.insert.call_args[0][0]
        assert inserted_data["avg_uclf_oclf"] == 100.0
        assert inserted_data["max_uclf_oclf"] == 100.0

    @patch("transform.supabase")
    def test_calculates_high_stress_hours(self, mock_supabase):
        """Test that high stress hours are counted correctly"""
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"datetime_hour_beginning": "2026-06-21 00:00:00", "hourly_uclf_oclf": 10000.0},
            {"datetime_hour_beginning": "2026-06-21 01:00:00", "hourly_uclf_oclf": 11000.0},
            {"datetime_hour_beginning": "2026-06-21 02:00:00", "hourly_uclf_oclf": 11500.0},
        ]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = None
        transform_hourly_to_daily()
        inserted_data = mock_supabase.table.return_value.insert.call_args[0][0]
        assert inserted_data["high_stress_hours"] == 2

    @patch("transform.supabase")
    def test_inserts_correct_date(self, mock_supabase):
        """Test that the correct date is extracted from timestamp"""
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"datetime_hour_beginning": "2026-06-21 00:00:00", "hourly_uclf_oclf": 9841.604},
        ]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = None
        transform_hourly_to_daily()
        inserted_data = mock_supabase.table.return_value.insert.call_args[0][0]
        assert inserted_data["date"] == "2026-06-21"

    @patch("transform.supabase")
    def test_handles_empty_data(self, mock_supabase):
        """Test that empty data from Supabase doesn't crash the script"""
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = []
        transform_hourly_to_daily()
        assert mock_supabase.table.return_value.insert.call_count == 0