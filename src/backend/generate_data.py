import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import os
import json

# 1. Setup
fake = Faker()
OUTPUT_DIR = "raw_data"
# If using Docker volume mapping to ./src/raw_data, ensure this path aligns with your container logic
# For the script running INSIDE Docker, "raw_data" (relative) usually works if WORKDIR is /app
# But based on your volume mapping:
# Local: ./src/database/raw_data  <--> Container: /app/src/raw_data
# We should write to:
OUTPUT_DIR = "./src/raw_data" 
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Configuration
start_date = datetime(2023, 10, 10)
end_date = datetime(2023, 10, 17)
hours = int((end_date - start_date).total_seconds() / 3600)
timestamps = [start_date + timedelta(hours=i) for i in range(hours)]

# Templates for realistic "Tech Twitter"
POSITIVE_TWEETS = [
    "Love the new UI update, so smooth!",
    "Checkout was instant today. Nice work.",
    "Customer support actually helped me. 5 stars.",
    "Best platform for buying widgets hands down.",
    "Just bought the annual plan. Worth every penny.",
    "App is flying today! 🚀",
]
NEGATIVE_TWEETS = [
    "Why is the checkout button greyed out??",
    "I keep getting 500 errors on login. Fix this!",
    "Is the site down? Can't load my dashboard.",
    "Charged twice for one item... DM me immediately.",
    "API is timing out. My workflow is broken.",
    "Worst update ever. Bring back the old version.",
    "Loading screen forever... #fail",
]

print(f"Generating rich data for {len(timestamps)} hours...")

sales_data = []
log_lines = [] # For TXT file
social_data = []

for ts in timestamps:
    # --- SCENARIO: The Crash (Oct 12, 2 PM - 6 PM) ---
    is_crash = (ts.day == 12) and (14 <= ts.hour <= 18)

    # ---------------------------------------------------------
    # A. SALES DATA (Complex JSON Structure)
    # ---------------------------------------------------------
    if is_crash:
        txn_count = random.randint(5, 15) # Low volume
        fail_rate = 0.8 # 80% failure rate
    else:
        txn_count = random.randint(50, 100)
        fail_rate = 0.05 # 5% failure rate

    for _ in range(txn_count):
        status = "FAILED" if random.random() < fail_rate else "COMPLETED"
        sales_data.append({
            "transaction_id": fake.uuid4(),
            "timestamp": ts.isoformat(),
            "product_category": random.choice(["Electronics", "SaaS_Sub", "Home_Goods"]),
            "amount": round(random.uniform(10.0, 500.0), 2),
            "payment_method": random.choice(["Credit_Card", "PayPal", "Stripe"]),
            "status": status,
            "region": random.choice(["US-East", "US-West", "EU-Central", "APAC"])
        })

    # ---------------------------------------------------------
    # B. SERVER LOGS (Raw Apache/Nginx Style Text)
    # ---------------------------------------------------------
    # Format: [TIMESTAMP] [IP] [LEVEL] [ENDPOINT] [STATUS] - Latency: Xms
    
    if is_crash:
        log_count = random.randint(200, 500) # Traffic spike (DDOS or panic reloads)
        error_prob = 0.9 # Mostly errors
    else:
        log_count = random.randint(20, 50)
        error_prob = 0.01

    for _ in range(log_count):
        if random.random() < error_prob:
            level = "ERROR"
            status = 500
            latency = random.randint(1000, 5000)
            endpoint = "/api/v1/checkout" # The broken endpoint
        else:
            level = "INFO"
            status = 200
            latency = random.randint(20, 150)
            endpoint = random.choice(["/home", "/login", "/products", "/contact"])

        # Construct a realistic log line
        log_line = f"[{ts.strftime('%Y-%m-%d %H:%M:%S')}] {fake.ipv4()} [{level}] GET {endpoint} HTTP/1.1 {status} - Latency: {latency}ms"
        log_lines.append(log_line)

    # ---------------------------------------------------------
    # C. SOCIAL MEDIA (Sentiment & Text)
    # ---------------------------------------------------------
    if is_crash:
        tweet_count = random.randint(10, 30) # Angry mob
        sentiment_bias = "negative"
    else:
        tweet_count = random.randint(2, 5)
        sentiment_bias = "positive"

    for _ in range(tweet_count):
        if sentiment_bias == "negative":
            text = random.choice(NEGATIVE_TWEETS)
            score = round(random.uniform(-0.9, -0.4), 2)
        else:
            text = random.choice(POSITIVE_TWEETS)
            score = round(random.uniform(0.4, 0.9), 2)
            
        social_data.append({
            "tweet_id": fake.random_number(digits=10),
            "timestamp": ts.strftime('%Y-%m-%d %H:%M:%S'),
            "user": f"@{fake.user_name()}",
            "text": text,
            "sentiment_score": score,
            "platform": "Twitter"
        })

# 3. Save Files in different formats
# JSON for Sales
with open(f"{OUTPUT_DIR}/sales_data.json", "w") as f:
    json.dump(sales_data, f, indent=4)

# TXT for Logs
with open(f"{OUTPUT_DIR}/server_logs.txt", "w") as f:
    f.write("\n".join(log_lines))

# CSV for Social
pd.DataFrame(social_data).to_csv(f"{OUTPUT_DIR}/social_media.csv", index=False)

print(f"✅ Rich data generation complete!")
print(f"   - Sales: JSON ({len(sales_data)} records)")
print(f"   - Logs: TXT ({len(log_lines)} lines)")
print(f"   - Social: CSV ({len(social_data)} tweets)")