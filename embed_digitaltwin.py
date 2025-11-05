"""
Digital Twin RAG Application
Based on Binal's production implementation
- Upstash Vector: Built-in embeddings and vector storage
- Groq: Ultra-fast LLM inference
"""

import os
import json
import time
from dotenv import load_dotenv
from upstash_vector import Index
from groq import Groq
from groq import RateLimitError, APIError, AuthenticationError
from groq_monitor import GroqUsageMonitor

# Load environment variables
load_dotenv()

# Constants
JSON_FILE = "digitaltwin.json"
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
DEFAULT_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
GROQ_TEMPERATURE = float(os.getenv('GROQ_TEMPERATURE', '0.7'))
GROQ_MAX_TOKENS = int(os.getenv('GROQ_MAX_TOKENS', '500'))
GROQ_TIMEOUT = float(os.getenv('GROQ_TIMEOUT', '30.0'))

# Initialize usage monitor
usage_monitor = GroqUsageMonitor()

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

def setup_vector_database():
    """Setup Upstash Vector database with built-in embeddings"""
    print("🔄 Setting up Upstash Vector database...")
    
    try:
        index = Index.from_env()
        print("✅ Connected to Upstash Vector successfully!")
        
        # Check current vector count
        try:
            info = index.info()
            current_count = getattr(info, 'vector_count', 0)
            print(f"📊 Current vectors in database: {current_count}")
        except:
            current_count = 0
        
        # Load data if database is empty
        if current_count == 0:
            print("📝 Loading your professional profile...")
            
            try:
                with open(JSON_FILE, "r", encoding="utf-8") as f:
                    profile_data = json.load(f)
            except FileNotFoundError:
                print(f"❌ {JSON_FILE} not found!")
                return None
            
            # Prepare vectors from content chunks
            vectors = []
            content_chunks = profile_data.get('content_chunks', [])
            
            if not content_chunks:
                print("❌ No content chunks found in profile data")
                return None
            
            for chunk in content_chunks:
                enriched_text = f"{chunk['title']}: {chunk['content']}"
                
                vectors.append((
                    chunk['id'],
                    enriched_text,
                    {
                        "title": chunk['title'],
                        "type": chunk['type'],
                        "content": chunk['content'],
                        "category": chunk.get('metadata', {}).get('category', ''),
                        "tags": chunk.get('metadata', {}).get('tags', [])
                    }
                ))
            
            # Upload vectors
            index.upsert(vectors=vectors)
            print(f"✅ Successfully uploaded {len(vectors)} content chunks!")
        
        return index
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
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

