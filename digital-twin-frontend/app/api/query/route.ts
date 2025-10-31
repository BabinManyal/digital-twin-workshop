import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';

const GROQ_API_KEY = process.env.GROQ_API_KEY;
const UPSTASH_VECTOR_REST_URL = process.env.UPSTASH_VECTOR_REST_URL;
const UPSTASH_VECTOR_REST_TOKEN = process.env.UPSTASH_VECTOR_REST_TOKEN;

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
  } catch (error: any) {
    console.error('Upstash query error:', error.response?.data || error.message);
    throw error;
  }
}

async function generateResponseWithGroq(prompt: string) {
  if (!GROQ_API_KEY) {
    throw new Error('Groq API key not configured');
  }

  const response = await axios.post(
    'https://api.groq.com/openai/v1/chat/completions',
    {
      model: 'llama-3.1-8b-instant',
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
}

export async function POST(request: NextRequest) {
  try {
    const { question } = await request.json();

    if (!question) {
      return NextResponse.json(
        { error: 'Question is required' },
        { status: 400 }
      );
    }

    // Query vector database
    const results = await queryVectorDatabase(question, 3);

    if (!results || results.length === 0) {
      return NextResponse.json({
        answer: "I don't have specific information about that topic.",
      });
    }

    // Extract relevant content
    const topDocs = results
      .map((result: { metadata?: { title?: string; content?: string } }) => {
        const metadata = result.metadata || {};
        const title = metadata.title || 'Information';
        const content = metadata.content || '';
        return content ? `${title}: ${content}` : null;
      })
      .filter(Boolean);

    if (topDocs.length === 0) {
      return NextResponse.json({
        answer: "I found some information but couldn't extract details.",
      });
    }

    // Generate response with context
    const context = topDocs.join('\n\n');
    const prompt = `Based on the following information about yourself, answer the question.
Speak in first person as if you are describing your own background.

Your Information:
${context}

Question: ${question}

Provide a helpful, professional response:`;

    const answer = await generateResponseWithGroq(prompt);

    return NextResponse.json({ answer });
  } catch (error) {
    console.error('Error processing query:', error);
    return NextResponse.json(
      { error: 'Failed to process query' },
      { status: 500 }
    );
  }
}
