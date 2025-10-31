# Digital Twin MCP Server - Agent Instructions

> **Instructions for GitHub Copilot to build a production-ready MCP server**

## 🎯 Project Overview

Build a **Model Context Protocol (MCP) server** that provides AI-powered professional profile queries using RAG (Retrieval-Augmented Generation). The server integrates with Upstash Vector for vector similarity search and Groq for LLM inference.

**Project Name**: Digital Twin Workshop  
**GitHub Repository**: https://github.com/BabinManyal/digital-twin-workshop  
**Purpose**: Create an AI-powered digital twin that answers interview questions about a professional's background using RAG  
**Target Use Case**: Interview preparation, professional portfolio queries, career coaching

### Key Features
- 🎤 **Interview Preparation**: Answer behavioral, technical, and situational interview questions
- 📊 **STAR Method Responses**: Generate structured answers using Situation-Task-Action-Result format
- 🔍 **RAG-Powered Search**: Vector similarity search with built-in Upstash embeddings
- 🤖 **LLM Generation**: Fast inference using Groq's Llama 3.1 8B Instant model
- 💬 **Multi-Channel**: Web UI (Next.js), Python CLI, and MCP server for AI assistants

## 📋 Technical Requirements

### Core Technologies
- **Runtime**: Node.js 18+ with TypeScript
- **Protocol**: Model Context Protocol (MCP) SDK v1.0+
- **Vector Database**: Upstash Vector (with built-in embeddings)
- **LLM Provider**: Groq API (Llama 3.1 8B Instant)
- **Transport**: StdioServerTransport (for MCP communication)
- **Validation**: Zod for schema validation

### Dependencies
```json
{
  "@modelcontextprotocol/sdk": "^1.20.2",
  "axios": "^1.13.1",
  "dotenv": "^17.2.3",
  "zod": "^3.25.76"
}
```

## 🏗️ Project Architecture

### File Structure
```
digital-twin-workshop/
├── digital-twin-frontend/
│   └── mcp/
│       ├── digital-twin-server.ts    # Main MCP server (PRIMARY FILE)
│       └── dist/                     # Compiled output
└── digitaltwin.json                  # Professional profile data
```

### Server Location
**Primary file**: `/Users/mclovin/digital-twin-workshop/digital-twin-frontend/mcp/digital-twin-server.ts`

## 🔧 MCP Server Implementation

### Server Structure

```typescript
#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';

// Server initialization
const server = new Server(
  {
    name: 'digital-twin-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);
```

### Required Environment Variables
```typescript
// All three environment variables are REQUIRED for MCP server to function
const GROQ_API_KEY = process.env.GROQ_API_KEY;
const UPSTASH_VECTOR_REST_URL = process.env.UPSTASH_VECTOR_REST_URL;
const UPSTASH_VECTOR_REST_TOKEN = process.env.UPSTASH_VECTOR_REST_TOKEN;

// Default LLM model configuration
const DEFAULT_MODEL = 'llama-3.1-8b-instant';
```

**Environment File Locations**:
- Python: `/Users/mclovin/digital-twin-workshop/.env`
- Next.js: `/Users/mclovin/digital-twin-workshop/digital-twin-frontend/.env.local`
- MCP Server: Configured in Claude Desktop or passed via MCP client config

**Required Values**:
```bash
# Upstash Vector Database (with built-in embeddings)
UPSTASH_VECTOR_REST_URL=https://your-endpoint.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_token_here

# Groq API for LLM inference
GROQ_API_KEY=gsk_your_groq_api_key_here
```

**How to Obtain API Keys**:
- **Upstash Vector**: Sign up at https://upstash.com → Create Vector Index → Copy REST URL & Token
- **Groq API**: Sign up at https://console.groq.com → API Keys → Create new key

### Tool Definition

The server must expose ONE main tool:

```typescript
{
  name: 'query_profile',
  description: 'Query the professional profile using RAG (Retrieval-Augmented Generation). Ask questions about experience, skills, projects, education, or career goals.',
  inputSchema: {
    type: 'object',
    properties: {
      question: {
        type: 'string',
        description: 'Question about the professional profile',
      },
      top_k: {
        type: 'number',
        description: 'Number of relevant results to retrieve (default: 3)',
        default: 3,
      },
    },
    required: ['question'],
  },
}
```

