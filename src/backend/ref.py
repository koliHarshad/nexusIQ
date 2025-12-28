import duckdb
import chromadb
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "./src/database/nexus.duckdb"
CHROMA_PATH = "./src/database/chromadb"

def _fetch_tweet_context(start_time, end_time):
    """
    INTERNAL TOOL: Fetches tweets for a specific time window.
    """
    # 1. Get IDs from DuckDB
    query = f"""
        SELECT tweet_id FROM social_media
        WHERE timestamp >= '{start_time}' 
          AND timestamp <= '{end_time}'
          AND sentiment_score < -0.2
        ORDER BY sentiment_score ASC 
        LIMIT 2 -- Low limit to keep the prompt short
    """
    
    ids = []
    try:
        with duckdb.connect(DB_PATH) as con:
            df = con.execute(query).df()
            if df.empty: return []
            ids = [str(x) for x in df['tweet_id'].tolist()]
    except Exception:
        return []

    # 2. Get Text from ChromaDB
    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = client.get_collection(name="social_posts")
        results = collection.get(ids=ids)
        return results['documents'] if results['documents'] else []
    except Exception:
        return []

def generate_system_report(incidents_list):
    """
    PUBLIC TOOL: The 'Chief Investigator'.
    Takes the FULL LIST of incidents to find patterns across time.
    """
    print(f"   [Reporter] 🧠 Analyzing {len(incidents_list)} incidents for global patterns...")
    
    if not incidents_list:
        return "No anomalies detected. System is healthy."

    # --- STEP 1: Build the Master Timeline ---
    timeline_evidence = []
    
    for i, incident in enumerate(incidents_list):
        anchor = incident['anchor']
        
        # A. Format Technical Context
        if incident['root_cause_candidates']:
            # We list all errors found for this specific anchor
            tech_details = "; ".join([f"{log['details']}" for log in incident['root_cause_candidates']])
        else:
            tech_details = "No Error Logs"

        # B. Fetch Social Context (Just-In-Time)
        social_snippets = []
        if incident['social_fallout']:
            s_start = incident['social_fallout'][0]['time']
            s_end = incident['social_fallout'][-1]['time']
            social_snippets = _fetch_tweet_context(s_start, s_end)
        
        social_text = f"User Quotes: {social_snippets}" if social_snippets else "No specific quotes."

        # C. Add to Master Timeline
        entry = f"""
        EVENT #{i+1}:
        - Time: {anchor['time']}
        - Impact: Revenue down by {anchor['details']}
        - Logs: {tech_details}
        - Social: {social_text}
        """
        timeline_evidence.append(entry)

    full_timeline_str = "\n".join(timeline_evidence)

    # --- STEP 2: The "Pattern Recognition" Prompt ---
    prompt_content = f"""
    ACT AS: Chief Technology Officer (CTO).
    
    TASK: Analyze this series of system anomalies.
    
    RAW TIMELINE:
    {full_timeline_str}
    
    INSTRUCTIONS:
    1. Pattern Recognition: Is this a single continuous outage or separate random incidents?
    2. Root Cause: If the same error appears across multiple events, identify it as the primary culprit.
    3. User Sentiment: Are users reacting to the specific error?
    
    OUTPUT FORMAT:
    - SUMMARY: (1 sentence high-level verdict)
    - TIMELINE ANALYSIS: (Briefly explain the progression of the failure)
    - ACTION ITEM: (What should the team fix first?)
    """

    # --- STEP 3: Invoke AI ---
    try:
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        response = llm.invoke([HumanMessage(content=prompt_content)])
        return response.content
    except Exception as e:
        return f"⚠️ AI Analysis Failed: {e}"