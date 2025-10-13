"""
Cleanup script for Content Orchestration Agent
Deletes all deployed agent engines from Vertex AI
"""

import os
import sys
import vertexai
from dotenv import load_dotenv
from vertexai import agent_engines


def cleanup_deployments():
    """Delete all agent engine deployments"""
    load_dotenv()
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    bucket = os.getenv("GOOGLE_CLOUD_STAGING_BUCKET")
    
    if not project_id or not location or not bucket:
        print("❌ Missing required environment variables:")
        print("   GOOGLE_CLOUD_PROJECT")
        print("   GOOGLE_CLOUD_LOCATION")
        print("   GOOGLE_CLOUD_STAGING_BUCKET")
        sys.exit(1)
    
    # Initialize Vertex AI
    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=bucket,
    )
    
    print("\n" + "=" * 80)
    print("🧹 Cleanup: Content Orchestration Agent Deployments")
    print("=" * 80)
    print("\n🔄 Fetching all deployments...")
    
    try:
        deployments = agent_engines.list()
        
        if not deployments:
            print("✅ No deployments found. Nothing to clean up!")
            return
        
        print(f"\n⚠️  Found {len(deployments)} deployment(s) to delete:")
        for i, deployment in enumerate(deployments, 1):
            print(f"  {i}. {deployment.resource_name}")
        
        # Confirm deletion
        print("\n⚠️  WARNING: This will permanently delete all deployments!")
        confirm = input("Continue? (yes/no): ").strip().lower()
        
        if confirm not in ['yes', 'y']:
            print("❌ Cleanup cancelled.")
            return
        
        print("\n🔄 Deleting deployments...")
        for i, deployment in enumerate(deployments, 1):
            print(f"  [{i}/{len(deployments)}] Deleting {deployment.resource_name}...")
            try:
                remote_app = agent_engines.get(deployment.resource_name)
                remote_app.delete(force=True)
                print(f"  ✅ Deleted successfully!")
            except Exception as e:
                print(f"  ❌ Error deleting: {e}")
        
        print("\n✅ Cleanup complete!")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cleanup_deployments()