## 🔍 RAG Implementation

### RAG Architecture Overview
This project uses a **3-step RAG pipeline**:
1. **Vector Search**: Query Upstash Vector with user question
2. **Context Extraction**: Extract relevant metadata from top K results
3. **LLM Generation**: Generate first-person response using Groq + context

### Data Schema & Structure

#### Profile Data Format (digitaltwin.json)
```typescript
interface ProfileData {
  personal: {
    name: string;
    title: string;
    location: string;
    summary: string;
    elevator_pitch: string;
    contact: { email, linkedin, github, portfolio }
  };
  salary_location: {
    current_salary: string;
    salary_expectations: string;
    location_preferences: string[];
    remote_experience: string;
  };
  experience: Array<{
    company: string;
    title: string;
    duration: string;
    achievements_star: Array<{
      situation: string;  // STAR method
      task: string;
      action: string;
      result: string;
    }>;
    technical_skills_used: string[];
    leadership_examples: string[];
  }>;
  skills: {
    technical: {
      programming_languages: Array<{
        language: string;
        years: number;
        proficiency: string;
        frameworks: string[];
      }>;
      databases: string[];
      cloud_platforms: string[];
      ai_ml: string[];
    };
    soft_skills: string[];
    certifications: string[];
  };
  education: {
    university: string;
    degree: string;
    graduation_year: number;
    gpa: string;
  };
  projects_portfolio: Array<{
    name: string;
    description: string;
    technologies: string[];
    impact: string;
    github_url: string;
  }>;
  career_goals: {
    short_term: string;
    long_term: string;
    learning_focus: string[];
  };
  interview_prep: {
    common_questions: {
      behavioral: string[];
      technical: string[];
      situational: string[];
    };
  };
  content_chunks: Array<{
    id: string;
    title: string;
    type: string;
    content: string;
    metadata?: { category, tags };
  }>;
}
```

#### Vector Database Schema (Upstash)
Each chunk stored in Upstash Vector contains:
```typescript
{
  id: string;                    // Unique identifier
  vector: number[];              // Auto-generated by Upstash embeddings
  metadata: {
    title: string;               // Section title (e.g., "Python Experience")
    type: string;                // Type: skill, experience, project, education
    content: string;             // Full text content for RAG context
    category?: string;           // Category: technical, behavioral, personal
    tags?: string[];            // Tags: python, aws, leadership, etc.
  }
}
```

### 1. Vector Database Query

**Upstash Vector Endpoint**: `POST ${UPSTASH_VECTOR_REST_URL}/query`

```typescript
async function queryVectorDatabase(question: string, topK: number = 3) {
  const response = await axios.post(
    `${UPSTASH_VECTOR_REST_URL}/query`,
    {
      data: question,           // Upstash has built-in embeddings
      topK,
      includeMetadata: true,
    },
    {
      headers: {
        Authorization: `Bearer ${UPSTASH_VECTOR_REST_TOKEN}`,
      },
    }
  );
  return response.data.result || [];
}
```

**Expected Response Format**:
```typescript
{
  result: [
    {
      id: "chunk_123",
      score: 0.92,
      metadata: {
        title: "Python Development Experience",
        type: "experience",
        content: "5 years of Python development...",
        category: "technical",
        tags: ["python", "backend", "django"]
      }
    }
  ]
}
```

### 2. LLM Response Generation

**Groq API Endpoint**: `POST https://api.groq.com/openai/v1/chat/completions`

```typescript
async function generateResponseWithGroq(prompt: string, model: string = DEFAULT_MODEL) {
  const response = await axios.post(
    'https://api.groq.com/openai/v1/chat/completions',
    {
      model,                    // llama-3.1-8b-instant
      messages: [
        {
          role: 'system',
          content: 'You are an AI digital twin. Answer questions as if you are the person, speaking in first person about your background, skills, and experience.',
        },
        {
          role: 'user',
          content: prompt,
        },
      ],
      temperature: 0.7,         // Balance creativity and accuracy
      max_tokens: 500,          // Limit response length
    },
    {
      headers: {
        Authorization: `Bearer ${GROQ_API_KEY}`,
        'Content-Type': 'application/json',
      },
    }
  );
  return response.data.choices[0]?.message?.content || 'No response generated';
}
```

