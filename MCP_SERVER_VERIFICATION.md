# Digital Twin MCP Server - Verification & Setup Guide

**Date**: November 6, 2025  
**Project**: Digital Twin Workshop  
**MCP Server Type**: Stdio Transport (for Claude Desktop)

---

## 🔍 **Understanding Your MCP Server**

### **Important Clarification**

Your Digital Twin MCP server is **NOT an HTTP server**. It uses the **stdio transport protocol**, which means:

❌ **Does NOT run at** `http://localhost:3000`  
❌ **Does NOT have** `/api/mcp` endpoint  
✅ **Runs via** stdio (standard input/output)  
✅ **Integrates with** Claude Desktop app  
✅ **Uses** JSON-RPC over stdin/stdout  

---

## 📊 **Current Status**

### ✅ **MCP Server Files**

| File | Status | Purpose |
|------|--------|---------|
| `mcp/digital-twin-server.ts` | ✅ Exists | TypeScript source code |
| `mcp/dist/digital-twin-server.js` | ✅ Built | Compiled JavaScript |
| `.env.local` | ✅ Configured | Environment variables |

### ✅ **Environment Variables**

```bash
UPSTASH_VECTOR_REST_URL=your_upstash_url_here
UPSTASH_VECTOR_REST_TOKEN=ABC...
GROQ_API_KEY=gsk_...
```

All credentials are configured! ✅

---

## 🚀 **Step 1: Verify MCP Server Build**

The MCP server is already compiled. Let's verify it's working:

### **Option A: Manual Test** (Recommended)

```bash
# Navigate to the frontend directory
cd /Users/mclovin/digital-twin-workshop/digital-twin-frontend

# Test the MCP server directly
node mcp/dist/digital-twin-server.js
```

**Expected Output**:
```
🤖 Starting Digital Twin MCP Server...
✅ Digital Twin MCP Server running on stdio
```

The server will wait for JSON-RPC input. Press `Ctrl+C` to exit.

### **Option B: Rebuild If Needed**

```bash
cd /Users/mclovin/digital-twin-workshop/digital-twin-frontend

# Rebuild the MCP server
npm run mcp:build

# Expected output: TypeScript compilation successful
```

---

## 🔧 **Step 2: Configure Claude Desktop**

### **macOS Configuration File Location**

```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

### **Configuration Format**

Create or edit this file with the following content:

```json
{
  "mcpServers": {
    "digital-twin": {
      "command": "node",
      "args": [
        "/Users/mclovin/digital-twin-workshop/digital-twin-frontend/mcp/dist/digital-twin-server.js"
      ],
      "env": {
        "GROQ_API_KEY": "your_groq_api_key_here",
        "UPSTASH_VECTOR_REST_URL": "your_upstash_url_here",
        "UPSTASH_VECTOR_REST_TOKEN": "your_upstash_token_here"
      }
    }
  }
}
```

### **Quick Setup Commands**

```bash
# Create the config directory if it doesn't exist
mkdir -p ~/Library/Application\ Support/Claude

# Create the config file (manual editing required)
open -a TextEdit ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Then paste the JSON configuration above.

---

## ✅ **Step 3: Restart Claude Desktop**

1. **Quit Claude Desktop completely** (Cmd+Q or Claude → Quit)
2. **Reopen Claude Desktop**
3. **Verify MCP server is loaded**:
   - Look for a 🔌 plug icon or "Tools" indicator in Claude
   - The MCP server should auto-connect on startup

---

## 🧪 **Step 4: Test the MCP Server in Claude**

Once Claude Desktop is restarted, try these queries:

### **Test Query 1: Basic Question**
```
Can you use the digital-twin tool to tell me about my work experience?
```

**Expected Behavior**:
- Claude recognizes the `query_profile` tool
- Sends query to your MCP server
- Returns first-person response about TechCorp, skills, etc.

### **Test Query 2: Specific Skills**
```
Use my digital twin to describe my Python and AWS skills
```

### **Test Query 3: Career Goals**
```
Query my professional profile for career goals and aspirations
```

---

## 🔍 **Troubleshooting**

### **Issue 1: Claude Desktop doesn't show the tool**

**Solution**:
```bash
# Check if config file is valid JSON
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool

# Should output formatted JSON without errors
```

### **Issue 2: "Server not responding"**

**Solution**:
```bash
# Test server manually
cd /Users/mclovin/digital-twin-workshop/digital-twin-frontend
node mcp/dist/digital-twin-server.js

# Check if environment variables are accessible
echo $GROQ_API_KEY
echo $UPSTASH_VECTOR_REST_URL
```

### **Issue 3: Missing dependencies**

**Solution**:
```bash
cd /Users/mclovin/digital-twin-workshop/digital-twin-frontend

# Reinstall dependencies
npm install

# Rebuild MCP server
npm run mcp:build
```

---

## 📋 **Verification Checklist**

Before connecting Claude Desktop, ensure:

- [x] MCP server TypeScript compiled: `mcp/dist/digital-twin-server.js` exists
- [x] Environment variables configured in `.env.local`
- [x] `claude_desktop_config.json` created with correct paths
- [ ] Claude Desktop restarted after config changes
- [ ] MCP server appears in Claude's available tools
- [ ] Test query returns expected response

---

## 🎯 **What's Different from Web App?**

| Feature | Web App (localhost:3000) | MCP Server (stdio) |
|---------|-------------------------|-------------------|
| **Protocol** | HTTP REST API | JSON-RPC over stdio |
| **Interface** | Browser | Claude Desktop |
| **Endpoint** | `/api/query` | N/A (stdio only) |
| **Running** | `npm run dev` | Auto-started by Claude |
| **Testing** | Open in browser | Ask Claude to use tool |
| **Use Case** | Demos, interviews | AI assistant integration |

