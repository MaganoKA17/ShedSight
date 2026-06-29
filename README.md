# ShedSight

A data analytics application that tracks, stores, and analyzes South African load shedding data, and uses AI to
surface insights that raw schedules cannot show you.

## Problem Statement

South Africans lack a clear, data-driven picture of how load shedding affects their lives over time. ShedSight solves this by building a pipeline that collects, transforms and analyzes real Eskom data, then displays it on an interactive dashboard with AI-generated insights.

## Target Audience
- Households wanting to understand their power loss over time
- Small businesses owners making decisions about backup power
- Students and remote workers planning around outages
- Researchers and journalists studying load shedding impacts

## Features
- Ingests real Eskom outage data (hourly and weekly) using Pandas
- Stores raw and transformed data in Supabase (PostgreSQL)
- Transforms raw data into meaningful daily percentage summaries
- AI-powered insights via Google Gemini (coming soon)
- Interactive React dashboard with  line charts, bar charts and stat cards
- Flask API serving AI-generated insights
- Groq AI (Llama 3) analyzes 14 days of grid data and explains it in plain English

## Tech Stack

| Layer | Tool |
|---|---|
| Data Source | Eskom Open Data Portal |
| Data Processing | Python + Pandas |
| Database | Supabase (PostgreSQL) |
| AI Layer | Groq API (Llama 3.1) |
| Backend API | Flask |
| Frontend | React + Vite + Recharts |
| Version Control | Git + GitHub |

## Project Structure
```
shedsight/
├── ai/
│   └── insights.py
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── supabaseClient.js
├── pipeline/
│   ├── config.py
│   ├── ingestion.py
│   ├── transform.py
│   ├── hourly_outages.csv
│   └── weekly_outages.csv
├── sql/
│   └── schema.sql
├── .env.example
└── README.md
```

## Data Explanation

Data is sourced from the [Eskom Open Data Portal](https://www.eskom.co.za/dataportal).

**UCLF+OCLF** = Unplanned Capacity Loss Factor + Outage Capacity loss Factor. Raw values are in megawatts (MW) and aree converted toa percentage of Eskom's total generation capacity (~44,000 MW). Higher
percentages indicate more severe load shedding conditions.

| Metric | Description |
|---|---|
| Avg Stress % | Average percentage of capacity lost per day |
| Max Stress % | Peak capacity loss recorded that day |
| High Stress Hours | Hours where capacity loss exceeded 20,500 MW |

## Automated Pipeline

The pipeline is scheduled to run every Monday at 6am using a cron job:

```Bash
0 6 * * 1 cd /home/wtc/Documents/ShedSight/pipeline && python3 ingestion.py && python3 transform.py
```

This ensures the dashboard always reflects the latest 14 days of Eskom data.
To set it up on your machine run `crontab -e` and add the line above.
## Setup

### 1. Clone the repo
```Bash
git clone git@github.com:YOURUSERNAME/shedsight.git
cd ShedSight
```

### 2. Install Dependencies
```Bash
pip install supabase pandas groq flask flask-cors python-dotenv
```

### 3. Set up environment variables
```Bash
cp .env.example .env
```
Fill in your keys in '.env'

### 4. Refreshing Data
Download the latest CSVs from the [Eskom Open Data Portal](https://www.eskom.co.za/dataportal) 
and replace the files in the `pipeline/` folder, then rerun the pipeline.

### 5. Run the pipeline
```Bash
cd pipeline
python3 ingestion.py
python3 transform.py
```
### 6. Start the Flask API
```Bash
cd api
python3 app.py
```

### 7. Run the frontend
```Bash
cd frontend
npm install
npm run dev
```

## Author
Kgosi-E-tsile Magano