def generate_response_with_groq(client, prompt, model=DEFAULT_MODEL, max_retries=3, question=None):
    """Generate response using Groq with enhanced error handling and retry logic"""
    start_time = time.time()
    
    for attempt in range(max_retries):
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
                max_tokens=GROQ_MAX_TOKENS,
                timeout=GROQ_TIMEOUT
            )
            
            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000
            
            # Log token usage for monitoring
            usage = completion.usage
            if usage:
                print(f"📊 Tokens: {usage.prompt_tokens} prompt + {usage.completion_tokens} completion = {usage.total_tokens} total")
                
                # Log to usage monitor
                usage_monitor.log_request(
                    model=model,
                    prompt_tokens=usage.prompt_tokens,
                    completion_tokens=usage.completion_tokens,
                    latency_ms=latency_ms,
                    question=question,
                    success=True
                )
            
            return completion.choices[0].message.content.strip()
        
        except RateLimitError as e:
            latency_ms = (time.time() - start_time) * 1000
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 1  # Exponential backoff: 1s, 2s, 4s
                print(f"⏳ Rate limit hit (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"❌ Rate limit exceeded: {str(e)}")
                usage_monitor.log_request(
                    model=model, prompt_tokens=0, completion_tokens=0,
                    latency_ms=latency_ms, question=question,
                    success=False, error=f"Rate limit: {str(e)}"
                )
                return "❌ Service temporarily unavailable due to high demand. Please try again in a moment."
        
        except AuthenticationError as e:
            latency_ms = (time.time() - start_time) * 1000
            print(f"❌ Authentication error: {str(e)}")
            usage_monitor.log_request(
                model=model, prompt_tokens=0, completion_tokens=0,
                latency_ms=latency_ms, question=question,
                success=False, error=f"Auth error: {str(e)}"
            )
            return "❌ Configuration error: Invalid API credentials. Please check your GROQ_API_KEY."
        
        except APIError as e:
            latency_ms = (time.time() - start_time) * 1000
            print(f"❌ Groq API error: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = 2
                print(f"⏳ Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                usage_monitor.log_request(
                    model=model, prompt_tokens=0, completion_tokens=0,
                    latency_ms=latency_ms, question=question,
                    success=False, error=f"API error: {str(e)}"
                )
                return f"❌ Unable to generate response: {str(e)}. Please try again later."
        
        except TimeoutError as e:
            latency_ms = (time.time() - start_time) * 1000
            print(f"⏱️ Request timeout: {str(e)}")
            if attempt < max_retries - 1:
                print(f"⏳ Retrying (attempt {attempt + 2}/{max_retries})...")
            else:
                usage_monitor.log_request(
                    model=model, prompt_tokens=0, completion_tokens=0,
                    latency_ms=latency_ms, question=question,
                    success=False, error="Timeout"
                )
                return "⏱️ Request timeout: The AI service is taking too long to respond. Please try again."
        
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            print(f"❌ Unexpected error: {type(e).__name__}: {str(e)}")
            if attempt < max_retries - 1:
                print(f"⏳ Retrying (attempt {attempt + 2}/{max_retries})...")
                time.sleep(1)
            else:
                usage_monitor.log_request(
                    model=model, prompt_tokens=0, completion_tokens=0,
                    latency_ms=latency_ms, question=question,
                    success=False, error=f"{type(e).__name__}: {str(e)}"
                )
                return f"❌ An unexpected error occurred: {str(e)}"
    
    return "❌ Failed to generate response after multiple attempts. Please try again later."

def rag_query(index, groq_client, question):
    """Perform RAG query using Upstash Vector + Groq"""
    try:
        # Step 1: Query vector database
        results = query_vectors(index, question, top_k=3)
        
        if not results or len(results) == 0:
            return "I don't have specific information about that topic."
        
        # Step 2: Extract relevant content
        print("🧠 Searching your professional profile...")
        
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
            return "I found some information but couldn't extract details."
        
        print(f"⚡ Generating personalized response...")
        
        # Step 3: Generate response with context
        context = "\n\n".join(top_docs)
        prompt = f"""Based on the following information about yourself, answer the question.
Speak in first person as if you are describing your own background.

Your Information:
{context}

Question: {question}

Provide a helpful, professional response:"""
        
        response = generate_response_with_groq(groq_client, prompt, question=question)
        return response
    
    except Exception as e:
        return f"❌ Error during query: {str(e)}"

def main():
    """Main application loop"""
    print("🤖 Your Digital Twin - AI Profile Assistant")
    print("=" * 50)
    print("🔗 Vector Storage: Upstash (built-in embeddings)")
    print(f"⚡ AI Inference: Groq ({DEFAULT_MODEL})")
    print("📋 Data Source: Your Professional Profile\n")
    
    # Setup clients
    groq_client = setup_groq_client()
    if not groq_client:
        return
    
    index = setup_vector_database()
    if not index:
        return
    
    print("✅ Your Digital Twin is ready!\n")
    
    # Interactive chat loop
    print("🤖 Chat with your AI Digital Twin!")
    print("Ask questions about your experience, skills, projects, or career goals.")
    print("Type 'exit' to quit.\n")
    
    print("💭 Try asking:")
    print("  - 'Tell me about your work experience'")
    print("  - 'What are your technical skills?'")
    print("  - 'Describe your career goals'")
    print()
    
    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            print("👋 Thanks for chatting with your Digital Twin!")
            # Show usage summary before exiting
            usage_monitor.print_summary()
            break
        
        if question.strip():
            answer = rag_query(index, groq_client, question)
            print(f"🤖 Digital Twin: {answer}\n")

if __name__ == "__main__":
    main()