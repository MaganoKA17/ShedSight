from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
from datetime import datetime

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def transform_hourly_to_daily():
    print("Fetching raw hourly data")
    result = supabase.table("raw_hourly_outages").select("*").execute()
    rows = result.data

    daily_data = {}

    for row in rows:
        date = row["datetime_hour_beginning"][:10]

        if date not in daily_data:
            daily_data[date] = {
                "uclf_oclf_values" : []
            }
        daily_data[date]["uclf_oclf_values"].append(float(row["hourly_uclf_oclf"]))
    
    print("Aggregatting daily metrics...")

    for date, values in daily_data.items():
        uclf_values = values["uclf_oclf_values"]
        avg = sum(uclf_values) / len(uclf_values)
        maximum = max(uclf_values)

        high_stress_hours = len([value for value in uclf_values if value > 30])

        data = {
            "date": date,
            "avg_uclf_oclf": round(avg, 4),
            "max_uclf_oclf": round(maximum, 4),
            "high_stress_hours": high_stress_hours
        }

        supabase.table("daily_outage_summary").insert(data).execute()
        print(f"Inserted daily summary for {date}")

if __name__ == "__main__":
    transform_hourly_to_daily()