**System Prompt Strategy**:
- Always respond in **first person** (as the digital twin)
- Use **professional tone** appropriate for interviews
- Base answers on **provided context only**
- Format **STAR method** responses when discussing achievements

### 3. RAG Query Flow

```typescript
async function performRAGQuery(question: string, topK: number = 3): Promise<string> {
  // Step 1: Query vector database
  const results = await queryVectorDatabase(question, topK);
  
  if (!results || results.length === 0) {
    return "I don't have specific information about that topic.";
  }
  
  // Step 2: Extract relevant content
  const topDocs = results
    .map((result: any) => {
      const metadata = result.metadata || {};
      const title = metadata.title || 'Information';
      const content = metadata.content || '';
      return content ? `${title}: ${content}` : null;
    })
    .filter(Boolean);
  
  // Step 3: Generate response with context
  const context = topDocs.join('\n\n');
  const prompt = `Based on the following information about yourself, answer the question.
Speak in first person as if you are describing your own background.

Your Information:
${context}

Question: ${question}

Provide a helpful, professional response:`;
  
  return await generateResponseWithGroq(prompt);
}
```

## 🎮 Request Handlers

### List Tools Handler
```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});
```

### Call Tool Handler
```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === 'query_profile') {
    const validated = QueryProfileSchema.parse(args);
    const answer = await performRAGQuery(validated.question, validated.top_k);
    
    return {
      content: [
        {
          type: 'text',
          text: answer,
        },
      ],
    };
  }
  
  throw new Error(`Unknown tool: ${name}`);
});
```

## 🚀 Server Initialization

```typescript
async function main() {
  console.error('🤖 Starting Digital Twin MCP Server...');
  
  // Validate environment variables
  if (!GROQ_API_KEY) {
    console.error('❌ GROQ_API_KEY not found');
    process.exit(1);
  }
  
  if (!UPSTASH_VECTOR_REST_URL || !UPSTASH_VECTOR_REST_TOKEN) {
    console.error('❌ Upstash credentials not found');
    process.exit(1);
  }
  
  // Start server with stdio transport
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.error('✅ Digital Twin MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
```

## 📦 Build Configuration

### package.json Scripts
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "mcp:build": "tsc mcp/digital-twin-server.ts --outDir mcp/dist --module nodenext --moduleResolution nodenext --target es2022 --esModuleInterop",
    "mcp:dev": "node mcp/dist/digital-twin-server.js"
  }
}
```

### Current Dependencies (Next.js 16.0.1)
```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.20.2",
    "axios": "^1.13.1",
    "dotenv": "^17.2.3",
    "next": "16.0.1",
    "react": "19.2.0",
    "react-dom": "19.2.0",
    "zod": "^3.25.76"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4",
    "tailwindcss": "^4",
    "typescript": "^5"
  }
}
```

### TypeScript Configuration
Ensure `.ts` files use ES modules:
- Import with `.js` extensions
- Use `"type": "module"` in package.json or `.mjs` extensions
- Configure `moduleResolution: "nodenext"`

## 🔗 API Endpoints & Business Logic

### Next.js API Route: `/api/query`
**Location**: `digital-twin-frontend/app/api/query/route.ts`

**Request Format**:
```typescript
POST /api/query
Content-Type: application/json

{
  "question": "What are your technical skills?"
}
```

**Response Format**:
```typescript
{
  "answer": "I have 5+ years of experience with Python..."
}
```

**Error Responses**:
```typescript
// Missing question
{ "error": "Question is required" }  // 400

// No results found
{ "answer": "I don't have specific information about that topic." }

// Server error
{ "error": "Failed to process query" }  // 500
```

### Business Logic Constraints

#### 1. **Content Extraction Logic**
```typescript
const topDocs = results
  .map((result: any) => {
    const metadata = result.metadata || {};
    const title = metadata.title || 'Information';
    const content = metadata.content || '';
    return content ? `${title}: ${content}` : null;
  })
  .filter(Boolean);
