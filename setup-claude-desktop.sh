#!/bin/bash

# Setup Claude Desktop MCP Server Integration
echo "🤖 Digital Twin MCP Server - Claude Desktop Setup"
echo "=================================================="
echo ""

# Check if Claude Desktop config directory exists
CONFIG_DIR="$HOME/Library/Application Support/Claude"
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

if [ ! -d "$CONFIG_DIR" ]; then
    echo "📁 Creating Claude Desktop config directory..."
    mkdir -p "$CONFIG_DIR"
fi

# Backup existing config if it exists
if [ -f "$CONFIG_FILE" ]; then
    BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    echo "💾 Backing up existing config to:"
    echo "   $BACKUP_FILE"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
fi

# Copy new config
echo "📋 Installing MCP server configuration..."
cp /Users/mclovin/digital-twin-workshop/claude_desktop_config.json "$CONFIG_FILE"

# Verify config is valid JSON
echo "✅ Validating configuration..."
if python3 -m json.tool "$CONFIG_FILE" > /dev/null 2>&1; then
    echo "✅ Configuration is valid JSON"
else
    echo "❌ Error: Configuration is not valid JSON"
    exit 1
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "=============="
echo ""
echo "1. 🔄 Restart Claude Desktop:"
echo "   - Quit Claude Desktop completely (Cmd+Q)"
echo "   - Reopen Claude Desktop"
echo ""
echo "2. 🧪 Test the MCP server in Claude:"
echo "   Ask: 'Use the digital-twin tool to tell me about my work experience'"
echo ""
echo "3. 💡 Example queries to try:"
echo "   - 'Query my digital twin about Python skills'"
echo "   - 'Use my professional profile to describe my career goals'"
echo "   - 'Tell me about my experience at TechCorp using the digital-twin tool'"
echo ""
echo "📍 Configuration Location:"
echo "   $CONFIG_FILE"
echo ""
echo "🔧 MCP Server Location:"
echo "   /Users/mclovin/digital-twin-workshop/digital-twin-frontend/mcp/dist/digital-twin-server.js"
echo ""
echo "📚 Documentation:"
echo "   See MCP_SERVER_VERIFICATION.md for troubleshooting"
echo ""
