"""
Groq Streaming Support for Digital Twin
Demonstrates streaming responses for better user experience
"""

import os
import time
from dotenv import load_dotenv
from groq import Groq
from upstash_vector import Index

# Load environment variables
load_dotenv()

# Constants
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
DEFAULT_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
GROQ_TEMPERATURE = float(os.getenv('GROQ_TEMPERATURE', '1.0'))
GROQ_MAX_TOKENS = int(os.getenv('GROQ_MAX_TOKENS', '1024'))


def setup_groq_client():
    """Setup Groq client"""
    if not GROQ_API_KEY:
        print("❌ GROQ_API_KEY not found in .env file")
        return None
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq client initialized successfully!")
        return client
    except Exception as e:
        print(f"❌ Error initializing Groq client: {str(e)}")
        return None


def generate_streaming_response(client, prompt, model=DEFAULT_MODEL):
    """
    Generate streaming response using Groq
    
    This provides real-time output as the model generates text,
    improving perceived performance and user experience.
    
    Args:
        client: Groq client instance
        prompt: User prompt/question
        model: Model name (default: llama-3.1-8b-instant)
    
    Returns:
        Complete response text
    """
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI digital twin. Answer questions as if you are the person, speaking in first person about your background, skills, and experience."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=GROQ_TEMPERATURE,
            max_completion_tokens=GROQ_MAX_TOKENS,  # Note: Different from max_tokens
            top_p=1,
            stream=True,  # Enable streaming
            stop=None
        )
        
        print("🤖 Digital Twin: ", end="", flush=True)
        full_response = ""
        
        # Stream response chunks in real-time
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            print(content, end="", flush=True)
            full_response += content
        
        print("\n")  # New line after streaming completes
        return full_response
        
    except Exception as e:
        print(f"\n❌ Error generating streaming response: {str(e)}")
        return None


def query_vectors(index, query_text, top_k=3):
    """Query Upstash Vector for similar vectors"""
    try:
        results = index.query(
            data=query_text,
            top_k=top_k,
            include_metadata=True
        )
        return results
    except Exception as e:
        print(f"❌ Error querying vectors: {str(e)}")
        return None


def rag_query_streaming(index, groq_client, question):
    """
    Perform RAG query with streaming response
    
    This combines vector search with streaming LLM generation
    for a responsive user experience.
    """
    try:
        # Step 1: Query vector database
        print("🧠 Searching your professional profile...")
        results = query_vectors(index, question, top_k=3)
        
        if not results or len(results) == 0:
            print("🤖 Digital Twin: I don't have specific information about that topic.\n")
            return None
        
        # Step 2: Extract relevant content
        top_docs = []
        for result in results:
            metadata = result.metadata or {}
            title = metadata.get('title', 'Information')
            content = metadata.get('content', '')
            score = result.score
            
            print(f"🔹 Found: {title} (Relevance: {score:.3f})")
            if content:
                top_docs.append(f"{title}: {content}")
        
        if not top_docs:
            print("🤖 Digital Twin: I found some information but couldn't extract details.\n")
            return None
        
        print(f"⚡ Generating personalized streaming response...\n")
        
        # Step 3: Generate streaming response with context
        context = "\n\n".join(top_docs)
        prompt = f"""Based on the following information about yourself, answer the question.
Speak in first person as if you are describing your own background.

Your Information:
{context}

Question: {question}

Provide a helpful, professional response:"""
        
        response = generate_streaming_response(groq_client, prompt)
        return response
    
    except Exception as e:
        print(f"❌ Error during query: {str(e)}")
        return None


def main():
    """Main streaming demo"""
    print("🤖 Your Digital Twin - Streaming Demo")
    print("=" * 50)
    print("⚡ AI Inference: Groq (Streaming Enabled)")
    print(f"📋 Model: {DEFAULT_MODEL}\n")
    
    # Setup clients
    groq_client = setup_groq_client()
    if not groq_client:
        return
    
    try:
        index = Index.from_env()
        print("✅ Connected to Upstash Vector successfully!\n")
    except Exception as e:
        print(f"❌ Error connecting to vector database: {str(e)}")
        return
    
    print("✅ Digital Twin ready with streaming!\n")
    
    # Demo queries
    demo_questions = [
        "What are your Python skills?",
        "Tell me about your work experience at TechCorp",
        "What are your career goals?"
    ]
    
    print("🎬 Running streaming demo with sample questions...\n")
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n{'='*60}")
        print(f"Demo Query {i}/{len(demo_questions)}: {question}")
        print('='*60 + '\n')
        
        start_time = time.time()
        response = rag_query_streaming(index, groq_client, question)
        elapsed = time.time() - start_time
        
        if response:
            print(f"⏱️ Total time: {elapsed:.2f}s")
            print(f"📊 Response length: {len(response)} characters\n")
        
        if i < len(demo_questions):
            print("⏸️ Waiting 2 seconds before next query...\n")
            time.sleep(2)
    
    print("\n" + "="*60)
    print("🎉 Streaming demo complete!")
    print("="*60)
    print("\n💡 Streaming Benefits:")
    print("  - Real-time output (better perceived performance)")
    print("  - Lower latency to first token")
    print("  - Better UX for longer responses")
    print("  - Same accuracy as non-streaming")


if __name__ == "__main__":
    main()
