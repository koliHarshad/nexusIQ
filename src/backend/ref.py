import pandas as pd
import duckdb
import json
import re
import os
import chromadb
from chromadb.utils import embedding_functions

# 1. Setup & Config
RAW_DIR = "./src/raw_data"        # Where generator puts files
DB_PATH = "./src/database/nexus.duckdb" # Where DuckDB saves
CHROMA_PATH = "./src/database/chroma_db" # Where ChromaDB saves

# Make sure DB directory exists
os.makedirs("./src/database", exist_ok=True)

print("🚀 Starting ETL Pipeline...")

# ---------------------------------------------------------
# TASK A: Process Sales Data (JSON -> DuckDB)
# ---------------------------------------------------------
print("🔹 Processing Sales Data (JSON)...")
try:
    with open(f"{RAW_DIR}/sales_data.json", 'r') as f:
        sales_data = json.load(f)
    
    # Flatten/Normalize: Turn list of dicts into DataFrame
    df_sales = pd.DataFrame(sales_data)
    
    # Connect to DuckDB and write
    con = duckdb.connect(DB_PATH)
    con.execute("CREATE TABLE IF NOT EXISTS sales AS SELECT * FROM df_sales LIMIT 0")
    # Using 'INSERT OR IGNORE' logic (simplistic version: drop & replace for this demo)
    con.execute("DROP TABLE IF EXISTS sales")
    con.execute("CREATE TABLE sales AS SELECT * FROM df_sales")
    
    print(f"   ✅ Loaded {len(df_sales)} sales records into DuckDB.")
    con.close()
except Exception as e:
    print(f"   ❌ Error processing sales: {e}")

# ---------------------------------------------------------
# TASK B: Process Server Logs (Raw Text -> Regex -> DuckDB)
# ---------------------------------------------------------
print("🔹 Processing Server Logs (Regex Parsing)...")
log_pattern = re.compile(r'\[(.*?)\] (.*?) \[(.*?)\] (.*?) (.*?) (.*?) - Latency: (.*?)ms')

parsed_logs = []
try:
    with open(f"{RAW_DIR}/server_logs.txt", 'r') as f:
        for line in f:
            match = log_pattern.search(line)
            if match:
                parsed_logs.append({
                    "timestamp": match.group(1),
                    "ip_address": match.group(2),
                    "level": match.group(3),
                    "method": match.group(4).split()[0], # Extract 'GET' from 'GET /api...'
                    "endpoint": match.group(4).split()[1], # Extract '/api'
                    "status_code": int(match.group(6)),
                    "latency": int(match.group(7))
                })

    df_logs = pd.DataFrame(parsed_logs)
    
    # Load into DuckDB
    con = duckdb.connect(DB_PATH)
    con.execute("DROP TABLE IF EXISTS logs")
    con.execute("CREATE TABLE logs AS SELECT * FROM df_logs")
    print(f"   ✅ Parsed & Loaded {len(df_logs)} log lines into DuckDB.")
    con.close()

except Exception as e:
    print(f"   ❌ Error processing logs: {e}")

# ---------------------------------------------------------
# TASK C: Process Social Media (CSV -> Vector DB)
# ---------------------------------------------------------
print("🔹 Processing Social Media (Embeddings)...")
try:
    # 1. Read CSV
    df_social = pd.read_csv(f"{RAW_DIR}/social_media.csv")
    
    # 2. Setup ChromaDB (Local Persistent)
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # Use default embedding function (all-MiniLM-L6-v2) - runs locally, no API key needed yet
    collection = chroma_client.get_or_create_collection(name="social_posts")
    
    # 3. Add to Vector DB
    # We store the 'text' as the document, and other fields as metadata
    documents = df_social['text'].tolist()
    metadatas = df_social[['timestamp', 'platform', 'sentiment_score']].to_dict(orient='records')
    ids = [str(x) for x in df_social['tweet_id'].tolist()]
    
    # Clean previous run data (optional, prevents duplicates for this demo)
    if collection.count() > 0:
        collection.delete(collection.get()['ids'])

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"   ✅ Vectorized {len(documents)} tweets into ChromaDB.")

except Exception as e:
    print(f"   ❌ Error processing social: {e}")

print("🎉 ETL Pipeline Complete!")