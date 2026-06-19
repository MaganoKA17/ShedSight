import os
import csv
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, ESKOMSEPUSH_API_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_hourly_wages(filepath):
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data = {
                "datetim_key": row["DateTimeKey"],
                "datetime_hour_beginning" : row["DateTimeHourBeginning"],
                "hourly_uclf_oclf" : float(row["Hourly UCLF + OCLF"])
            }
            supabase.table("raw_hourly_outages").insert(data).execute()
            print(f"Inserted row for {row['DataTimeHourBeginning']}")
