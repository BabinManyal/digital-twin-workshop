# Digital Twin MCP Server Setup Guide

## ✅ Server Status: Built and Ready!

Your MCP server has been successfully generated following the patterns in `agents.md`.

## 📁 Files Created

- **Source**: `digital-twin-frontend/mcp/digital-twin-server.ts` (7.0KB)
- **Compiled**: `digital-twin-frontend/mcp/dist/digital-twin-server.js`

## 🔧 What Was Built

### ✅ Complete Implementation Checklist

- [x] **Shebang**: `#!/usr/bin/env node` for executable script
- [x] **Imports**: All required MCP SDK components, axios, zod
- [x] **Environment Variables**: GROQ_API_KEY, UPSTASH_VECTOR_REST_URL, UPSTASH_VECTOR_REST_TOKEN
- [x] **Validation Schema**: Zod schema for query_profile tool
- [x] **queryVectorDatabase()**: Axios POST to Upstash Vector with built-in embeddings
- [x] **generateResponseWithGroq()**: LLM inference with Llama 3.1 8B Instant
- [x] **performRAGQuery()**: 3-step RAG pipeline (Vector Search → Extract Context → Generate)
- [x] **query_profile Tool**: MCP tool definition with proper input schema
- [x] **ListToolsRequestSchema Handler**: Returns available tools
- [x] **CallToolRequestSchema Handler**: Executes query_profile with validation
- [x] **StdioServerTransport**: MCP communication via stdio
- [x] **Error Handling**: Graceful degradation and meaningful error messages
- [x] **Logging**: Console.error for server events (stdout reserved for MCP)

## 🚀 How to Use

### Step 1: Set Environment Variables

Create or update `.env.local` in `digital-twin-frontend/`:

```bash
# Upstash Vector Database
UPSTASH_VECTOR_REST_URL=https://your-endpoint.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_token_here

# Groq API for LLM inference
GROQ_API_KEY=gsk_your_groq_api_key_here
```

**Get API Keys**:
- **Upstash**: Sign up at https://upstash.com → Create Vector Index → Copy REST URL & Token
- **Groq**: Sign up at https://console.groq.com → API Keys → Create new key

### Step 2: Prepare Profile Data

Ensure `digitaltwin.json` has a `content_chunks` array for RAG:

```json
{
  "content_chunks": [
    {
      "id": "chunk_py_001",
      "title": "Python Expertise",
      "type": "skill",
      "content": "I have 5 years of expert-level Python experience with Django, FastAPI, and Flask...",
      "metadata": {
        "category": "technical",
        "tags": ["python", "backend", "django"]
      }
    }
  ]
}
```

### Step 3: Upload Vectors to Upstash

Run the Python script to upload your profile data:

```bash
cd /Users/mclovin/digital-twin-workshop
.venv/bin/python embed_digitaltwin.py
```

This will:
- Read `digitaltwin.json`
- Extract `content_chunks`
- Upload to Upstash Vector with built-in embeddings

### Step 4: Test the MCP Server (Standalone)

```bash
cd /Users/mclovin/digital-twin-workshop/digital-twin-frontend
npm run mcp:dev
```

This starts the server on stdio. You should see:
```
🤖 Starting Digital Twin MCP Server...
✅ Digital Twin MCP Server running on stdio
```

**Note**: The server waits for JSON-RPC messages on stdin. Press `Ctrl+C` to stop.

### Step 5: Configure MCP Client

