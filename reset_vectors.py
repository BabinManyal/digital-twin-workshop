"""
Reset Upstash Vector Database
Delete all existing vectors and re-upload with proper metadata
"""

import os
from dotenv import load_dotenv
from upstash_vector import Index

# Load environment variables
load_dotenv()

def reset_database():
    """Delete all vectors from Upstash"""
    print("🔄 Connecting to Upstash Vector...")
    
    try:
        index = Index.from_env()
        print("✅ Connected successfully!")
        
        # Check current count
        info = index.info()
        current_count = getattr(info, 'vector_count', 0)
        print(f"📊 Current vectors in database: {current_count}")
        
        if current_count == 0:
            print("✅ Database already empty!")
            return True
        
        # Reset the database
        print(f"🗑️  Deleting {current_count} vectors...")
        index.reset()
        print("✅ Database reset successfully!")
        
        # Verify deletion
        info = index.info()
        new_count = getattr(info, 'vector_count', 0)
        print(f"📊 Vectors after reset: {new_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error resetting database: {str(e)}")
        return False

if __name__ == "__main__":
    print("🤖 Upstash Vector Database Reset Tool")
    print("=" * 50)
    
    # Confirm action
    confirm = input("\n⚠️  This will DELETE ALL vectors. Continue? (yes/no): ")
    
    if confirm.lower() == 'yes':
        if reset_database():
            print("\n✅ Database reset complete!")
            print("💡 Run 'python embed_digitaltwin.py' to re-upload with proper metadata")
    else:
        print("❌ Reset cancelled")
