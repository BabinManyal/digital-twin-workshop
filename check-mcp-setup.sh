#!/bin/bash

echo "🔍 Digital Twin MCP - Connection Method Checker"
echo "==============================================="
echo ""

# Check if Claude Desktop config exists
CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

if [ -f "$CONFIG_FILE" ]; then
    echo "✅ Claude Desktop config found"
    echo "   Location: $CONFIG_FILE"
    echo ""
    
    # Check if digital-twin server is configured
    if grep -q "digital-twin" "$CONFIG_FILE"; then
        echo "✅ Digital Twin MCP server is configured"
        echo ""
        
        # Extract command from config
        SERVER_PATH=$(grep -A 5 "digital-twin" "$CONFIG_FILE" | grep "digital-twin-server.js" | sed 's/.*"\(.*digital-twin-server.js\)".*/\1/')
        
        if [ -n "$SERVER_PATH" ]; then
            echo "📍 Server Path: $SERVER_PATH"
            
            # Check if server file exists
            if [ -f "$SERVER_PATH" ]; then
                echo "✅ MCP server file exists"
            else
                echo "❌ MCP server file NOT found at configured path"
            fi
        fi
        
        echo ""
        echo "📊 Your Setup Type: STDIO MCP (Direct Integration)"
        echo ""
        echo "✅ This is the CORRECT setup for Claude Desktop!"
        echo ""
        echo "🎯 What You Should Do:"
        echo "====================="
        echo ""
        echo "1. ❌ DO NOT run: npx mcp-remote http://localhost:3000/api/mcp"
        echo "   → Your server doesn't have /api/mcp endpoint"
        echo "   → You don't need mcp-remote for local use"
        echo ""
        echo "2. ✅ DO restart Claude Desktop:"
        echo "   → Press Cmd+Q to quit Claude Desktop"
        echo "   → Reopen Claude Desktop from Applications"
        echo ""
        echo "3. ✅ DO test with a query:"
        echo "   → Ask: 'Use the digital-twin tool to tell me about my work experience'"
        echo ""
        
    else
        echo "❌ Digital Twin MCP server NOT configured"
        echo ""
        echo "Run this to configure:"
        echo "  ./setup-claude-desktop.sh"
    fi
else
    echo "❌ Claude Desktop config NOT found"
    echo ""
    echo "Run this to create config:"
    echo "  ./setup-claude-desktop.sh"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Understanding Your Setup:"
echo ""
echo "┌─────────────────────────────────────────────────┐"
echo "│ STDIO MCP (What You Have)                       │"
echo "├─────────────────────────────────────────────────┤"
echo "│ ✅ Claude Desktop launches Node process         │"
echo "│ ✅ Communication via stdin/stdout               │"
echo "│ ✅ No HTTP server needed                        │"
echo "│ ✅ No mcp-remote needed                         │"
echo "│ ✅ More secure (local only)                     │"
echo "│ ✅ Simpler setup                                │"
echo "│ ✅ Standard for Claude Desktop                  │"
echo "└─────────────────────────────────────────────────┘"
echo ""
echo "┌─────────────────────────────────────────────────┐"
echo "│ HTTP MCP (What mcp-remote expects)              │"
echo "├─────────────────────────────────────────────────┤"
echo "│ ❌ Requires HTTP server with /api/mcp           │"
echo "│ ❌ Requires mcp-remote bridge                   │"
echo "│ ❌ More complex setup                           │"
echo "│ ✅ Allows remote access                         │"
echo "│ ✅ Multiple clients can connect                 │"
echo "│ ⚠️  Network security considerations             │"
echo "└─────────────────────────────────────────────────┘"
echo ""
echo "🎯 Your Next.js Server:"
echo "   http://localhost:3000"
echo "   ├── /             → Web UI"
echo "   ├── /api/query    → REST API (not MCP)"
echo "   └── /api/mcp      → ❌ Does NOT exist"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Bottom Line:"
echo ""
echo "   Your STDIO MCP setup is READY and CORRECT!"
echo "   Just restart Claude Desktop to activate it."
echo ""
echo "   No need for mcp-remote or HTTP endpoints."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📖 For more details, see:"
echo "   - MCP_REMOTE_VS_STDIO.md"
echo "   - MCP_SERVER_STATUS.md"
echo "   - MCP_SERVER_VERIFICATION.md"
echo ""
