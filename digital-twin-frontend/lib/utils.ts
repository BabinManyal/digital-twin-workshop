/**
 * Utility functions for the Digital Twin application
 */

import axios from 'axios';

const GROQ_API_KEY = process.env.NEXT_PUBLIC_GROQ_API_KEY || process.env.GROQ_API_KEY;
const UPSTASH_VECTOR_REST_URL = process.env.UPSTASH_VECTOR_REST_URL;
const UPSTASH_VECTOR_REST_TOKEN = process.env.UPSTASH_VECTOR_REST_TOKEN;

export async function queryDigitalTwin(question: string): Promise<string> {
  try {
    const response = await fetch('/api/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      throw new Error('Failed to query digital twin');
    }

    const data = await response.json();
    return data.answer;
  } catch (error) {
    console.error('Error querying digital twin:', error);
    throw error;
  }
}

export async function queryVectorDatabase(question: string, topK: number = 3) {
  if (!UPSTASH_VECTOR_REST_URL || !UPSTASH_VECTOR_REST_TOKEN) {
    throw new Error('Upstash Vector credentials not configured');
  }

  const response = await axios.post(
    `${UPSTASH_VECTOR_REST_URL}/query`,
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
}

export async function generateResponseWithGroq(prompt: string, model: string = 'llama-3.1-8b-instant') {
  if (!GROQ_API_KEY) {
    throw new Error('Groq API key not configured');
  }

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
}
