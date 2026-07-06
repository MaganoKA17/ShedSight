import pandas as pd
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def clear_old_data():
    print("Clearing old data...")
    supabase.table("raw_hourly_outages").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    supabase.table("daily_outage_summary").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print("Old data cleared")

def load_hourly_outages(filepath):
    """Read hourly outage CSV using Pandas and insert into Supabase"""
    print("⏳ Reading hourly outages CSV...")
    df = pd.read_csv(filepath)

    df = df.rename(columns={
        "DateTimeKey": "datetime_key",
        "Date Time Hour Beginning": "datetime_hour_beginning",
        "Hourly UCLF+OCLF": "hourly_uclf_oclf"
    })

    df = df.dropna()
    df["hourly_uclf_oclf"] = pd.to_numeric(df["hourly_uclf_oclf"], errors="coerce")
    df = df.dropna()

    print(f"{len(df)} rows loaded from CSV")
    print(df.head())

    for _, row in df.iterrows():
        data = {
            "datetime_key": str(row["datetime_key"]),
            "datetime_hour_beginning": str(row["datetime_hour_beginning"]),
            "hourly_uclf_oclf": float(row["hourly_uclf_oclf"])
        }
        supabase.table("raw_hourly_outages").insert(data).execute()

    print(f"{len(df)} hourly rows inserted into Supabase")

if __name__ == "__main__":
    clear_old_data()
    load_hourly_outages("hourly_outages.csv")