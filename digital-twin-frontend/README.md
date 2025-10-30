# Digital Twin MCP Server

A production-ready Next.js application with TypeScript, Tailwind CSS, and Model Context Protocol (MCP) server integration.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Upstash Vector Database account
- Groq API key

### Installation

1. **Install dependencies:**
```bash
cd digital-twin-frontend
npm install
```

2. **Set up environment variables:**
```bash
cp .env.local.example .env.local
```

Edit `.env.local` and add your credentials:
```env
UPSTASH_VECTOR_REST_URL=your_upstash_vector_url
UPSTASH_VECTOR_REST_TOKEN=your_upstash_vector_token
GROQ_API_KEY=your_groq_api_key
```

3. **Run the development server:**
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

## 🏗️ Project Structure

```
digital-twin-frontend/
├── app/
│   ├── api/
│   │   └── query/
│   │       └── route.ts          # API endpoint for RAG queries
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Main chat interface
├── mcp/
│   └── digital-twin-server.ts    # MCP server implementation
├── lib/
│   └── utils.ts                  # Utility functions
├── types/
│   └── index.ts                  # TypeScript type definitions
├── .env.local.example            # Environment variables template
├── package.json
├── tsconfig.json
└── tailwind.config.ts
```

## 🔧 MCP Server

### Build the MCP Server

```bash
npm run mcp:build
```

### Run the MCP Server

```bash
npm run mcp:dev
```

### MCP Server Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "digital-twin": {
      "command": "node",
      "args": ["/path/to/digital-twin-frontend/mcp/dist/digital-twin-server.js"],
      "env": {
        "GROQ_API_KEY": "your_key",
        "UPSTASH_VECTOR_REST_URL": "your_url",
        "UPSTASH_VECTOR_REST_TOKEN": "your_token"
      }
    }
  }
}
```

## 🎯 Features

- **RAG System**: Retrieval-Augmented Generation using Upstash Vector
- **Fast AI**: Powered by Groq for ultra-fast LLM inference
- **Type-Safe**: Full TypeScript support
- **Modern UI**: Beautiful Tailwind CSS interface
- **MCP Integration**: Standard Model Context Protocol server
- **API Routes**: Next.js API routes for backend logic

## 🛠️ Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Vector DB**: Upstash Vector
- **LLM**: Groq (Llama 3.1)
- **Protocol**: Model Context Protocol (MCP)
- **Validation**: Zod

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run mcp:build` - Build MCP server
- `npm run mcp:dev` - Run MCP server

## 🔐 Environment Variables

Required environment variables:

| Variable | Description |
|----------|-------------|
| `UPSTASH_VECTOR_REST_URL` | Upstash Vector database URL |
| `UPSTASH_VECTOR_REST_TOKEN` | Upstash Vector authentication token |
| `GROQ_API_KEY` | Groq API key for LLM inference |

## 🎨 Customization

### Update the UI

Edit `app/page.tsx` to customize the chat interface.

### Modify RAG Logic

Edit `app/api/query/route.ts` to change the retrieval and generation logic.

### Adjust MCP Tools

Edit `mcp/digital-twin-server.ts` to add or modify MCP tools.

## 📦 Deployment

### Vercel (Recommended)

```bash
npm run build
vercel deploy
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for your own digital twin!
