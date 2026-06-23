from google import genai
from supabase import create_client
import sys
sys.path.append("../pipeline")
from config import SUPABASE_URL, SUPABASE_KEY, GEMINI_API_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = genai.Client(api_key=GEMINI_API_KEY)


def fetch_daily_summaries():
    result = supabase.table("daily_outage_summary").select("*").order("date").execute()
    return result.data

def format_data_for_gemini(summaries):
    lines = ["Date | Avg UCLF+OCLF | Max UCLF+OCLF | High Stress Hours"]
    lines.append("-" * 60)
    for row in summaries:
        lines.append(
            f"{row['date']} | {row['avg_uclf_oclf']}% | {row['max_uclf_oclf']}% | {row['high_stress_hours']} hrs"
        )
    return "\n".join(lines)

def generate_insights(data_str):
    prompt = f"""
    You are a South African energy analyst. Below is 14 days of Eskom 
    grid stress data. UCLF+OCLF represents the percentage of generation 
    capacity lost due to unplanned outages. Higher values mean more load 
    shedding risk.

    {data_str}

    Please provide:
    1. A summary of the overall grid health over this period
    2. The worst and best days and what they indicate
    3. Any patterns or trends you notice
    4. What this means for ordinary South Africans
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    print("Fetching daily summaries...")
    summaries = fetch_daily_summaries()

    print("Formatting data for Gemini...")
    data_str = format_data_for_gemini(summaries)

    print("Generating AI insights...")
    insights = generate_insights(data_str)

    print("\n ShedSight AI Insights:")
    print("=" * 60)
    print(insights)