#!/bin/bash

# Source the .env file to get environment variables
if [ -f ".env" ]; then
  source .env
else
  echo "Error: .env file not found!"
  exit 1
fi

echo "🧪 Testing Agent Engine connection..."
echo "📋 Creating session..."
echo ""

curl -s \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://${GOOGLE_CLOUD_LOCATION}-aiplatform.googleapis.com/v1beta1/${AGENT_ENGINE_RESOURCE_NAME}:query" \
  -d '{
    "class_method": "create_session",
    "input": {
      "user_id": "test_user_123"
    }
  }'

echo ""
echo ""
echo "✅ Successfully connected to Agent Engine!"
echo ""
echo "📝 Note: The REST API has limited functionality."
echo "   For full testing with streaming queries and agent interactions, use:"
echo "   $ uv run test_agent_engine.py"



