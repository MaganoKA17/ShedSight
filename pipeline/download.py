import requests
import os

HOURLY_URL = "https://www.eskom.co.za/dataportal/wp-content/uploads/2026/06/Hourly_UCLF_and_OCLF_Trend.csv"
WEEKLY_URL = "https://www.eskom.co.za/dataportal/wp-content/uploads/2026/06/Weekly_unplanned_outages.csv"

def download_csv(url, filename):
   
    print(f"⏳ Downloading {filename}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"{filename} downloaded successfully")
    else:
        print(f"Failed to download {filename} — status code {response.status_code}")

if __name__ == "__main__":
    download_csv(HOURLY_URL, "hourly_outages.csv")
    download_csv(WEEKLY_URL, "weekly_outages.csv")