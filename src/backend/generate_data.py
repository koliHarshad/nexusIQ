import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import os

# 1. Setup
fake = Faker()
OUTPUT_DIR = "./src/raw_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define our timeline (7 days of data)
start_date = datetime(2023, 10, 10)
end_date = datetime(2023, 10, 17)
hours = int((end_date - start_date).total_seconds() / 3600)
timestamps = [start_date + timedelta(hours=i) for i in range(hours)]

# Storage lists
sales_data = []
log_data = []
social_data = []

print(f"Generating data for {len(timestamps)} hours...")

# 2. The Simulation Loop
for ts in timestamps:
    # --- SCENARIO LOGIC: The "Crash" happens on Oct 12 between 2PM and 6PM ---
    is_crash = (ts.day == 12) and (14 <= ts.hour <= 18)

    # --- A. SALES DATA (The Money) ---
    if is_crash:
        # Crash: Revenue tanks to $500-$1000
        revenue = random.uniform(500, 1000)
        transactions = random.randint(10, 50)
    else:
        # Normal: Revenue is healthy $5000-$8000
        revenue = random.uniform(5000, 8000)
        transactions = random.randint(200, 500)
    
    sales_data.append({
        "timestamp": ts,
        "revenue": round(revenue, 2),
        "transactions": transactions
    })

    # --- B. SERVER LOGS (The Tech) ---
    if is_crash:
        # Crash: Massive spike in 500 Errors
        error_count = random.randint(300, 800)
        avg_latency = random.uniform(2000, 5000) # 2-5 seconds (Slow!)
    else:
        # Normal: Healthy system
        error_count = random.randint(0, 5)
        avg_latency = random.uniform(50, 150) # Fast
        
    log_data.append({
        "timestamp": ts,
        "error_count": error_count,
        "avg_latency_ms": round(avg_latency, 2)
    })

    # --- C. SOCIAL SENTIMENT (The Vibe) ---
    # We generate 5 sample tweets per hour to represent the "mood"
    if is_crash:
        sentiment_score = random.uniform(-0.9, -0.4) # Very Negative
        keywords = ["broken", "stuck", "error", "fail", "slow", "checkout", "money gone"]
        tweet_text = f"{fake.sentence()} {random.choice(keywords)}! {random.choice(keywords)}."
    else:
        sentiment_score = random.uniform(0.2, 0.9) # Positive/Neutral
        keywords = ["love", "fast", "great", "smooth", "thanks", "working"]
        tweet_text = f"{fake.sentence()} {random.choice(keywords)}."

    social_data.append({
        "timestamp": ts,
        "sentiment_score": round(sentiment_score, 2),
        "sample_tweet": tweet_text
    })

# 3. Save to CSV
pd.DataFrame(sales_data).to_csv(f"{OUTPUT_DIR}/sales_data.csv", index=False)
pd.DataFrame(log_data).to_csv(f"{OUTPUT_DIR}/server_logs.csv", index=False)
pd.DataFrame(social_data).to_csv(f"{OUTPUT_DIR}/social_media.csv", index=False)

print(f"✅ Data generation complete! Files saved to {OUTPUT_DIR}/")