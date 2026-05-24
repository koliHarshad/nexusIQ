# Main entry point for NexusIQ backend

import json
import uuid
import duckdb
from datetime import datetime
import etl_pipeline
import ai_analyst
import reporter


def parse_and_save(story_clusters, final_report):
    print("Parsing and saving the final report...")
    
    # parsing the final report

    if isinstance(final_report, str):
        final_report = final_report.split("\n")

    structured_report = {
        "verdict": "No verdict provided.",
        "timeline": "No timeline provided.",
        "actions": []
    }

    # takes one line, checks for headers - if present, updates the current section to that header
    # if there is no header, appends the line to whatever the current section
    current_section = None
    for line in final_report:
        clean_line = line.strip()
        if not clean_line: continue # Skip empty lines

        # --- CHECK FOR HEADERS ---
        # If we find a header, we switch the 'current_section' state
        if "**VERDICT:**" in clean_line or "VERDICT:" in clean_line:
            current_section = "verdict"
            # Remove the label and save the rest of the line (if any)
            content = clean_line.replace("**VERDICT:**", "").replace("VERDICT:", "").strip()
            if content: 
                structured_report["verdict"] = content
            continue

        elif "**TIMELINE ANALYSIS:**" in clean_line or "TIMELINE ANALYSIS:" in clean_line:
            current_section = "timeline"
            content = clean_line.replace("**TIMELINE ANALYSIS:**", "").replace("TIMELINE ANALYSIS:", "").strip()
            if content:
                structured_report["timeline"] = content
            continue
            
        elif "**RECOMMENDED ACTIONS:**" in clean_line or "RECOMMENDED ACTION" in clean_line:
            current_section = "actions"
            content = clean_line.replace("**RECOMMENDED ACTIONS:**", "").replace("RECOMMENDED ACTION:", "").strip()
            if content:
                structured_report["actions"] = content 
            continue

        # --- PROCESS CONTENT BASED ON CURRENT STATE ---
        # If it's not a header, append it to whatever section is active
        if current_section == "verdict":
            structured_report["verdict"] += " " + clean_line
            
        elif current_section == "timeline":
            structured_report["timeline"] += " " + clean_line
            
        elif current_section == "actions":
            structured_report["actions"] += " " + clean_line
    
    print("successfully parsed the final report.")
    

    # converting to json strings for storage
    final_report_json = json.dumps(structured_report)
    clusters_json = json.dumps(story_clusters, default=str)

    # connecting and saving to duckdb
    incident_id = f"INC-{uuid.uuid4().hex[:6].upper()}"

    try: 
        con = duckdb.connect("src/database/nexus.duckdb")
        con.execute("""
            CREATE TABLE IF NOT EXISTS incident_reports(
                    id VARCHAR PRIMARY KEY,
                    timestamp TIMESTAMP,
                    ai_report VARCHAR,
                    story_clusters JSON
            );
        """)
        con.execute(
            "INSERT INTO incident_reports VALUES (?, ?, ?, ?)",
            (incident_id,datetime.now(), final_report_json, clusters_json)
        )
        con.close()
        print(f"Saved report with ID: {incident_id}")

    except Exception as e:
        print(f"Error saving report to database: {e}")


def run_nexus_pipeline():

    # etl_pipeline.etl_pipeline()
    story_clusters = ai_analyst.run_investigation()
    final_report = reporter.create_narrative(story_clusters)

    parse_and_save(story_clusters, final_report)

if __name__ == "__main__":
    run_nexus_pipeline()