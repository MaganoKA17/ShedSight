import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/home/wtc/Documents/ShedSight/pipeline')
from ingestion import load_hourly_outages, clear_old_data

class TestClearOldData:

    @patch("ingestion.supabase")
    def test_clears_hourly_outages_table(self, mock_supabase):
        """Test that clear_old_data deletes from raw_hourly_outages"""
        mock_supabase.table.return_value.delete.return_value.neq.return_value.execute.return_value = None
        clear_old_data()
        calls = [call[0][0] for call in mock_supabase.table.call_args_list]
        assert "raw_hourly_outages" in calls

    @patch("ingestion.supabase")
    def test_clears_daily_summary_table(self, mock_supabase):
        """Test that clear_old_data deletes from daily_outage_summary"""
        mock_supabase.table.return_value.delete.return_value.neq.return_value.execute.return_value = None
        clear_old_data()
        calls = [call[0][0] for call in mock_supabase.table.call_args_list]
        assert "daily_outage_summary" in calls


class TestLoadHourlyOutages:

    @patch("ingestion.supabase")
    def test_loads_csv_and_inserts_rows(self, mock_supabase, tmp_path):
        """Test that CSV loads and inserts correct number of rows"""
        csv_content = """DateTimeKey,Date Time Hour Beginning,Hourly UCLF+OCLF
2026-06-21 00:00:00,2026-06-21 00:00:00,9841.604
2026-06-21 01:00:00,2026-06-21 01:00:00,9889.649
2026-06-21 02:00:00,2026-06-21 02:00:00,10327.454"""
        csv_file = tmp_path / "hourly_outages.csv"
        csv_file.write_text(csv_content)
        mock_supabase.table.return_value.insert.return_value.execute.return_value = None
        load_hourly_outages(str(csv_file))
        assert mock_supabase.table.return_value.insert.call_count == 3

    @patch("ingestion.supabase")
    def test_drops_rows_with_missing_values(self, mock_supabase, tmp_path):
        """Test that rows with missing values are dropped"""
        csv_content = """DateTimeKey,Date Time Hour Beginning,Hourly UCLF+OCLF
2026-06-21 00:00:00,2026-06-21 00:00:00,9841.604
2026-06-21 01:00:00,,
2026-06-21 02:00:00,2026-06-21 02:00:00,10327.454"""
        csv_file = tmp_path / "hourly_outages.csv"
        csv_file.write_text(csv_content)
        mock_supabase.table.return_value.insert.return_value.execute.return_value = None
        load_hourly_outages(str(csv_file))
        assert mock_supabase.table.return_value.insert.call_count == 2

    @patch("ingestion.supabase")
    def test_renames_columns_correctly(self, mock_supabase, tmp_path):
        """Test that columns are renamed to match Supabase schema"""
        csv_content = """DateTimeKey,Date Time Hour Beginning,Hourly UCLF+OCLF
2026-06-21 00:00:00,2026-06-21 00:00:00,9841.604"""
        csv_file = tmp_path / "hourly_outages.csv"
        csv_file.write_text(csv_content)
        mock_supabase.table.return_value.insert.return_value.execute.return_value = None
        load_hourly_outages(str(csv_file))
        inserted_data = mock_supabase.table.return_value.insert.call_args[0][0]
        assert "datetime_key" in inserted_data
        assert "datetime_hour_beginning" in inserted_data
        assert "hourly_uclf_oclf" in inserted_data