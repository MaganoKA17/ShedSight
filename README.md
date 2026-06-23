# ShedSight

A data analytics application that tracks, stores, and analyzes South African load shedding data, and uses AI to
surface insights that raw schedules cannot show you.

## Problem Statement

South Africans lack a clear, data-driven picture of how load shedding affects their lives over time. ShedSight solves this by building a pipeline that collects, transforms and analyzes real Eskom data, then displays it on an interactive dashboard.

## Target Audience
- Households wanting to understand their power loss over time
- Small businesses owners making decisions about backup power
- Students and remote workers planning around outages
- Researchers and journalists studying load shedding impacts

## Features
- Ingests real Eskom outage data (hourly and weekly)
- Stores raw and transformed data in Supabase (PostgreSQL)
- Transforms raw data into meaningful daily summaries
- AI-powered insights via Google Gemini (coming soon)
- Interactive React dashboard with charts and stat cards

## Tech Stack

| Layer | Tool |
|---|---|
| Data Source | Eskom Open Data Portal |
| Pipeline | Python |
| Database | Supabase (PostgreSQL) |
| AI Layer | Google Gemini API |
| Frontend | React + Vite |
| Deployment | Vercel (coming soon) |

## Project Structure

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

## Setup

### 1. Clone the repo
```Bash
git clone git@github.com:YOURUSERNAME/shedsight.git
cd ShedSight
```

### 2. Install Dependencies
```Bash
pip install supabase requests python-dotenv google-genai
```

### 3. Set up environment variables
```Bash
cp .env.example .env
```
Fill in your keys in '.env'

### 4. Run the pipeline
```Bash
cd pipeline
python3 ingestion.py
python3 transform.py
```

### 5. Run the frontend
```Bash
cd frontend
npm install
npm run dev
```

## Data Source

Data was sourced from [Eskom Open Data Portal](https://www.eskom.co.za/dataportal), specifically the hourly and weekly UCLF+OCLF outage datasets.

UCLF+OCLF = Unplanned Capacity Loss Factor + Outage Capacity Loss Factor.
Higher values indicate more severe load shedding conditions.

## Author

Kgosi-E-tsile Magano
