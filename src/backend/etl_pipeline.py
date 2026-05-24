# Handles the Extraction, Transformation, and Loading of raw forensic reports into the database.

import pandas as pd
import duckdb
import json
import re
import os
import chromadb
from chromadb.utils import embedding_functions

def etl_pipeline():
    print("🚀 Starting ETL Pipeline...")

    extract()

def extract():
    print("extracting sales data...")
    try:
        # Load Sales Data-

        # JSON to python list
        with open("src/raw_data/sales_data.json", 'r') as f:
            sales_data = json.load(f)
        # python list to DataFrame
        df_sales = pd.DataFrame(sales_data)

        # Connect to DuckDB and write
        con = duckdb.connect("src/database/nexus.duckdb")
        con.execute("CREATE OR REPLACE TABLE sales_data AS SELECT * FROM df_sales ")
        print(f"   ✅ Loaded {len(df_sales)} sales records into DuckDB.")
        con.close()

    except Exception as e:
        print(f" Error processing sales data: {e}")


    print("extracting server logs...")
    log_pattern = re.compile(r'\[(.*?)\] (.*?) \[(.*?)\] (.*?) (.*?) HTTP/1.1 (.*?) - Latency: (.*?)ms')
    parsed_logs = []
    try:
        # Load Server Logs -
        with open("src/raw_data/server_logs.txt", "r") as f:
            for line in f:
                match = log_pattern.search(line)
                if match:
                    parsed_logs.append({
                        "timestamp": match.group(1),
                        "ip_address": match.group(2),
                        "level": match.group(3),
                        "method": match.group(4),
                        "endpoint": match.group(5),
                        "status_code": int(match.group(6)),
                        "latency": int(match.group(7))
                    })
        # Convert parsed logs to DataFrame
        df_server_logs = pd.DataFrame(parsed_logs)

        # Connect to DuckDB and write
        con = duckdb.connect("src/database/nexus.duckdb")
        con.execute("CREATE OR REPLACE TABLE server_logs AS SELECT * FROM df_server_logs")
        print(f"   ✅ Loaded {len(df_server_logs)} server logs into DuckDB.")
        con.close()

    except Exception as e:
        print(f" Error processing server logs: {e}")
    

    print("extracting social media data...")
    try:
        # Load Social Media Data 
        df_social = pd.read_csv("src/raw_data/social_media.csv")

        # Initialize ChromaDB Client
        chroma_client = chromadb.PersistentClient("src/database/chromadb")
        # Use default embedding function (all-MiniLM-L6-v2) - runs locally, no API key needed yet
        collection = chroma_client.get_or_create_collection(name="social_posts")
        
        # 3. Add to Vector DB
        # We store the 'text' as the document, and other fields as metadata
        documents = df_social['text'].tolist()
        metadatas = df_social[['timestamp', 'platform', 'sentiment_score']].to_dict(orient='records')
        ids = [str(x) for x in df_social['tweet_id'].tolist()]
        
        # Clean previous run data, prevents duplicates
        if collection.count() > 0:
            collection.delete(collection.get()['ids'])

        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        con = duckdb.connect("src/database/nexus.duckdb")
        con.execute("CREATE OR REPLACE TABLE social_media AS " \
                         "SELECT tweet_id, timestamp, platform, sentiment_score " \
                         "FROM df_social")
        
        print(f"   ✅ Loaded {len(df_social)} social media metadata into ChromaDB and DuckDB.")
        con.close()

    except Exception as e:
        print(f" Error processing social media data: {e}")

        