import duckdb
import chromadb
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

def _fetch_tweet_context(start_time, end_time):
    """
    INTERNAL TOOL: Fetches tweets for a specific time window.
    """
    # 1. Get IDs from DuckDB
    query = f"""
        SELECT tweet_id FROM social_media
        WHERE timestamp >= '{start_time}' 
          AND timestamp <= '{end_time}'
          AND sentiment_score < 0
        ORDER BY sentiment_score ASC 
        LIMIT 4 -- Low limit to keep the prompt short
    """
    
    ids = []
    try:
        with duckdb.connect("src/database/nexus.duckdb") as con:
            df = con.execute(query).df()
            if df.empty: return []
            ids = [str(x) for x in df['tweet_id'].tolist()]
    except Exception:
        return []

    # 2. Get Text from ChromaDB
    try:
        client = chromadb.PersistentClient("src/database/chromadb")
        collection = client.get_collection(name="social_posts")
        results = collection.get(ids=ids)
        return results['documents'] if results['documents'] else []
    except Exception:
        return []

def create_narrative(story_clusters):
    """
    unpack the list of story clusters (incidents) into proper format for LLM consumption.
    creates a single list of incidents and their details and calls the LLM to generate a narrative report.

    also does the work of attaching the social media context to each incident by calling the _fetch_tweet_context tool.
    """

    if not story_clusters:
        return "No significant incidents detected."
    
    # --- STEP 1: Build the Master Timeline which includes all incidents ---
    timeline_evidence = []
    for i, incident in enumerate(story_clusters):

        anchor = incident['anchor']
        
        # 1. Format Technical Context
        if incident['candidate_log_events']:
             # We list all errors found for this specific anchor
            tech_details = "; ".join([f"{log['details']}" for log in incident['candidate_log_events']])
        else:
            tech_details = "No significant log events found."

        # 2. Format Social Media Context
        social_snippets = []
        if incident['candidate_social_events']:
            s_start = incident['candidate_social_events'][0]['time']
            s_end = incident['candidate_social_events'][-1]['time']
            social_snippets = _fetch_tweet_context(s_start, s_end)
        
        social_text = f"User Quotes: {social_snippets}" if social_snippets else "No specific quotes."

        # 3. Add to Master Timeline
        entry = f"""
        EVENT #{i+1}:
        - Time: {anchor['time']}
        - Impact: Revenue dropped. {anchor['details']}
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
    1. DIAGNOSE PERSISTENCE: Look at the timestamps. Is this a sequence of unrelated glitches, or one continuous outage that kept triggering alarms?
    2. NAME THE CULPRIT: You MUST explicitly mention the specific failing endpoint (e.g. '/api/checkout') and error code (e.g. 500) if visible in the logs. Do not be vague.
    3. VERIFY WITH SOCIALS: Do the user quotes validate the logs? (e.g., If logs say '/login' failed, do users mention "logging in"?).
    4. STYLE: Be direct. No "It seems that". State the facts.
    
    OUTPUT FORMAT:
    - VERDICT: (One sentence summary including the specific endpoint and total impact)
    - TIMELINE ANALYSIS: (Explain how the incident started and progressed)
    - RECOMMENDED ACTION: (What specific service/endpoint needs fixing?)
    """
    # --- STEP 3: Invoke AI ---
    try:
        print(" Connecting to LLM...")
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        response = llm.invoke([HumanMessage(content=prompt_content)])
        return response.content
    except Exception as e:
        return f"⚠️ AI Analysis Failed: {e}"
