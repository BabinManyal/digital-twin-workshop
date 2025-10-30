# Digital Twin Workshop 🤖

An AI-powered professional profile assistant using RAG (Retrieval-Augmented Generation) with Upstash Vector and Groq LLM.

## 🌟 Features

- **RAG System**: Vector similarity search with built-in embeddings
- **Next.js Frontend**: Beautiful, responsive chat interface
- **MCP Server**: Model Context Protocol integration
- **Python CLI**: Command-line interface for quick queries
- **Type-Safe**: Full TypeScript support
- **Fast AI**: Powered by Groq for ultra-fast inference

## 🏗️ Project Structure

```
digital-twin-workshop/
├── digital-twin-frontend/    # Next.js application
│   ├── app/                  # Pages and API routes
│   ├── mcp/                  # MCP server implementation
│   ├── lib/                  # Utility functions
│   └── types/                # TypeScript definitions
├── embed_digitaltwin.py      # Python RAG implementation
├── digitaltwin.json         # Professional profile data
└── data/                    # Data directory
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- Upstash Vector Database account
- Groq API key

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/digital-twin-workshop.git
cd digital-twin-workshop
```

### 2. Python Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install upstash-vector groq python-dotenv

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 3. Next.js Setup

```bash
cd digital-twin-frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.local.example .env.local
# Edit .env.local with your API keys

# Run development server
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000)

## 🔑 Environment Variables

### Root `.env` (Python)
```env
UPSTASH_VECTOR_REST_URL=your_upstash_url
UPSTASH_VECTOR_REST_TOKEN=your_upstash_token
GROQ_API_KEY=your_groq_key
```

### Frontend `.env.local` (Next.js)
```env
UPSTASH_VECTOR_REST_URL=your_upstash_url
UPSTASH_VECTOR_REST_TOKEN=your_upstash_token
GROQ_API_KEY=your_groq_key
```

## 📖 Usage

### Python CLI

```bash
python embed_digitaltwin.py
```

### Web Interface

```bash
cd digital-twin-frontend
npm run dev
```

### MCP Server

```bash
cd digital-twin-frontend
npm run mcp:build
npm run mcp:dev
```

## 🛠️ Tech Stack

- **Frontend**: Next.js 15, TypeScript, Tailwind CSS
- **Backend**: Python 3.12, Node.js
- **Vector DB**: Upstash Vector
- **LLM**: Groq (Llama 3.1)
- **Protocol**: Model Context Protocol (MCP)

## 📝 Customization

1. Edit `digitaltwin.json` with your professional profile
2. Add `content_chunks` for RAG retrieval
3. Customize the UI in `digital-twin-frontend/app/page.tsx`
4. Modify prompts in API routes or Python script

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use for your own digital twin!

## 🔗 Resources

- [Upstash Vector Docs](https://upstash.com/docs/vector)
- [Groq API Docs](https://console.groq.com/docs)
- [Next.js Docs](https://nextjs.org/docs)
- [MCP Protocol](https://modelcontextprotocol.io)

## 📧 Contact

Created with ❤️ for building AI-powered professional profiles.
