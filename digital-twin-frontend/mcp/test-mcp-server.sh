#!/bin/bash

# Test MCP Server Startup
# This script tests if the MCP server can start and validates environment variables

echo "🧪 Testing Digital Twin MCP Server..."
echo ""

# Check if compiled file exists
if [ ! -f "mcp/dist/digital-twin-server.js" ]; then
    echo "❌ Error: Compiled server not found at mcp/dist/digital-twin-server.js"
    echo "   Run: npm run mcp:build"
    exit 1
fi

echo "✅ Compiled server found"

# Check for environment variables
if [ -z "$GROQ_API_KEY" ]; then
    echo "⚠️  Warning: GROQ_API_KEY not set"
    echo "   The server will exit immediately without this variable"
fi

if [ -z "$UPSTASH_VECTOR_REST_URL" ] || [ -z "$UPSTASH_VECTOR_REST_TOKEN" ]; then
    echo "⚠️  Warning: Upstash credentials not set"
    echo "   The server will exit immediately without these variables"
fi

echo ""
echo "📋 Expected environment variables:"
echo "   - GROQ_API_KEY"
echo "   - UPSTASH_VECTOR_REST_URL"
echo "   - UPSTASH_VECTOR_REST_TOKEN"
echo ""

# Load .env.local if it exists
if [ -f ".env.local" ]; then
    echo "✅ Found .env.local file"
    export $(cat .env.local | grep -v '^#' | xargs)
else
    echo "⚠️  No .env.local file found"
    echo "   Create one with your API keys"
fi

echo ""
echo "🚀 Attempting to start server (press Ctrl+C to stop)..."
echo "   If you see environment variable errors, add your API keys to .env.local"
echo ""

# Try to run the server
node mcp/dist/digital-twin-server.js