#### Option A: Claude Desktop (macOS)

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "digital-twin": {
      "command": "node",
      "args": [
        "/Users/mclovin/digital-twin-workshop/digital-twin-frontend/mcp/dist/digital-twin-server.js"
      ],
      "env": {
        "GROQ_API_KEY": "gsk_your_groq_api_key",
        "UPSTASH_VECTOR_REST_URL": "https://your-endpoint.upstash.io",
        "UPSTASH_VECTOR_REST_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Restart Claude Desktop** to load the MCP server.

#### Option B: VS Code with MCP Extension

Edit `~/Library/Application Support/Code - Insiders/User/mcp.json`:

```json
{
  "servers": {
    "digital-twin": {
      "type": "stdio",
      "command": "node",
      "args": [
        "/Users/mclovin/digital-twin-workshop/digital-twin-frontend/mcp/dist/digital-twin-server.js"
      ],
      "env": {
        "GROQ_API_KEY": "gsk_your_groq_api_key",
        "UPSTASH_VECTOR_REST_URL": "https://your-endpoint.upstash.io",
        "UPSTASH_VECTOR_REST_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Reload VS Code Insiders** to activate.

### Step 6: Use the MCP Server

In Claude Desktop or your MCP client, you can now use:

```
Use the query_profile tool to answer: What are my Python skills?
```

The MCP server will:
1. Query Upstash Vector with your question
2. Retrieve top 3 similar content chunks
3. Generate a first-person response using Groq
4. Return the answer via MCP protocol

## 🔍 Available Tool

### `query_profile`

**Description**: Query the professional profile using RAG (Retrieval-Augmented Generation). Ask questions about experience, skills, projects, education, or career goals.

**Parameters**:
- `question` (string, required): Question about the professional profile
- `top_k` (number, optional, default: 3): Number of relevant results to retrieve

**Example Queries**:
- "What are your technical skills?"
- "Tell me about your work experience at TechCorp"
- "Describe your AI projects"
- "What are your short-term career goals?"
- "Tell me about a time you had to lead a difficult technical decision"
- "What are your salary expectations?"

## 📊 RAG Pipeline

### 3-Step Process

1. **Vector Search** (Upstash Vector)
   - Converts question to embeddings (automatic)
   - Finds top K similar content chunks
   - Returns results with metadata

2. **Context Extraction**
   - Extracts `title` and `content` from metadata
   - Filters out empty results
   - Combines into context string

3. **LLM Generation** (Groq)
   - Sends context + question to Llama 3.1 8B Instant
   - System prompt: Respond in first person as digital twin
   - Temperature: 0.7 (balanced)
   - Max tokens: 500 (concise responses)

## 🛠️ Troubleshooting

### Server Won't Start

**Error**: `❌ GROQ_API_KEY not found`
- **Solution**: Add environment variables to `.env.local` or MCP client config

**Error**: `❌ Upstash Vector credentials not found`
- **Solution**: Add `UPSTASH_VECTOR_REST_URL` and `UPSTASH_VECTOR_REST_TOKEN`

### No Results Returned

**Response**: `I don't have specific information about that topic.`
- **Cause**: No similar content chunks found in Upstash Vector
- **Solution**: Run `embed_digitaltwin.py` to upload vectors
- **Check**: Verify `content_chunks` array exists in `digitaltwin.json`

### Error During Query

**Response**: `❌ Error during query: Failed to query vector database`
- **Cause**: Upstash Vector API error or invalid credentials
- **Solution**: Check Upstash dashboard, verify credentials are correct

**Response**: `❌ Error during query: Failed to generate response`
- **Cause**: Groq API error or invalid key
- **Solution**: Verify Groq API key at https://console.groq.com

## 🔄 Development Workflow

### Rebuild After Changes

```bash
cd digital-twin-frontend
npm run mcp:build
```

### Test Locally

```bash
npm run mcp:dev
```

### Add New Tools

Edit `mcp/digital-twin-server.ts`:

1. Add tool definition to `tools` array
2. Add case to `CallToolRequestSchema` handler
3. Rebuild with `npm run mcp:build`
4. Restart MCP client

## 📚 Architecture Reference

### File Structure
```
digital-twin-frontend/
├── mcp/
│   ├── digital-twin-server.ts    # Source code
│   └── dist/
│       └── digital-twin-server.js # Compiled output
├── app/
│   └── api/query/route.ts        # Next.js API (similar logic)
├── lib/utils.ts                   # Shared utilities
├── types/index.ts                 # TypeScript definitions
└── package.json                   # Dependencies & scripts
```

### Key Components

- **Server**: `@modelcontextprotocol/sdk/server`
- **Transport**: `StdioServerTransport` (JSON-RPC over stdio)
- **Vector DB**: Upstash Vector REST API (built-in embeddings)
- **LLM**: Groq API (Llama 3.1 8B Instant)
- **Validation**: Zod schemas for type safety

## 🎯 Next Steps

1. ✅ **MCP Server Built** - Ready to use!
2. 🔄 **Add Environment Variables** - Required for functionality
3. 🔄 **Upload Profile Data** - Run `embed_digitaltwin.py`
4. 🔄 **Configure MCP Client** - Claude Desktop or VS Code
5. 🔄 **Test Query** - Ask questions about your profile
6. 📈 **Customize** - Add more tools, refine prompts, adjust parameters

## 📖 Documentation

- **agents.md**: Complete implementation guide
- **COPILOT_GUIDE.md**: How to use GitHub Copilot with this project
- **PROJECT_SETUP.md**: General project setup instructions
- **README.md**: Project overview

## 🚀 Success Criteria

Your MCP server is working correctly when:

- ✅ Server starts without errors
- ✅ Returns "I don't have specific information..." when no data uploaded
- ✅ Returns relevant answers after uploading vectors
- ✅ Responds in first person (as the digital twin)
- ✅ Generates professional, interview-appropriate answers
- ✅ Handles errors gracefully

---

**Built on**: October 31, 2025
**Project**: Digital Twin Workshop
**Repository**: https://github.com/BabinManyal/digital-twin-workshop
