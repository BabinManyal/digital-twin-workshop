#!/bin/bash

echo "🚀 Vercel Deployment - Pre-Flight Checklist"
echo "==========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "digital-twin-frontend" ]; then
    echo "❌ Error: Run this from the project root directory"
    exit 1
fi

cd digital-twin-frontend

echo "📋 Checking deployment readiness..."
echo ""

# 1. Check package.json exists
if [ -f "package.json" ]; then
    echo "✅ package.json found"
else
    echo "❌ package.json not found"
    exit 1
fi

# 2. Check .env.local exists
if [ -f ".env.local" ]; then
    echo "✅ .env.local found"
    
    # Check for required environment variables
    if grep -q "UPSTASH_VECTOR_REST_URL" .env.local; then
        echo "  ✅ UPSTASH_VECTOR_REST_URL configured"
    else
        echo "  ❌ UPSTASH_VECTOR_REST_URL missing"
    fi
    
    if grep -q "UPSTASH_VECTOR_REST_TOKEN" .env.local; then
        echo "  ✅ UPSTASH_VECTOR_REST_TOKEN configured"
    else
        echo "  ❌ UPSTASH_VECTOR_REST_TOKEN missing"
    fi
    
    if grep -q "GROQ_API_KEY" .env.local; then
        echo "  ✅ GROQ_API_KEY configured"
    else
        echo "  ❌ GROQ_API_KEY missing"
    fi
else
    echo "❌ .env.local not found"
    exit 1
fi

# 3. Check if node_modules exists
if [ -d "node_modules" ]; then
    echo "✅ node_modules installed"
else
    echo "⚠️  node_modules not found - run 'npm install'"
fi

# 4. Check if app directory exists
if [ -d "app" ]; then
    echo "✅ Next.js app directory found"
else
    echo "❌ Next.js app directory not found"
    exit 1
fi

# 5. Check if API route exists
if [ -f "app/api/query/route.ts" ]; then
    echo "✅ API route (/api/query) exists"
else
    echo "❌ API route not found"
fi

# 6. Check Git status
cd ..
echo ""
echo "📦 Git Status:"
echo ""

if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "✅ Git repository initialized"
    
    # Check for uncommitted changes
    if [[ -z $(git status -s) ]]; then
        echo "✅ No uncommitted changes"
    else
        echo "⚠️  Uncommitted changes detected:"
        git status -s
        echo ""
        echo "💡 Commit changes before deploying:"
        echo "   git add ."
        echo "   git commit -m 'Prepare for Vercel deployment'"
        echo "   git push origin main"
    fi
    
    # Check remote
    if git remote get-url origin > /dev/null 2>&1; then
        REMOTE_URL=$(git remote get-url origin)
        echo "✅ Remote repository: $REMOTE_URL"
    else
        echo "⚠️  No remote repository configured"
    fi
else
    echo "❌ Not a Git repository"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎯 Deployment Checklist:"
echo ""
echo "Before deploying to Vercel, ensure:"
echo ""
echo "1. ✅ Local app works"
echo "   Test: cd digital-twin-frontend && npm run dev"
echo "   Visit: http://localhost:3000"
echo "   Try a test query"
echo ""
echo "2. ✅ Environment variables ready"
echo "   UPSTASH_VECTOR_REST_URL"
echo "   UPSTASH_VECTOR_REST_TOKEN"
echo "   GROQ_API_KEY"
echo ""
echo "3. ✅ Code committed to Git"
echo "   git add ."
echo "   git commit -m 'Ready for deployment'"
echo "   git push origin main"
echo ""
echo "4. ✅ Vercel account ready"
echo "   Sign up: https://vercel.com"
echo "   Connect GitHub account"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Next Steps:"
echo ""
echo "1. Visit: https://vercel.com"
echo "2. Click: 'Add New...' → 'Project'"
echo "3. Import: BabinManyal/digital-twin-workshop"
echo "4. Set root directory: digital-twin-frontend"
echo "5. Add environment variables (3 total)"
echo "6. Click: 'Deploy'"
echo ""
echo "📖 Full guide: See VERCEL_DEPLOYMENT_GUIDE.md"
echo ""
echo "🚀 Ready to deploy!"
echo ""
