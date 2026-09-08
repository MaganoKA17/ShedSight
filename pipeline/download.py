import requests
from bs4 import BeautifulSoup
from datetime import datetime

HOURLY_PAGE_URL = "https://www.eskom.co.za/dataportal/outage-performance/hourly-uclfoclf-trend/"

def get_latest_csv_url(page_url):
    """Scrape the Eskom page to find the latest CSV download URL"""
    print(f"🔍 Scraping {page_url} for latest CSV URL...")
    response = requests.get(page_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch page — status code {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all CSV links containing UCLF
    csv_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if ".csv" in href.lower() and "uclf" in href.lower():
            csv_links.append(href)
    
    if not csv_links:
        print("No CSV URLs found on page")
        return None
    
    # Sort links and pick the most recent one
    csv_links.sort(reverse=True)
    latest = csv_links[0]
    print(f"Found latest CSV URL: {latest}")
    return latest

def download_csv(url, filename):
    """Download a CSV file from a URL"""
    print(f"⏳ Downloading {filename} from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"{filename} downloaded successfully")
        return True
    else:
        print(f"Failed to download {filename} — status code {response.status_code}")
        return False

if __name__ == "__main__":
    url = get_latest_csv_url(HOURLY_PAGE_URL)
    if url:
        download_csv(url, "hourly_outages.csv")
    else:
        print("Could not find CSV URL — please update manually in download.py")