```
- Only include results with valid `content` field
- Filter out null/empty entries
- Format: `{title}: {content}`

#### 2. **Context Window Management**
- Maximum 3 chunks retrieved (top_k=3)
- Each chunk limited by Upstash Vector similarity score
- Combined context passed to LLM (max ~1500 tokens)

#### 3. **Response Generation Rules**
- **Always first person**: "I have experience..." not "They have..."
- **Professional tone**: Interview-appropriate language
- **Evidence-based**: Only information from retrieved chunks
- **Concise**: Max 500 tokens per response

#### 4. **Error Handling Strategy**
```typescript
// Graceful degradation
if (!results || results.length === 0) {
  return "I don't have specific information about that topic.";
}

if (topDocs.length === 0) {
  return "I found some information but couldn't extract details.";
}
```

### Custom Business Requirements

#### Interview-Specific Features
1. **STAR Method Detection**: When query contains "tell me about a time", format response as:
   - Situation: Context
   - Task: Objective
   - Action: Steps taken
   - Result: Outcomes with metrics

2. **Skill Queries**: For "what are your skills in X", include:
   - Years of experience
   - Proficiency level
   - Specific frameworks/tools
   - Real-world applications

3. **Salary Questions**: Handle sensitively:
   - Current range (if comfortable sharing)
   - Expectations based on role complexity
   - Location preferences
   - Remote work experience

## 🔗 MCP Client Configuration

### Claude Desktop (macOS)
```json
{
  "mcpServers": {
    "digital-twin": {
      "command": "node",
      "args": ["/Users/mclovin/digital-twin-workshop/digital-twin-frontend/mcp/dist/digital-twin-server.js"],
      "env": {
        "GROQ_API_KEY": "your_groq_api_key",
        "UPSTASH_VECTOR_REST_URL": "your_upstash_url",
        "UPSTASH_VECTOR_REST_TOKEN": "your_upstash_token"
      }
    }
  }
}
```

Location: `~/Library/Application Support/Claude/claude_desktop_config.json`

## ✅ Implementation Checklist

- [ ] Import required MCP SDK components
- [ ] Set up environment variable validation
- [ ] Implement `queryVectorDatabase()` function
- [ ] Implement `generateResponseWithGroq()` function
- [ ] Implement `performRAGQuery()` function with RAG logic
- [ ] Define `query_profile` tool with proper schema
- [ ] Set up `ListToolsRequestSchema` handler
- [ ] Set up `CallToolRequestSchema` handler
- [ ] Add Zod validation for input parameters
- [ ] Initialize server with StdioServerTransport
- [ ] Add proper error handling and logging
- [ ] Add shebang `#!/usr/bin/env node` at top
- [ ] Export server for testing (optional)

## 🧪 Testing

### Manual Test
```bash
# Build
npm run mcp:build

# Run
npm run mcp:dev
```

### Test Query
The server communicates via stdio (JSON-RPC). Test with:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "query_profile",
    "arguments": {
      "question": "What are your technical skills?"
    }
  }
}
```

## 📚 Reference Documentation

### Reference Repositories
- **Pattern Reference**: https://github.com/gocallum/rolldice-mcpserver.git
  - Roll dice MCP server - demonstrates MCP server structure and patterns
  - Use same technology stack and architectural patterns
- **Logic Reference**: https://github.com/gocallum/binal_digital-twin_py.git
  - Python implementation using Upstash Vector for RAG search
  - Groq and LLaMA integration examples
  - RAG query flow to replicate in TypeScript

### MCP Protocol
- **Official Docs**: https://modelcontextprotocol.io
- **SDK Reference**: https://github.com/modelcontextprotocol/typescript-sdk
- **Examples**: https://github.com/modelcontextprotocol/servers

### API Documentation
- **Groq API**: https://console.groq.com/docs
- **Upstash Vector**: https://upstash.com/docs/vector
- **Axios**: https://axios-http.com/docs

## 🎯 Code Quality Standards

### TypeScript Type Definitions
**Location**: `digital-twin-frontend/types/index.ts`

```typescript
// Vector query result from Upstash
export interface VectorQueryResult {
  id: string;
  score: number;
  metadata?: {
    title?: string;
    type?: string;
    content?: string;
    category?: string;
    tags?: string[];
  };
}

// Groq API response
export interface GroqResponse {
  choices: Array<{
    message: {
      content: string;
      role: string;
    };
  }>;
}

// RAG query result
export interface RAGQueryResult {
  answer: string;
  sources: VectorQueryResult[];
  context: string;
}

