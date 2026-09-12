# ShedSight

A data analytics application that tracks, stores, and analyzes South African 
load shedding data — and uses AI to surface insights that raw schedules can't show you.

## Problem Statement
South Africans lack a clear, data-driven picture of how load shedding affects 
their lives over time. ShedSight solves this by building a pipeline that collects, 
transforms, and analyzes real Eskom data — then displays it on an interactive dashboard 
with AI-generated insights.

## Target Audience
- Households wanting to understand their power loss over time
- Small business owners making decisions about backup power
- Students and remote workers planning around outages
- Researchers and journalists studying load shedding impacts

## Features

- Ingests real Eskom hourly outage data using Pandas
- Stores raw and transformed data in Supabase (PostgreSQL)
- Transforms raw hourly MW data into meaningful daily percentage summaries
- Interactive React dashboard with line charts, bar charts, and stat cards
- Dark and light mode toggle with energy-themed colour scheme
- Flask API serving AI-generated insights
- Groq AI (LLaMA 3.1) analyzes 14 days of grid data and explains it in plain English

## Tech Stack
| Layer | Tool |
|---|---|
| Data Source | Eskom Open Data Portal |
| Data Processing | Python + Pandas |
| Database | Supabase (PostgreSQL) |
| AI Layer | Groq API (LLaMA 3.1) |
| Backend API | Flask |
| Frontend | React + Vite + Recharts |
| Version Control | Git + GitHub |

## Project Structure

```Bash
shedsight/
├── ai/
│   └── insights.py             # Standalone Groq AI insights script
├── api/
│   └── app.py                  # Flask API serving AI insights
├── frontend/
│   └── src/
│       ├── App.jsx             # Main dashboard component
│       └── supabaseClient.js   # Supabase connection
├── pipeline/
│   ├── config.py               # Environment variable loader
│   ├── download.py             # Downloads latest hourly CSV from Eskom
│   ├── ingestion.py            # Loads CSV data into Supabase using Pandas
│   ├── transform.py            # Aggregates raw data into daily summaries
│   └── hourly_outages.csv      # Hourly UCLF+OCLF data from Eskom
├── sql/
│   └── schema.sql              # Supabase table definitions
├── .env.example                # Environment variable template
└── README.md
```

## Data Explanation
Data is sourced from the [Eskom Open Data Portal](https://www.eskom.co.za/dataportal).

**UCLF+OCLF** = Unplanned Capacity Loss Factor + Outage Capacity Loss Factor.
Raw values are in megawatts (MW) and are converted to a percentage of Eskom's
total generation capacity (~44,000 MW). Higher percentages indicate more severe
load shedding conditions.

| Metric | Description |
|---|---|
| Avg Stress % | Average percentage of capacity lost per day |
| Max Stress % | Peak capacity loss recorded that day |
| High Stress Hours | Hours where capacity loss exceeded 10,500 MW |

## Automated Pipeline
The pipeline is fully automated using a cron job that runs every Monday at 6am:

```bash
0 6 * * 1 cd /path/to/shedsight/pipeline && python3 download.py && python3 ingestion.py && python3 transform.py
```

### What happens automatically every Monday:
1. `download.py` — fetches the latest hourly CSV from the Eskom Open Data Portal
2. `ingestion.py` — clears old data and loads fresh CSV data into Supabase
3. `transform.py` — aggregates hourly data into daily summaries

To set it up on your machine:
```bash
crontab -l > /tmp/mycron
echo "0 6 * * 1 cd /path/to/shedsight/pipeline && python3 download.py && python3 ingestion.py && python3 transform.py" >> /tmp/mycron
crontab /tmp/mycron
```

## Setup

### 1. Clone the repo
```bash
git clone git@github.com:MaganoKA17/shedsight.git
cd shedsight
```

### 2. Install dependencies
```bash
pip install supabase pandas groq flask flask-cors python-dotenv
```

### 3. Set up environment variables
```bash
cp .env.example .env
```
Fill in your keys in `.env`:
```bash
SUPABASE_URL= your_supabase_url
SUPABASE_KEY= your_supabase_database_key
GROQ_API_KEY= your_groq_api_key
```

### 4. Run the pipeline
```bash
cd pipeline
python3 download.py
python3 ingestion.py
python3 transform.py
```

### 5. Start the Flask API
```bash
cd api
python3 app.py
```

### 6. Run the frontend
```bash
cd frontend
npm install
npm run dev
```

## Refreshing Data Manually
To refresh data outside the scheduled run:
```bash
cd pipeline
python3 download.py
python3 ingestion.py
python3 transform.py
```

Note: `download.py` automatically scrapes the Eskom data portal to find 
the latest CSV URL — no manual URL updates needed when Eskom changes their links.

## Current Data Status
As of mid-2026, South Africa has had experienced over 341 consecutive days without load shedding following Eskom's Grid
Recovery Plan. As a result, the Eskom data portal is not publishing fresh outage data at the same frequency as 
previous years.

The pipeline currently uses the most recent available dataset (June-July 2026) which captures the tail end of the last 
period of grid stress. The pipeline and prediction model are fully functional and will automatically ingest fresh data 
when Eskom resumes publishing data hourly outage metrics.

## Author
Kgosi-E-tsile Magano

## Verification Code:
WTC-CY28J9UG