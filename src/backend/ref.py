import duckdb
import pandas as pd
from datetime import timedelta

DB_PATH = "./src/database/nexus.duckdb"

def get_data_as_dataframe(query):
    with duckdb.connect(DB_PATH) as con:
        df = con.execute(query).df()
    return df

# --- DETECTOR 1: FINANCIALS (The one we already have) ---
def scan_sales_anomalies():
    print("   Scanning Sales...")
    query = """
        SELECT date_trunc('hour', timestamp::TIMESTAMP) as time, SUM(amount) as value
        FROM sales GROUP BY time ORDER BY time ASC
    """
    df = get_data_as_dataframe(query)
    if df.empty: return []

    df['moving_avg'] = df['value'].rolling(window=6).mean()
    df['is_anomaly'] = df['value'] < (df['moving_avg'].shift(1) * 0.7)
    
    # Return list of anomalies
    events = []
    for index, row in df[df['is_anomaly']].iterrows():
        events.append({
            "time": row['time'],
            "type": "REVENUE_DROP",
            "details": f"Revenue ${row['value']:.2f} (Expected ~${row['moving_avg']:.2f})"
        })
    return events

# --- DETECTOR 2: INFRASTRUCTURE (New!) ---
def scan_log_anomalies():
    print("   Scanning Server Logs...")
    # Logic: Find hours where error count > 50 (or any threshold)
    query = """
        SELECT date_trunc('hour', timestamp::TIMESTAMP) as time, COUNT(*) as error_count
        FROM logs
        WHERE level = 'ERROR'
        GROUP BY time
        HAVING error_count > 10  -- Threshold for "Weird"
        ORDER BY time ASC
    """
    df = get_data_as_dataframe(query)
    
    events = []
    for index, row in df.iterrows():
        events.append({
            "time": row['time'],
            "type": "ERROR_SPIKE",
            "details": f"{row['error_count']} Errors detected"
        })
    return events

# --- DETECTOR 3: SOCIAL SENTIMENT (New!) ---
# (For now, we simulate this query since we might not have vector logic fully hooked up yet)
def scan_social_anomalies():
    # In a real scenario, this queries ChromaDB or a 'sentiment' table
    # For now, let's return an empty list or a mock event to test the cluster engine
    return [] 

# --- THE CLUSTER ENGINE (The "Relation Finder") ---
def correlate_events(all_events):
    if not all_events:
        return []
    
    # 1. Sort everything by time
    all_events.sort(key=lambda x: x['time'])
    
    clusters = []
    current_cluster = [all_events[0]]
    
    # 2. Group events that are within 3 hours of each other
    for event in all_events[1:]:
        last_event_time = current_cluster[-1]['time']
        if event['time'] - last_event_time <= timedelta(hours=3):
            current_cluster.append(event)
        else:
            clusters.append(current_cluster)
            current_cluster = [event]
            
    clusters.append(current_cluster)
    return clusters

def run_investigation():
    print("🕵️  AI Detective Starting Independent Scans...")
    
    # 1. Gather distinct clues
    sales_events = scan_sales_anomalies()
    log_events = scan_log_anomalies()
    social_events = scan_social_anomalies()
    
    all_clues = sales_events + log_events + social_events
    print(f"   Found {len(all_clues)} suspicious events total.")
    
    # 2. Find the Story (Cluster them)
    story_clusters = correlate_events(all_clues)
    
    # 3. Report
    print(f"\n🧩  Identified {len(story_clusters)} Unique Incidents:")
    for i, cluster in enumerate(story_clusters):
        print(f"\n--- Incident #{i+1} ---")
        # Just print the raw timeline for now
        for event in cluster:
            print(f"   [{event['time']}] {event['type']}: {event['details']}")
            
        # PRO TIP: This 'cluster' list is exactly what we will feed to ChatGPT later!

if __name__ == "__main__":
    run_investigation()