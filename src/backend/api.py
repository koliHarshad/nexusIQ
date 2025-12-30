import duckdb
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
        return {"error fetching data from database": str(e)}