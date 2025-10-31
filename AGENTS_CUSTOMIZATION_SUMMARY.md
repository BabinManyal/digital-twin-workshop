# Agents.md Customization Summary

## ✅ Completed Customizations (October 31, 2025)

### 1. **Project-Specific Information**
- ✅ Added GitHub repository URL: `https://github.com/BabinManyal/digital-twin-workshop`
- ✅ Added project purpose and key features
- ✅ Specified target use case: Interview preparation, professional portfolio queries, career coaching

### 2. **Environment Variables**
- ✅ Documented exact file locations for all environments:
  - Python: `/Users/mclovin/digital-twin-workshop/.env`
  - Next.js: `/Users/mclovin/digital-twin-workshop/digital-twin-frontend/.env.local`
  - MCP Config: `~/Library/Application Support/Claude/claude_desktop_config.json`
- ✅ Added detailed instructions for obtaining API keys
- ✅ Included all required environment variables with examples

### 3. **RAG Architecture Documentation**
- ✅ Added comprehensive 3-step RAG pipeline explanation
- ✅ Documented complete ProfileData TypeScript interface
- ✅ Documented Upstash Vector schema with metadata structure
- ✅ Added expected API response formats
- ✅ Included system prompt strategy

### 4. **API Endpoints & Business Logic**
- ✅ Documented Next.js API route: `POST /api/query`
- ✅ Added request/response format examples
- ✅ Documented all error responses (400, 500)
- ✅ Added content extraction logic
- ✅ Documented context window management (max 3 chunks, ~1500 tokens)
- ✅ Added response generation rules (first person, professional tone, evidence-based)
- ✅ Included error handling strategy with graceful degradation

### 5. **Custom Business Requirements**
- ✅ **Interview-Specific Features**:
  - STAR Method Detection for behavioral questions
  - Skill query formatting with years/proficiency/frameworks
  - Sensitive salary question handling
- ✅ **Response Constraints**:
  - Always first person
  - Max 500 tokens
  - Professional interview tone

### 6. **TypeScript Type Definitions**
- ✅ Added complete type definitions from `types/index.ts`:
  - VectorQueryResult interface
  - GroqResponse interface
  - RAGQueryResult interface
  - ContentChunk interface
- ✅ Documented location of type definition file

### 7. **Current Project Setup**
- ✅ Updated to Next.js 16.0.1 (actual version)
- ✅ Added complete dependency list with versions
- ✅ Updated package manager to npm (current setup) with pnpm migration option
- ✅ Changed commands to macOS/zsh (not Windows PowerShell)
- ✅ Added complete project structure with file descriptions

### 8. **Database Schema**
- ✅ Added Upstash Vector schema with all metadata fields
- ✅ Documented chunk structure with id, title, type, content, category, tags
- ✅ Added sample data structure from digitaltwin.json
- ✅ Included content_chunks array structure

### 9. **Example Use Cases**
- ✅ Added 6 query examples (experience, skills, projects, goals, STAR, salary)
- ✅ Added sample profile structure from actual digitaltwin.json
- ✅ Included STAR method achievement example
- ✅ Added content_chunks example with metadata

### 10. **Reference Repositories**
- ✅ Added roll dice MCP server pattern reference
- ✅ Added Python digital twin logic reference
- ✅ Moved to main Reference Documentation section with context

### 11. **Development Workflow**
- ✅ Added complete development workflow section
- ✅ Included commands for Next.js dev server
- ✅ Added MCP server build/test commands
- ✅ Added Python RAG script testing
- ✅ Documented Git workflow
- ✅ Added environment file locations for all platforms

### 12. **Package Manager Options**
- ✅ Documented current npm setup
- ✅ Added optional pnpm migration instructions
- ✅ Included both npm and pnpm commands throughout

## 📊 What Makes This agents.md Project-Specific

### Unique to Digital Twin Workshop:
1. **Actual GitHub Repository**: `BabinManyal/digital-twin-workshop`
2. **Real File Paths**: All paths reference actual macOS locations
3. **Exact Dependencies**: Next.js 16.0.1, React 19.2.0, MCP SDK 1.20.2
4. **Custom Business Logic**: Interview-focused STAR method, salary handling
5. **Actual API Structure**: Real Next.js `/api/query` endpoint implementation
6. **Project-Specific Schema**: digitaltwin.json structure with content_chunks
7. **Type Definitions**: Actual TypeScript interfaces from `types/index.ts`
8. **Environment Setup**: macOS + zsh + npm (with pnpm option)

## 🎯 How GitHub Copilot Uses This File

When you use `@workspace` in GitHub Copilot Chat, it can now:

1. **Generate project-specific code** using your exact:
   - API endpoint structure (`/api/query`)
   - Type definitions (VectorQueryResult, ContentChunk, etc.)
   - Environment variables (GROQ_API_KEY, UPSTASH_*)
   - Business logic (STAR method, first-person responses)

2. **Follow your conventions**:
   - npm package manager (or suggest pnpm migration)
   - Next.js 16.0.1 patterns
   - macOS/zsh commands
   - Error handling strategies

3. **Understand your architecture**:
   - 3-step RAG pipeline
   - Upstash Vector + Groq integration
   - MCP server structure
   - Content chunk metadata schema

4. **Respect your constraints**:
   - Max 3 chunks (top_k=3)
   - 500 token limit
   - First-person responses
   - Professional interview tone

## 📝 Usage Examples

### With GitHub Copilot Chat:

```
@workspace Create a new MCP tool for querying salary information
```
→ Copilot will use the salary handling logic from agents.md

```
@workspace Add error handling to the vector query function
```
→ Copilot will use the error handling strategy from agents.md

```
@workspace Generate TypeScript types for a new profile section
```
→ Copilot will follow the type definition patterns from agents.md

```
@workspace How do I add a new content chunk type?
```
→ Copilot will reference the ContentChunk interface and metadata schema

## 🚀 Next Steps

1. **Keep agents.md updated** as you add new features
2. **Add new business logic** when you create custom handlers
3. **Document new API endpoints** as you build them
4. **Update type definitions** when schema changes
5. **Add migration notes** if you switch from npm to pnpm

## 📊 Statistics

- **Total Lines**: ~700+ lines of comprehensive documentation
- **Code Examples**: 20+ TypeScript/JSON code blocks
- **API Endpoints**: 2 (Upstash Vector, Groq)
- **Type Interfaces**: 5 (VectorQueryResult, GroqResponse, RAGQueryResult, ContentChunk, ProfileData)
- **Environment Variables**: 3 required (GROQ_API_KEY, UPSTASH_VECTOR_REST_URL, UPSTASH_VECTOR_REST_TOKEN)
- **Business Rules**: 4 main categories (Content Extraction, Context Window, Response Generation, Error Handling)

---

**Last Updated**: October 31, 2025
**Project**: Digital Twin Workshop
**Repository**: https://github.com/BabinManyal/digital-twin-workshop
