#!/bin/bash

# Test MCP Server Startup
echo "🧪 Testing Digital Twin MCP Server..."
echo ""

# Load environment variables from .env.local
export $(cat /Users/mclovin/digital-twin-workshop/digital-twin-frontend/.env.local | grep -v '^#' | xargs)

# Navigate to frontend directory
cd /Users/mclovin/digital-twin-workshop/digital-twin-frontend

# Test the server (it will wait for stdin, so we kill it after 2 seconds)
echo "Starting MCP server..."
node mcp/dist/digital-twin-server.js &
SERVER_PID=$!

# Wait 2 seconds
sleep 2

# Kill the server
kill $SERVER_PID 2>/dev/null

echo ""
echo "✅ MCP Server test complete!"
echo ""
echo "📋 Next steps:"
echo "1. Copy claude_desktop_config.json to Claude Desktop config location:"
echo "   cp /Users/mclovin/digital-twin-workshop/claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json"
echo ""
echo "2. Restart Claude Desktop"
echo ""
echo "3. Test by asking Claude: 'Use the digital-twin tool to tell me about my work experience'"
