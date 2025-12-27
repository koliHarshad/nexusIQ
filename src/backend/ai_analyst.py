import duckdb
import pandas as pd
import numpy as np
from datetime import timedelta

DB_PATH = "src/database/nexus.duckdb"

def get_data_as_dataframe(query):
    """Helper to get DuckDB data into Pandas for analysis"""
    con = duckdb.connect(DB_PATH)
    df = con.execute(query).df()
    con.close()
    return df

# --- DETECTOR 1: Sales data---
def scan_sales_anomalies():
    print("   Scanning Sales...")
    query = """ 
        SELECT date_trunc('hour', timestamp::TIMESTAMP) as time,
        SUM(amount) as value
        FROM sales_data
        GROUP BY time
        ORDER BY time ASC"""

    df_sales = get_data_as_dataframe(query)

    if df_sales.empty:
        return []
    
    df_sales['moving_avg'] = df_sales['value'].rolling(window=6).mean() # 6-hour moving average
    df_sales['is_anomaly'] = df_sales['value'] < (df_sales['moving_avg'].shift(1) * 0.7)  # 30% drop = anomaly

    events = []
    for index, row in df_sales[df_sales['is_anomaly']].iterrows():
        events.append({
            "time": row['time'],
            "type": "REVENUE_DROP",
            "details": f"Revenue ${row['value']:.2f} (Expected ~${row['moving_avg']:.2f})"
        })
    return events

# --- DETECTOR 2: Server Log Data ---
def scan_log_anomalies():
    print("   Scanning Server Logs...")
    query = """
        SELECT date_trunc('hour', timestamp::TIMESTAMP) as time, COUNT(*) as error_count
        FROM server_logs
        WHERE level = 'ERROR'
        GROUP BY time
        HAVING error_count > 10  -- Threshold for "Weird"
        ORDER BY time ASC
    """
    df_logs = get_data_as_dataframe(query)

    events = []
    for index, row in df_logs.iterrows():
        events.append({
            "time": row['time'],
            "type": "ERROR_SPIKE",
            "details": f"{row['error_count']} Errors detected"
        })
    return events

# --- DETECTOR 3: Social Sentiment Data ---
def scan_social_anomalies():
    return []  

def incident_correlation(sales_events, log_events, social_events):
    """
        chooses an anchor event (here, sales drop) 
        looks for candidate root causes from log events and social events 
        by filtering out the events that occurred within a time window around the anchor event.
    """
    incidents = []

    for sales in sales_events:
        if sales["type"] == "REVENUE_DROP":

            incident = {
                "anchor": sales,
                "candidate_log_events": [],
                "candidate_social_events": [],
                "start_time": sales["time"],
                "end_time": sales["time"]
            }

            # for a particular sales drop, will look for root cause candidates in the +-24 hours window
            lookback_window = sales["time"] - timedelta(hours=24)
            lookforward_window = sales["time"] + timedelta(hours=24)

            for log in log_events:
                # will consider logs as potential root causes candidates if they occurred within the lookback window
                if lookback_window <= log["time"] <= sales["time"]:
                    incident["candidate_log_events"].append(log)
                    # Update incident start time if log happened earlier
                    if log['time'] < incident['start_time']:
                        incident['start_time'] = log['time']

            for social in social_events:
                # will consider social events as potential fallout if they occurred within the lookback and lookforward window 
                # i.e., 24 hours before or after the sales drop
                if lookback_window <= social["time"] <= lookforward_window:
                    incident["candidate_social_events"].append(social)
                    if social['time'] > incident['end_time']:
                        incident['end_time'] = social['time']
            
            if incident['candidate_log_events'] or incident['candidate_social_events']:
                incidents.append(incident)

    return incidents

def run_investigation():
    print("🕵️  AI Detective Starting Independent Scans...")
    
    # 1. Gather distinct clues
    sales_events = scan_sales_anomalies()
    log_events = scan_log_anomalies()
    social_events = scan_social_anomalies()
    
    # 2. Find the Story (Cluster them)
    story_clusters = incident_correlation(sales_events, log_events, social_events)
    
    # 3. Report
    print(f"\n🧩  Identified {len(story_clusters)} Unique Incidents:")
    for i, chain in enumerate(story_clusters):
        print(f"  ⚓ ANCHOR EVENT:       [{chain['anchor']['time']}] {chain['anchor']['details']}")

        for root in chain['candidate_log_events']:
            lag = root['time'] - chain['anchor']['time']
            print(f"  🔥ROOT CAUSE CANDIDATES ({lag}): [{root['time']}] {root['details']}")
                    
        # Print Fallout
        for fallout in chain['candidate_social_events']:
            lag = fallout['time'] - chain['anchor']['time']
            print(f"  🗣️ FALLOUT (+{lag}):   [{fallout['time']}] {fallout['details']}")
if __name__ == "__main__":
    run_investigation()