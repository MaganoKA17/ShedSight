import os
import csv
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_hourly_outages(filepath):
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data = {
                "datetime_key": row["DateTimeKey"],
                "datetime_hour_beginning" : row["Date Time Hour Beginning"],
                "hourly_uclf_oclf" : float(row["Hourly UCLF+OCLF"])
            }
            supabase.table("raw_hourly_outages").insert(data).execute()
            print(f"Inserted row for {row['Date Time Hour Beginning']}")

def load_weekly_outages(filepath):
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data = {
                "week_date" : row["Week_min_DateKey"],
                "min_uclf_oclf" : float(row["Min of UCLF + OCLF"]),
                "avg_uclf_oclf" : float(row["Average of UCLF + OCLF"]),
                "max_uclf_oclf" : float(row["Max of UCLF + OCLF"]),
            }
            supabase.table("raw_weekly_outages").insert(data).execute()
            print(f"Inserted row for {row['Week_min_DateKey']}")

if __name__ == "__main__":
    load_hourly_outages("hourly_outages.csv")
    load_weekly_outages("weekly_outages.csv")
    # result = supabase.table("raw_hourly_outages").select("*").execute()
    # print(f"Connection test: {result}")
    # print(f"Supabase URL: {SUPABASE_URL}")
    # print(f"Supabase Key: {SUPABASE_KEY[:20]}...")