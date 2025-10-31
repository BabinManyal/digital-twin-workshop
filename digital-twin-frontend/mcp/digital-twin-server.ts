#!/usr/bin/env node

/**
 * Digital Twin MCP Server
 * Provides AI-powered professional profile queries via Model Context Protocol
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';
import axios from 'axios';
import { z } from 'zod';

// Configuration
const GROQ_API_KEY = process.env.GROQ_API_KEY;
const UPSTASH_VECTOR_REST_URL = process.env.UPSTASH_VECTOR_REST_URL;
const UPSTASH_VECTOR_REST_TOKEN = process.env.UPSTASH_VECTOR_REST_TOKEN;
const DEFAULT_MODEL = 'llama-3.1-8b-instant';

// Validation schemas
const QueryProfileSchema = z.object({
  question: z.string().describe('Question about the professional profile'),
  top_k: z.number().optional().default(3).describe('Number of relevant results to retrieve'),
});

/**
 * Query Upstash Vector for similar content
 */
async function queryVectorDatabase(question: string, topK: number = 3) {
  if (!UPSTASH_VECTOR_REST_URL || !UPSTASH_VECTOR_REST_TOKEN) {
    throw new Error('Upstash Vector credentials not configured');
  }

  try {
    const response = await axios.post(
      `${UPSTASH_VECTOR_REST_URL}/query-data`,
      {
        data: question,
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
  } catch (error) {
    console.error('Error querying vector database:', error);
    throw new Error('Failed to query vector database');
  }
}

/**
 * Generate response using Groq
 */
async function generateResponseWithGroq(prompt: string, model: string = DEFAULT_MODEL) {
  if (!GROQ_API_KEY) {
    throw new Error('Groq API key not configured');
  }

  try {
    const response = await axios.post(
      'https://api.groq.com/openai/v1/chat/completions',
      {
        model,
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
        temperature: 0.7,
        max_tokens: 500,
      },
      {
        headers: {
          Authorization: `Bearer ${GROQ_API_KEY}`,
          'Content-Type': 'application/json',
        },
      }
    );

    return response.data.choices[0]?.message?.content || 'No response generated';
  } catch (error) {
    console.error('Error generating response with Groq:', error);
    throw new Error('Failed to generate response');
  }
}

/**
 * Perform RAG query
 */
async function performRAGQuery(question: string, topK: number = 3): Promise<string> {
  try {
    // Step 1: Query vector database
    const results = await queryVectorDatabase(question, topK);

    if (!results || results.length === 0) {
      return "I don't have specific information about that topic.";
    }

    // Step 2: Extract relevant content
    const topDocs = results
      .map((result: { metadata?: { title?: string; content?: string } }) => {
        const metadata = result.metadata || {};
        const title = metadata.title || 'Information';
        const content = metadata.content || '';
        return content ? `${title}: ${content}` : null;
      })
      .filter(Boolean);

    if (topDocs.length === 0) {
      return "I found some information but couldn't extract details.";
    }

    // Step 3: Generate response with context
    const context = topDocs.join('\n\n');
    const prompt = `Based on the following information about yourself, answer the question.
Speak in first person as if you are describing your own background.

Your Information:
${context}

Question: ${question}

Provide a helpful, professional response:`;

    const response = await generateResponseWithGroq(prompt);
    return response;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    return `❌ Error during query: ${errorMessage}`;
  }
}

/**
 * Initialize and run the MCP server
 */
async function main() {
  console.error('🤖 Starting Digital Twin MCP Server...');

  // Validate environment variables
  if (!GROQ_API_KEY) {
    console.error('❌ GROQ_API_KEY not found in environment variables');
    process.exit(1);
  }

  if (!UPSTASH_VECTOR_REST_URL || !UPSTASH_VECTOR_REST_TOKEN) {
    console.error('❌ Upstash Vector credentials not found in environment variables');
    process.exit(1);
  }

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

  // Define available tools
  const tools: Tool[] = [
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
    },
  ];

  // Handle list_tools request
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return { tools };
  });

  // Handle call_tool request
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

  // Start server with stdio transport
  const transport = new StdioServerTransport();
  await server.connect(transport);

  console.error('✅ Digital Twin MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error in main():', error);
  process.exit(1);
});
