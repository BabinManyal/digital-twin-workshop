"""
Groq Usage Monitor
Track token usage, request counts, latency, and estimated costs for Groq API calls.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class GroqUsageMonitor:
    """Monitor and log Groq API usage for cost tracking and optimization"""
    
    def __init__(self, log_file: str = "groq_usage.json"):
        self.log_file = Path(log_file)
        self.usage_data = self._load_usage()
    
    def _load_usage(self) -> Dict:
        """Load existing usage data from file"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️ Warning: Could not load usage data: {e}")
                return self._init_usage_data()
        return self._init_usage_data()
    
    def _init_usage_data(self) -> Dict:
        """Initialize empty usage data structure"""
        return {
            "total_requests": 0,
            "total_tokens": 0,
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_latency_ms": 0,
            "requests": []
        }
    
    def log_request(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        latency_ms: float,
        question: Optional[str] = None,
        success: bool = True,
        error: Optional[str] = None
    ) -> Dict:
        """
        Log a single Groq API request
        
        Args:
            model: Model name (e.g., 'llama-3.1-8b-instant')
            prompt_tokens: Number of tokens in prompt
            completion_tokens: Number of tokens in completion
            latency_ms: Request latency in milliseconds
            question: Optional question text (truncated for privacy)
            success: Whether request succeeded
            error: Error message if request failed
        
        Returns:
            Dict with request details
        """
        total_tokens = prompt_tokens + completion_tokens
        
        request_data = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "latency_ms": round(latency_ms, 2),
            "success": success,
            "question_preview": question[:50] + "..." if question and len(question) > 50 else question,
            "error": error
        }
        
        # Update totals
        if success:
            self.usage_data["total_requests"] += 1
            self.usage_data["total_tokens"] += total_tokens
            self.usage_data["total_prompt_tokens"] += prompt_tokens
            self.usage_data["total_completion_tokens"] += completion_tokens
            self.usage_data["total_latency_ms"] += latency_ms
        
        # Add to request log
        self.usage_data["requests"].append(request_data)
        
        # Keep only last 1000 requests to prevent file bloat
        if len(self.usage_data["requests"]) > 1000:
            self.usage_data["requests"] = self.usage_data["requests"][-1000:]
        
        # Save to file
        self._save_usage()
        
        return request_data
    
    def _save_usage(self):
        """Save usage data to file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except IOError as e:
            print(f"⚠️ Warning: Could not save usage data: {e}")
    
    def get_summary(self) -> Dict:
        """
        Get usage summary statistics
        
        Returns:
            Dict with summary metrics
        """
        total_requests = self.usage_data["total_requests"]
        total_tokens = self.usage_data["total_tokens"]
        total_latency = self.usage_data["total_latency_ms"]
        
        # Calculate averages
        avg_tokens = total_tokens / total_requests if total_requests > 0 else 0
        avg_latency = total_latency / total_requests if total_requests > 0 else 0
        avg_prompt_tokens = self.usage_data["total_prompt_tokens"] / total_requests if total_requests > 0 else 0
        avg_completion_tokens = self.usage_data["total_completion_tokens"] / total_requests if total_requests > 0 else 0
        
        # Calculate success rate from recent requests
        recent_requests = self.usage_data["requests"][-100:] if self.usage_data["requests"] else []
        success_count = sum(1 for r in recent_requests if r.get("success", True))
        success_rate = (success_count / len(recent_requests) * 100) if recent_requests else 100.0
        
        # Groq pricing (free tier for now, but track for future)
        # Free tier: 14,400 tokens/min, 6,000 requests/min
        estimated_cost_usd = 0.0  # Free tier
        
        return {
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "total_prompt_tokens": self.usage_data["total_prompt_tokens"],
            "total_completion_tokens": self.usage_data["total_completion_tokens"],
            "avg_tokens_per_request": round(avg_tokens, 2),
            "avg_prompt_tokens": round(avg_prompt_tokens, 2),
            "avg_completion_tokens": round(avg_completion_tokens, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "success_rate_percent": round(success_rate, 2),
            "estimated_cost_usd": estimated_cost_usd,
            "note": "Currently on Groq free tier (14,400 tokens/min, 6,000 req/min)"
        }
    
    def print_summary(self):
        """Print a formatted summary to console"""
        summary = self.get_summary()
        
        print("\n" + "=" * 60)
        print("📊 Groq API Usage Summary")
        print("=" * 60)
        print(f"Total Requests:       {summary['total_requests']:,}")
        print(f"Total Tokens:         {summary['total_tokens']:,}")
        print(f"  - Prompt:           {summary['total_prompt_tokens']:,}")
        print(f"  - Completion:       {summary['total_completion_tokens']:,}")
        print(f"Avg Tokens/Request:   {summary['avg_tokens_per_request']:.2f}")
        print(f"Avg Latency:          {summary['avg_latency_ms']:.2f} ms")
        print(f"Success Rate:         {summary['success_rate_percent']:.2f}%")
        print(f"Estimated Cost:       ${summary['estimated_cost_usd']:.4f}")
        print(f"Status:               {summary['note']}")
        print("=" * 60 + "\n")
    
    def get_recent_requests(self, count: int = 10) -> List[Dict]:
        """Get the most recent N requests"""
        return self.usage_data["requests"][-count:] if self.usage_data["requests"] else []
    
    def clear_history(self):
        """Clear all usage history (use with caution)"""
        self.usage_data = self._init_usage_data()
        self._save_usage()
        print("✅ Usage history cleared")


# Example usage
if __name__ == "__main__":
    # Create monitor instance
    monitor = GroqUsageMonitor()
    
    # Example: Log a successful request
    monitor.log_request(
        model="llama-3.1-8b-instant",
        prompt_tokens=150,
        completion_tokens=300,
        latency_ms=750.5,
        question="What are your Python skills?",
        success=True
    )
    
    # Example: Log a failed request
    monitor.log_request(
        model="llama-3.1-8b-instant",
        prompt_tokens=120,
        completion_tokens=0,
        latency_ms=1000.0,
        question="Tell me about your experience",
        success=False,
        error="Rate limit exceeded"
    )
    
    # Print summary
    monitor.print_summary()
    
    # Get recent requests
    recent = monitor.get_recent_requests(5)
    print(f"Recent requests: {len(recent)}")
    for req in recent:
        status = "✅" if req["success"] else "❌"
        print(f"{status} {req['timestamp']}: {req['total_tokens']} tokens, {req['latency_ms']}ms")
