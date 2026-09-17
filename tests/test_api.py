import pytest
import sys
sys.path.insert(0, '/home/wtc/Documents/ShedSight/api')
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    with patch("app.supabase"), patch("app.client"):
        from app import app
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client


class TestPredictionsEndpoint:

    def test_predictions_endpoint_returns_200(self, client):
        """Test that /predictions returns 200"""
        with patch("app.supabase") as mock_supabase:
            mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
                {
                    "id": "abc123",
                    "predicted_hour": "2026-09-08T15:00:00+00:00",
                    "risk_level": "High",
                    "probability": 0.95,
                    "created_at": "2026-09-08T12:00:00+00:00"
                }
            ]
            response = client.get("/predictions")
            assert response.status_code == 200

    def test_predictions_response_has_required_keys(self, client):
        """Test that /predictions response contains predictions, warnings and has_warnings"""
        with patch("app.supabase") as mock_supabase:
            mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
                {
                    "id": "abc123",
                    "predicted_hour": "2026-09-08T15:00:00+00:00",
                    "risk_level": "High",
                    "probability": 0.95,
                    "created_at": "2026-09-08T12:00:00+00:00"
                }
            ]
            response = client.get("/predictions")
            data = response.get_json()
            assert "predictions" in data
            assert "warnings" in data
            assert "has_warnings" in data

    def test_warnings_only_contains_high_and_medium(self, client):
        """Test that warnings only includes High and Medium risk predictions"""
        with patch("app.supabase") as mock_supabase:
            mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
                {
                    "id": "abc123",
                    "predicted_hour": "2026-09-08T15:00:00+00:00",
                    "risk_level": "High",
                    "probability": 0.95,
                    "created_at": "2026-09-08T12:00:00+00:00"
                },
                {
                    "id": "def456",
                    "predicted_hour": "2026-09-08T16:00:00+00:00",
                    "risk_level": "Low",
                    "probability": 0.15,
                    "created_at": "2026-09-08T12:00:00+00:00"
                }
            ]
            response = client.get("/predictions")
            data = response.get_json()
            for warning in data["warnings"]:
                assert warning["risk_level"] in ["High", "Medium"]

    def test_has_warnings_true_when_high_risk_exists(self, client):
        """Test that has_warnings is True when High risk predictions exist"""
        with patch("app.supabase") as mock_supabase:
            mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
                {
                    "id": "abc123",
                    "predicted_hour": "2026-09-08T15:00:00+00:00",
                    "risk_level": "High",
                    "probability": 0.95,
                    "created_at": "2026-09-08T12:00:00+00:00"
                }
            ]
            response = client.get("/predictions")
            data = response.get_json()
            assert data["has_warnings"] == True

    def test_has_warnings_false_when_only_low_risk(self, client):
        """Test that has_warnings is False when only Low risk predictions exist"""
        with patch("app.supabase") as mock_supabase:
            mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
                {
                    "id": "abc123",
                    "predicted_hour": "2026-09-08T15:00:00+00:00",
                    "risk_level": "Low",
                    "probability": 0.15,
                    "created_at": "2026-09-08T12:00:00+00:00"
                }
            ]
            response = client.get("/predictions")
            data = response.get_json()
            assert data["has_warnings"] == False


class TestInsightsEndpoint:

    def test_insights_endpoint_returns_200(self, client):
        """Test that /insights returns 200"""
        with patch("app.supabase") as mock_supabase, \
                patch("app.client") as mock_groq:
            mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
                {
                    "date": "2026-06-21",
                    "avg_uclf_oclf": 23.5,
                    "max_uclf_oclf": 26.8,
                    "high_stress_hours": 5
                }
            ]
            mock_groq.chat.completions.create.return_value.choices = [
                MagicMock(message=MagicMock(content="Grid health summary here."))
            ]
            response = client.get("/insights")
            assert response.status_code == 200

    def test_insights_response_has_insights_key(self, client):
        """Test that /insights response contains insights key"""
        with patch("app.supabase") as mock_supabase, \
                patch("app.client") as mock_groq:
            mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
                {
                    "date": "2026-06-21",
                    "avg_uclf_oclf": 23.5,
                    "max_uclf_oclf": 26.8,
                    "high_stress_hours": 5
                }
            ]
            mock_groq.chat.completions.create.return_value.choices = [
                MagicMock(message=MagicMock(content="Grid health summary here."))
            ]
            response = client.get("/insights")
            data = response.get_json()
            assert "insights" in data

    def test_insights_returns_string(self, client):
        """Test that insights value is a non-empty string"""
        with patch("app.supabase") as mock_supabase, \
                patch("app.client") as mock_groq:
            mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
                {
                    "date": "2026-06-21",
                    "avg_uclf_oclf": 23.5,
                    "max_uclf_oclf": 26.8,
                    "high_stress_hours": 5
                }
            ]
            mock_groq.chat.completions.create.return_value.choices = [
                MagicMock(message=MagicMock(content="Grid health summary here."))
            ]
            response = client.get("/insights")
            data = response.get_json()
            assert isinstance(data["insights"], str)
            assert len(data["insights"]) > 0

    def test_insights_handles_groq_error(self, client):
        """Test that /insights handles Groq API errors gracefully"""
        with patch("app.supabase") as mock_supabase, \
                patch("app.client") as mock_groq:
            mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
                {
                    "date": "2026-06-21",
                    "avg_uclf_oclf": 23.5,
                    "max_uclf_oclf": 26.8,
                    "high_stress_hours": 5
                }
            ]
            mock_groq.chat.completions.create.side_effect = Exception("Groq API error")
            response = client.get("/insights")
            assert response.status_code == 500