// Content chunk structure
export interface ContentChunk {
  id: string;
  title: string;
  type: string;
  content: string;
  metadata?: {
    category?: string;
    tags?: string[];
  };
}
```

### Error Handling
- Validate all environment variables on startup
- Handle API errors gracefully
- Return meaningful error messages to clients
- Log errors to stderr (not stdout, which is for MCP)

### Logging
- Use `console.error()` for logs (stdout is reserved for MCP protocol)
- Include emoji indicators: ✅ ❌ 🔄 ⚡
- Log server lifecycle events

### Type Safety
- Use TypeScript strict mode
- Define interfaces for API responses
- Validate input with Zod schemas
- Handle null/undefined cases

## 🔐 Security Considerations

- Never log API keys or tokens
- Validate all user inputs
- Use environment variables for secrets
- Sanitize prompts before sending to LLM
- Rate limit if needed (future enhancement)

## 🚀 Deployment Notes

### Environment Setup
1. Ensure Node.js 18+ is installed
2. Set environment variables in `.env` or MCP client config
3. Build TypeScript: `npm run mcp:build`
4. Test locally before deploying

### Production Checklist
- [ ] Environment variables configured
- [ ] TypeScript compiled successfully
- [ ] Server starts without errors
- [ ] Tool responds to queries correctly
- [ ] Error handling works as expected

## 💡 Example Use Cases

### Query Examples
```typescript
// Experience query
"Tell me about your work experience at TechCorp"

// Skills query  
"What are your Python and AWS skills?"

// Project query
"Describe your AI projects"

// Career goals
"What are your short-term career goals?"

// STAR method (behavioral)
"Tell me about a time you had to lead a difficult technical decision"

// Salary inquiry
"What are your salary expectations?"
```

### Expected Responses
Responses should:
- Be in first person (as the digital twin)
- Reference specific details from the profile
- Be professional and concise
- Stay within 500 tokens

### Sample Profile Structure (digitaltwin.json)
```json
{
  "personal": {
    "name": "Your Full Name",
    "title": "Senior Software Engineer",
    "location": "Melbourne, Australia"
  },
  "experience": [
    {
      "company": "TechCorp Australia",
      "title": "Senior Software Engineer",
      "achievements_star": [
        {
          "situation": "Legacy monolith causing 3-second page load times",
          "task": "Lead architectural redesign to improve performance",
          "action": "Implemented microservices with Docker and Kubernetes",
          "result": "Reduced load times by 40%, increased retention by 15%"
        }
      ]
    }
  ],
  "skills": {
    "technical": {
      "programming_languages": [
        {
          "language": "Python",
          "years": 5,
          "proficiency": "Expert",
          "frameworks": ["Django", "FastAPI", "Flask"]
        }
      ],
      "ai_ml": ["RAG systems", "Vector databases", "LLM integration"]
    }
  },
  "content_chunks": [
    {
      "id": "chunk_py_001",
      "title": "Python Expertise",
      "type": "skill",
      "content": "I have 5 years of expert-level Python experience...",
      "metadata": {
        "category": "technical",
        "tags": ["python", "backend", "django"]
      }
    }
  ]
}
```

## 🎓 Learning Resources

- [Building MCP Servers](https://modelcontextprotocol.io/docs/building-servers)
- [TypeScript MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [RAG Best Practices](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Groq Documentation](https://console.groq.com/docs/quickstart)

---

## 🤖 GitHub Copilot Instructions

When building this MCP server:

1. **Start with imports**: Import all required MCP SDK components
2. **Environment setup**: Validate environment variables early
3. **Implement utilities**: Build helper functions first (query, generate)
4. **RAG logic**: Implement the complete RAG query flow
5. **Tool definition**: Define the query_profile tool with proper schema
6. **Handlers**: Set up request handlers for list_tools and call_tool
7. **Server init**: Initialize server with StdioServerTransport
8. **Error handling**: Add comprehensive error handling throughout
9. **Testing**: Ensure the server can be built and run successfully

**Follow the architecture and examples provided above exactly.**

---

**Current Status**: Ready for implementation
**Primary File**: `/Users/mclovin/digital-twin-workshop/digital-twin-frontend/mcp/digital-twin-server.ts`
**Build Command**: `npm run mcp:build`
**Run Command**: `npm run mcp:dev`
**GitHub Repository**: https://github.com/BabinManyal/digital-twin-workshop