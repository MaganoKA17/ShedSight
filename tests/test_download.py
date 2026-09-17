import pytest
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/home/wtc/Documents/ShedSight/pipeline')
from download import get_latest_csv_url, download_csv

class TestGetLatestCsvUrl:

    @patch("download.requests.get")
    def test_finds_csv_url_on_page(self, mock_get):
        """Test that scraper finds a CSV URL containing 'uclf'"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <body>
                    <a href="https://www.eskom.co.za/wp-content/uploads/2026/07/Hourly_UCLF_and_OCLF_Trend.csv">Download</a>
                </body>
            </html>
        """
        mock_get.return_value = mock_response
        url = get_latest_csv_url("https://fake-eskom-page.co.za")
        assert url is not None
        assert ".csv" in url
        assert "uclf" in url.lower()

    @patch("download.requests.get")
    def test_returns_none_when_page_fails(self, mock_get):
        """Test that scraper returns None when page returns non-200"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        url = get_latest_csv_url("https://fake-eskom-page.co.za")
        assert url is None

    @patch("download.requests.get")
    def test_returns_none_when_no_csv_found(self, mock_get):
        """Test that scraper returns None when no CSV link on page"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><a href='https://eskom.co.za/about'>About</a></body></html>"
        mock_get.return_value = mock_response
        url = get_latest_csv_url("https://fake-eskom-page.co.za")
        assert url is None


class TestDownloadCsv:

    @patch("download.requests.get")
    def test_downloads_file_successfully(self, mock_get, tmp_path):
        """Test that CSV downloads and saves correctly"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"DateTimeKey,Date Time Hour Beginning,Hourly UCLF+OCLF\n1,2026-06-21,9841.604"
        mock_get.return_value = mock_response
        filepath = tmp_path / "test.csv"
        result = download_csv("https://fake-url.csv", str(filepath))
        assert result == True
        assert filepath.exists()

    @patch("download.requests.get")
    def test_returns_false_on_failed_download(self, mock_get, tmp_path):
        """Test that download returns False on 404"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        filepath = tmp_path / "test.csv"
        result = download_csv("https://fake-url.csv", str(filepath))
        assert result == False