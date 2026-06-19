import requests
import json
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, ESKOMSEPUSH_API_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BASE_URL = "https://developer.sepush.co.za/business/2.0"
HEADERS = {"Token" : ESKOMSEPUSH_API_KEY}

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
        print(f"Raw response: {data}")

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

if __name__ == "__main__":           
    # areas = [
    #     # {
    #     #     "id" : "jhb-1-sandton",
    #     #     "name": "Sandton",
    #     # },
    #     # {
    #     #     "id" : "jhb-2-fourways",
    #     #     "name": "Fourways",
    #     # },
    #     {
    #         "id" : "eskde-7-rosebankjohannesburg",
    #         "name": "Rosebank",
    #     },
    #     {
    #         "id" : "jhb-rosebank",
    #         "name": "Rosebank v2",
    #     },
    #     {
    #         "id" : "eskde-rosebank",
    #         "name": "Rosebank v3",
    #     },
    # ]
    # # run_ingestion(areas)
    # response = requests.get(
    #     f"{BASE_URL}/status",
    #     headers=HEADERS,
    #     # params={"lat": "-26.2041", "lon":"28.0473"}
    # )
    # data = response.json()

    # with open("status_output.json", "w") as file:
    #     json.dump(data, file, indent=2)
    # print("Output saved to status_output.json")
    # # print(response.json())

    # for area in areas:
        response = requests.get(
            f"{BASE_URL}/areas_nearby",
            headers=HEADERS,
            # params={"id" : area["id"]}
            params={"lat": "-26.1452", "lon":"28.0436"}
        )
        data = response.json()
        # print(f"{area['name']} ({area['id']}): {data}")
    
