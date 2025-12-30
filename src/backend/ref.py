import duckdb
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your React App to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development. In prod, use ["http://localhost:5173"]
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "nexus_iq.duckdb"

@app.get("/api/latest-report")
def get_latest_report():
    try:
        # Connect in Read-Only mode to avoid locking
        con = duckdb.connect(DB_PATH, read_only=True)
        
        # Get the latest report
        query = """
            SELECT id, timestamp, report_json, story_clusters 
            FROM incident_reports 
            ORDER BY timestamp DESC 
            LIMIT 1
        """
        result = con.execute(query).fetchone()
        con.close()

        if not result:
            return {"error": "No reports found"}

        # Unpack the Tuple
        inc_id, timestamp, report_raw, clusters_raw = result

        # Parse JSON strings back into Python Objects
        # This restores the structure created by the Parser in Part 1
        report_data = json.loads(report_raw)
        clusters_list = json.loads(clusters_raw)

        # Return clean JSON for Frontend
        return {
            "id": inc_id,
            "timestamp": timestamp,
            "verdictTitle": "Critical Incident Analysis", # Dynamic or Fixed title
            "verdictStatus": "Critical",
            "verdictText": report_data.get("verdict", "No verdict available."),
            "timelineText": report_data.get("timeline", "No timeline available."),
            "recommendedActions": report_data.get("actions", []),
            "clusters": clusters_list
        }

    except Exception as e:
        return {"error": str(e)}

# Run with: uvicorn api_server:app --reload