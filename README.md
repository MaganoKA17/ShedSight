# ShedSight

A data analytics application that tracks, stores, and analyzes South African load shedding data, and uses AI to
surface insightsthat raw schedules cannot show you.

## Problem Statement

South Africans lack a clear, data-driven picture of how load shedding affects their lives over time. ShedSight solves this y building a pipeline that collects, transformsand analyzes real Eskom data.

## Features
- Ingests real Eskom outage data (hourly and weekly)
- Stores raw and transformed data in Supabase (PostgreSQL)
- Transforms raw data into meaningful metrics
- Uses Google Gemini AI to generate natural language insights
- React dashboard for data visualisations

## Tech Stack

| Layer | Tool |
|---|---|
| Data Source | Eskom Open Data Portal |
| Pipeline | Python |
| Database | Supabase (PostgreSQL) |
| AI Layer | Google Gemini API |
| Frontend | React + Vite (coming soon) |

## Project Structure

shedsight/
├── ai
│   └── insights.py
├── frontend
├── pipeline
│   ├── __pycache__
│   ├── config.py
│   ├── hourly_UCLF_and_OCLF_trend.csv
│   ├── ingestion.py 
│   ├── transform.py
│   └── weekly_unplanned_outages.csv
├── sql
|   └── schema.sql
└── README.md