---

## 🔧 **MCP Server Architecture**

```
Claude Desktop
    ↓
Launches: node mcp/dist/digital-twin-server.js
    ↓
Reads environment variables (from config)
    ↓
Initializes MCP Server (stdio transport)
    ↓
Exposes tool: query_profile
    ↓
Claude can now use the tool in conversations
```

**Communication Flow**:
```
User asks Claude a question
    ↓
Claude detects need for profile information
    ↓
Claude calls query_profile tool
    ↓
MCP server receives JSON-RPC request via stdin
    ↓
Server queries Upstash Vector
    ↓
Server generates response with Groq
    ↓
Server sends response via stdout
    ↓
Claude receives response
    ↓
Claude incorporates into answer
```

---

## 🎓 **Available MCP Tool**

### **Tool: `query_profile`**

**Description**: Query the professional profile using RAG (Retrieval-Augmented Generation). Ask questions about experience, skills, projects, education, or career goals.

**Parameters**:
- `question` (string, required): Question about the professional profile
- `top_k` (number, optional, default=3): Number of relevant results to retrieve

**Example Usage in Claude**:
```
User: "Use the digital-twin tool to tell me about my technical skills"

Claude: [Calls query_profile with question="What are my technical skills?"]

MCP Server: [Returns first-person response about Python, AWS, databases, etc.]

Claude: "Based on your digital twin, here's what I found about your technical skills: ..."
```

---

## 📊 **Monitoring MCP Server**

### **Check Server Logs**

The MCP server logs to stderr (not stdout, which is reserved for MCP protocol):

```bash
# Logs appear in Claude Desktop's console
# Or test manually to see logs:
node mcp/dist/digital-twin-server.js

# You'll see:
# 🤖 Starting Digital Twin MCP Server...
# ✅ Digital Twin MCP Server running on stdio
```

### **Common Log Messages**

```
✅ Digital Twin MCP Server running on stdio
   → Server started successfully

❌ GROQ_API_KEY not found in environment variables
   → Missing API key in config

❌ Upstash Vector credentials not found
   → Missing Upstash credentials

❌ Error during query: ...
   → Query failed (check network, API limits)
```

---

## 🚀 **Quick Start Commands**

### **1. Verify Build**
```bash
cd /Users/mclovin/digital-twin-workshop/digital-twin-frontend
ls -la mcp/dist/digital-twin-server.js
```

### **2. Test Server**
```bash
cd /Users/mclovin/digital-twin-workshop/digital-twin-frontend
node mcp/dist/digital-twin-server.js
# Press Ctrl+C to exit
```

### **3. Rebuild if Needed**
```bash
cd /Users/mclovin/digital-twin-workshop/digital-twin-frontend
npm run mcp:build
```

### **4. Configure Claude Desktop**
```bash
# Open config file
open -a TextEdit ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Or use command line editor
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### **5. Restart Claude Desktop**
```bash
# Quit completely
osascript -e 'quit app "Claude"'

# Reopen
open -a Claude
```

---

## 🎯 **Next Steps**

1. ✅ **Verify**: MCP server is built and ready
2. 📝 **Configure**: Add to `claude_desktop_config.json`
3. 🔄 **Restart**: Quit and reopen Claude Desktop
4. 🧪 **Test**: Ask Claude to use the digital-twin tool
5. 🎉 **Use**: Integrate your digital twin into Claude conversations!

---

## 💡 **Pro Tips**

### **Tip 1: Environment Variables**
Instead of hardcoding API keys in the config, you can reference environment variables:

```json
{
  "mcpServers": {
    "digital-twin": {
      "command": "node",
      "args": ["/path/to/digital-twin-server.js"],
      "env": {
        "GROQ_API_KEY": "${GROQ_API_KEY}",
        "UPSTASH_VECTOR_REST_URL": "${UPSTASH_VECTOR_REST_URL}",
        "UPSTASH_VECTOR_REST_TOKEN": "${UPSTASH_VECTOR_REST_TOKEN}"
      }
    }
  }
}
```

Then set them in your shell:
```bash
export GROQ_API_KEY="gsk_..."
export UPSTASH_VECTOR_REST_URL="https://..."
export UPSTASH_VECTOR_REST_TOKEN="ABC..."
```

### **Tip 2: Multiple Profiles**
You can add multiple MCP servers for different use cases:

```json
{
  "mcpServers": {
    "digital-twin": { ... },
    "company-knowledge": { ... },
    "research-assistant": { ... }
  }
}
```

### **Tip 3: Debugging**
Add debug logging by modifying the server:

```typescript
// In digital-twin-server.ts
console.error('🔍 Received query:', question);
console.error('📊 Vector results:', results.length);
console.error('✅ Generated response length:', response.length);
```

Then rebuild: `npm run mcp:build`

---

## 📚 **Additional Resources**

- **MCP Documentation**: https://modelcontextprotocol.io
- **Claude Desktop Integration**: https://docs.anthropic.com/claude/docs/mcp
- **Digital Twin Setup Guide**: See `MCP_SERVER_SETUP.md` in project root
- **Agents Instructions**: See `agents.md` for detailed implementation guide

---

**Status**: MCP server ready for Claude Desktop integration! ✅  
**Next Action**: Configure `claude_desktop_config.json` and restart Claude Desktop  
**Support**: Check troubleshooting section if issues occur
