# Digital Twin Workshop - Complete Project Setup

## 📁 Project Structure

```
digital-twin-workshop/
├── .env                           # Root environment variables (Python)
├── .venv/                         # Python virtual environment
├── data/                          # Data directory
├── digitaltwin.json              # Professional profile data
├── embed_digitaltwin.py          # Python RAG script
├── digital_twin_mcp_server.py    # Python MCP server (if needed)
└── digital-twin-frontend/        # Next.js application
    ├── app/
    │   ├── api/
    │   │   └── query/
    │   │       └── route.ts      # API endpoint for RAG queries
    │   ├── layout.tsx
    │   └── page.tsx              # Main chat interface
    ├── mcp/
    │   └── digital-twin-server.ts # TypeScript MCP server
    ├── lib/
    │   └── utils.ts              # Utility functions
    ├── types/
    │   └── index.ts              # TypeScript definitions
    ├── .env.local.example        # Environment template
    ├── package.json
    └── README.md
```

## ✅ What's Been Set Up

### 1. Python Environment
- ✅ Python virtual environment created (`.venv`)
- ✅ Packages installed:
  - `upstash-vector` - Vector database client
  - `groq` - LLM API client
  - `python-dotenv` - Environment variable management
- ✅ `embed_digitaltwin.py` - Complete RAG implementation with fixed syntax

### 2. Next.js Application
- ✅ Next.js 15 with TypeScript and Tailwind CSS
- ✅ Production-ready folder structure
- ✅ Beautiful chat interface UI
- ✅ API routes for backend logic
- ✅ MCP server implementation
- ✅ Type-safe with TypeScript
- ✅ Additional packages:
  - `@modelcontextprotocol/sdk` - MCP protocol
  - `axios` - HTTP client
  - `zod` - Schema validation

### 3. Configuration Files
- ✅ `.env` - Root environment variables
- ✅ `.env.local.example` - Frontend environment template
- ✅ `digitaltwin.json` - Professional profile (valid JSON)
- ✅ Updated `package.json` with MCP scripts
- ✅ Comprehensive README

## 🚀 Next Steps

### Step 1: Configure Environment Variables

**For Python (`/digital-twin-workshop/.env`):**
```env
UPSTASH_VECTOR_REST_URL="your_upstash_url"
UPSTASH_VECTOR_REST_TOKEN="your_upstash_token"
GROQ_API_KEY=your_groq_key
```

**For Next.js (`/digital-twin-workshop/digital-twin-frontend/.env.local`):**
```env
UPSTASH_VECTOR_REST_URL=your_upstash_url
UPSTASH_VECTOR_REST_TOKEN=your_upstash_token
GROQ_API_KEY=your_groq_key
```

### Step 2: Customize Your Profile

Edit `digitaltwin.json` with your actual professional information:
- Personal details
- Work experience
- Skills
- Projects
- Career goals

### Step 3: Create Content Chunks

Add a `content_chunks` array to `digitaltwin.json` for the RAG system:

```json
{
  "personal": { ... },
  "content_chunks": [
    {
      "id": "exp-1",
      "title": "Senior Software Engineer at TechCorp",
      "type": "experience",
      "content": "Led development of microservices architecture...",
      "metadata": {
        "category": "work_experience",
        "tags": ["leadership", "architecture", "microservices"]
      }
    }
  ]
}
```

### Step 4: Run the Python RAG Script

```bash
cd /Users/mclovin/digital-twin-workshop
/Users/mclovin/digital-twin-workshop/.venv/bin/python embed_digitaltwin.py
```

This will:
1. Load your profile from `digitaltwin.json`
2. Upload content chunks to Upstash Vector
3. Start an interactive chat interface

### Step 5: Run the Next.js Application

```bash
cd digital-twin-frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Step 6: Build and Run MCP Server

```bash
cd digital-twin-frontend
npm run mcp:build
npm run mcp:dev
```

### Step 7: Configure MCP Client (Optional)

For Claude Desktop, add to configuration:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "digital-twin": {
      "command": "node",
      "args": ["/Users/mclovin/digital-twin-workshop/digital-twin-frontend/mcp/dist/digital-twin-server.js"],
      "env": {
        "GROQ_API_KEY": "your_key",
        "UPSTASH_VECTOR_REST_URL": "your_url",
        "UPSTASH_VECTOR_REST_TOKEN": "your_token"
      }
    }
  }
}
```

## 🎯 Usage Examples

### Python CLI Chat
```bash
/Users/mclovin/digital-twin-workshop/.venv/bin/python embed_digitaltwin.py

You: Tell me about your work experience
🤖 Digital Twin: I'm currently working as a Senior Software Engineer...
```

### Web Interface
1. Visit http://localhost:3000
2. Type questions in the chat box
3. Get AI-powered responses about your profile

### MCP Protocol
Use the `query_profile` tool in any MCP-compatible client:
```json
{
  "tool": "query_profile",
  "arguments": {
    "question": "What are your technical skills?",
    "top_k": 3
  }
}
```

## 🔧 Development Commands

### Python
```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Run the script
python embed_digitaltwin.py
```

### Next.js
```bash
cd digital-twin-frontend

# Development
npm run dev

# Production build
npm run build
npm run start

# Lint
npm run lint

# MCP server
npm run mcp:build
npm run mcp:dev
```

## 📚 Key Features

### RAG System
- Vector similarity search with Upstash Vector
- Built-in embeddings (no external embedding service needed)
- Context-aware responses

### LLM Integration
- Groq API for ultra-fast inference
- Llama 3.1 8B model
- Optimized prompts for professional profiles

### Modern UI
- Responsive design with Tailwind CSS
- Loading states and error handling
- Suggested questions
- Beautiful gradient backgrounds

### Type Safety
- Full TypeScript support
- Zod schema validation
- Type-safe API routes

### MCP Protocol
- Standard protocol implementation
- Easy integration with AI assistants
- Extensible tool system

## 🐛 Troubleshooting

### Import Errors (Python)
```bash
# Ensure virtual environment is activated
source .venv/bin/activate
# Reinstall packages if needed
pip install upstash-vector groq python-dotenv
```

### API Errors
- Check environment variables are set correctly
- Verify API keys are valid
- Check Upstash Vector database is accessible

### Build Errors (Next.js)
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

## 📖 Documentation

- [Next.js Docs](https://nextjs.org/docs)
- [Upstash Vector Docs](https://upstash.com/docs/vector)
- [Groq API Docs](https://console.groq.com/docs)
- [MCP Protocol](https://modelcontextprotocol.io)

## 🎉 You're All Set!

Your Digital Twin project is now fully configured and ready to use. Follow the steps above to start building your AI-powered professional profile assistant!
