from flask import Flask, jsonify
from flask_cors import CORS
from groq import Groq
from supabase import create_client
import sys
sys.path.append("../pipeline")
from config import SUPABASE_URL, SUPABASE_KEY, GROQ_API_KEY

app = Flask(__name__)
CORS(app)

supabase =create_client(SUPABASE_URL, SUPABASE_KEY)
client = Groq(api_key=GROQ_API_KEY)

def fetch_daily_summaries():
    result = supabase.table("daily_outage_summary").select("*").order("date").execute()
    return result.data

def format_data(summaries):
    lines = ["Date | Avg Stress % | Max Stress % | High Stress Hours"]
    lines.append("-" * 60)

    for row in summaries:
        lines.append(
            f"{row['date']} | {row['avg_uclf_oclf']}% | {row['max_uclf-oclf']}% | {row['high_stress_hours']} hrs"
        )
        return "\n".join(lines)
    
@app.route("/insights", methods=["GET"])
def get_insights():
    summaries = fetch_daily_summaries()
    data_str = format_data(summaries)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a South African energy analyst who explains Eskom grid data in clear, simple language for everyday South Africans."
            },
            {
                "role": "user",
                "content": f"""
                Below is 14 days of Eskom grid stress data. 
                The stress percentage represents how much of Eskom's 
                total capacity was unavailable due to outages. 
                Higher values mean more load shedding risk.

                {data_str}

                Please provide:
                1. A summary of overall grid health over this period
                2. The worst and best days and what they indicate
                3. Any patterns or trends you notice
                4. What this means for ordinary South Africans
                """
            }
        ]
    )

    insights = response.choices[0].message.content
    return jsonify({"insights": insights})

if __name__ == "__main__":
    app.run(debug=True, port=5000)