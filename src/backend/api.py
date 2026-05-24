# API endpoints for NexusIQ backend. 
# This module defines the RESTful API using FastAPI to serve the latest incident report, dashboard metrics, and incident history to the React frontend.

import duckdb
import json
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

app = FastAPI()

# Allow your React App to talk to this API
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/latest-report")
def get_latest_report():
    try:
        # 1. fetch the data from db

        # Connect in Read-Only mode to avoid locking
        con = duckdb.connect("src/database/nexus.duckdb", read_only=True)

        query = """
            SELECT id, timestamp, ai_report, story_clusters
            FROM incident_reports
            ORDER BY timestamp DESC
            LIMIT 1
        """
        result = con.execute(query).fetchone()
        con.close()

        # 2. unpack the data for easy handling for frontend
        if not result:
            return {"error": "No reports found"}
        
        inc_id, timestamp, report_raw, clusters_raw = result
        # convert json strings back to python objects
        report_data = json.loads(report_raw)
        clusters_list = json.loads(clusters_raw)

        return {
            "id": inc_id,
            "timestamp": timestamp,
            "verdictTitle": "Sales Trend Analysis",
            "verdictStatus": "Critical",
            "verdictText": report_data.get("verdict", "No verdict available."),
            "timelineText": report_data.get("timeline", "No timeline available."),
            "recommendedActions": report_data.get("actions", "Couldn't provide recommended actions."),
            "clusters": clusters_list
        }

    except Exception as e:
        return {"error fetching report from database": str(e)}
    
@app.get("/api/dashboard-metrics")
def get_dashboard_metrics(timestamp: str = Query(None)):
    try:
        print(f"Fetching dashboard metrics for anchor time: {timestamp}")
        con = duckdb.connect("src/database/nexus.duckdb", read_only=True)

        if timestamp:
            anchor_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        else: 
            print("⚠️ No anchor time provided, defaulting to latest incident.")
            res = con.execute("SELECT story_clusters FROM incident_reports ORDER BY timestamp DESC LIMIT 1").fetchone()
            if not res: return {"error": "No data"}
            clusters = json.loads(res[0])
            anchor_dt = datetime.strptime(clusters[0]['anchor']['time'], "%Y-%m-%d %H:%M:%S")

        # 7 days window
        start_dt = anchor_dt - timedelta(days=7)
        if anchor_dt + timedelta(days=1):
            end_dt = anchor_dt + timedelta(days=1)
        else:
            end_dt = anchor_dt
        
        sales_query = f"""
            SELECT date_trunc('hour', timestamp::TIMESTAMP)AS time,
            SUM(amount) AS total_sales
            FROM sales_data
            WHERE timestamp BETWEEN '{start_dt}' AND '{end_dt}'
            GROUP BY time
            ORDER BY time ASC"""
        sales_data = con.execute(sales_query).fetchall()

        log_query = f""" 
            SELECT date_trunc('hour', timestamp::TIMESTAMP) AS time,
            COUNT(*) AS error_count
            FROM server_logs
            WHERE level = 'ERROR' AND timestamp BETWEEN '{start_dt}' AND '{end_dt}'
            GROUP BY time
            ORDER BY time ASC"""
        logs_data = con.execute(log_query).fetchall()

        social_query = f"""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN sentiment_score < 0 THEN 1 ELSE 0 END) as negative,
                SUM(CASE WHEN sentiment_score >= 0 THEN 1 ELSE 0 END) as positive
            FROM social_media
            WHERE timestamp BETWEEN '{start_dt}' AND '{end_dt}'
            """
        social_stats = con.execute(social_query).fetchone()
        
        con.close()        

        # Format for Frontend (List of Dictionaries)
        return {
            "sales_trend": [{"time": str(r[0]), "revenue": r[1]} for r in sales_data],
            "error_trend": [{"time": str(r[0]), "count": r[1]} for r in logs_data],
            "sentiment": {
                "total": social_stats[0],
                "negative": social_stats[1],
                "positive": social_stats[2]
            }
        }

    except Exception as e:
        return {"error fetching dashboard metrics": str(e)}    

@app.get("/api/incident-history")
def get_incident_history():
    try:
        con = duckdb.connect("src/database/nexus.duckdb", read_only=True)
        query = """ 
            SELECT id, timestamp, ai_report, story_clusters
            FROM incident_reports
            ORDER BY timestamp DESC"""
        
        data = con.execute(query).fetchall()
        con.close()

        history = []
        for row in data:
            history.append({
                "id": row[0],
                "timestamp": str(row[1]),
                "summary_report":json.loads(row[2]),
                "raw_logs": json.loads(row[3])
            })

        return history
    
    except Exception as e:
        return {"error fetching incident history": str(e)}