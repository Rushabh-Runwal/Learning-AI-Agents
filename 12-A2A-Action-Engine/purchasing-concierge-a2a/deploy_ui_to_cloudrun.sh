#!/bin/bash

# Deploy Purchasing Concierge UI to Cloud Run

# Exit on error
set -e

# Load environment variables
source .env

echo "🚀 Deploying Purchasing Concierge UI to Cloud Run..."
echo ""

# Deploy using gcloud run deploy
gcloud run deploy purchasing-concierge-ui \
  --source . \
  --region ${GOOGLE_CLOUD_LOCATION} \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=${GOOGLE_GENAI_USE_VERTEXAI} \
  --set-env-vars GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT} \
  --set-env-vars GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION} \
  --set-env-vars AGENT_ENGINE_RESOURCE_NAME=${AGENT_ENGINE_RESOURCE_NAME}

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Your Gradio UI is now available at the URL shown above."
