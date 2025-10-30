/**
 * TypeScript type definitions for Digital Twin application
 */

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

export interface GroqResponse {
  choices: Array<{
    message: {
      content: string;
      role: string;
    };
  }>;
}

export interface RAGQueryResult {
  answer: string;
  sources: VectorQueryResult[];
  context: string;
}

export interface ProfileData {
  personal?: {
    name: string;
    title: string;
    location: string;
    summary: string;
    elevator_pitch: string;
    contact: {
      email: string;
      linkedin: string;
      github: string;
      portfolio: string;
    };
  };
  experience?: Array<{
    company: string;
    title: string;
    duration: string;
    achievements_star: Array<{
      situation: string;
      task: string;
      action: string;
      result: string;
    }>;
  }>;
  skills?: {
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
  content_chunks?: ContentChunk[];
}
