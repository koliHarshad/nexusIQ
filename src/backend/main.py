import etl_pipeline
import ai_analyst
import reporter

def run_nexus_pipeline():

    # etl_pipeline.etl_pipeline()
    story_clusters = ai_analyst.run_investigation()
    final_report = reporter.create_narrative(story_clusters)
    print(f"{final_report}")

if __name__ == "__main__":
    run_nexus_pipeline()