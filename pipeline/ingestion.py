import requests
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, ESKOMPUSH_API_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BASE_URL = "https://developer.sepush.co.za/business/2.0"
HEADERS = {"Token" : ESKOMPUSH_API_KEY}

def get_area_schedule(area_id):
    response = requests.get(f"{BASE_URL}/area", headers=HEADERS, params= {"id": area_id})
    return response.json()

def save_raw_outage(area_id, area_name, stage, schedule):
    data = {
        "area_id" : area_id,
        "area_name" : area_name,
        "stage" : stage,
        "schedule" : schedule
    }
    supabase.table("raw_outages").insert(data).execute()
    print(f"Saved raw data for {area_name}")

def run_ingestion(areas):
    for area in areas:
        print(f"Fetching data for {area['name']}...")
        data = get_area_schedule(area['id'])

        if "schedule" in data:
            stage = data["schedule"]["current"]["stage"] if "current" in data["schedule"] else 0

            save_raw_outage(
                area_id=area['id'],
                area_name=area['name'],
                stage = int(stage),
                schedule =data["schedule"]
            ) 
        else:
            print(f"No schedule data for {area['name']}")
