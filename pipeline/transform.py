import pandas as pd
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def transform_hourly_to_daily():
   
    print("Fetching raw hourly data from Supabase...")
    result = supabase.table("raw_hourly_outages").select("*").execute()

    df = pd.DataFrame(result.data)

    df["datetime_hour_beginning"] = pd.to_datetime(df["datetime_hour_beginning"])
    df["hourly_uclf_oclf"] = pd.to_numeric(df["hourly_uclf_oclf"], errors="coerce")
    df.dropna()

    df["date"] = df["datetime_hour_beginning"].dt.date

    daily = df.groupby("date").agg(
        avg_uclf_oclf=("hourly_uclf_oclf", "mean"),
        max_uclf_oclf=("hourly_uclf_oclf", "max"),
        high_stress_hours=("hourly_uclf_oclf", lambda x: (x < 30).sum())
    ).reset_index()

    daily["avg_uclf_oclf"] = daily["avg_uclf_oclf"].round(4)
    daily["max_uclf_oclf"] = daily["max_uclf_oclf"].round(4)

    print(daily)

    for _, row in daily.iterrows():
        data = {
            "date": str(row["date"]),
            "avg_uclf_oclf": float(row["avg_uclf_oclf"]),
            "max_uclf_oclf": float(row["max_uclf_oclf"]),
            "high_stress_hours": int(row["high_stress_hours"])
        }
        supabase.table("daily_outage_summary").insert(data).execute()
        print(f"Inserted daily summary for {row['date']}")

if __name__ == "__main__":
    transform_hourly_to_daily()