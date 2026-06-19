
CREATE TABLE raw_hourly_outages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    datetime_key TEXT NOT NULL,
    datetime_hour_beginning TIMESTAMPTZ NOT NULL,
    hourly_uclf_oclf NUMERIC(10,4) NOT NULL,
    inserted_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE raw_weekly_outages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    week_date TEXT NOT NULL,
    min_uclf_oclf NUMERIC(10,4) NOT NULL,
    avg_uclf_oclf NUMERIC(10,4) NOT NULL,
    max_uclf_oclf NUMERIC(10,4) NOT NULL,
    inserted_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE daily_outage_summary (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    date DATE NOT NULL,
    avg_uclf_oclf NUMERIC(10,4) NOT NULL,
    max_uclf_oclf NUMERIC(10,4) NOT NULL,
    high_stress_hours INT NOT NULL,
    inserted_at TIMESTAMPTZ DEFAULT NOW()
);