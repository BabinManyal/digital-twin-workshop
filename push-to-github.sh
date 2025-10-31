#!/bin/bash

# Digital Twin Workshop - GitHub Push Helper Script
# This script helps you push your repository to GitHub

echo "🚀 Digital Twin Workshop - GitHub Push Helper"
echo "=============================================="
echo ""

# Check if git is configured
if [ -z "$(git config --global user.name)" ]; then
    echo "⚠️  Git user not configured."
    echo ""
    read -p "Enter your GitHub username: " github_username
    read -p "Enter your email: " github_email
    
    git config --global user.name "$github_username"
    git config --global user.email "$github_email"
    
    echo "✅ Git configured with:"
    echo "   Name: $github_username"
    echo "   Email: $github_email"
    echo ""
else
    github_username=$(git config --global user.name)
    echo "✅ Git already configured as: $github_username"
    echo ""
fi

# Check if remote already exists
if git remote get-url origin > /dev/null 2>&1; then
    echo "✅ Remote 'origin' already exists:"
    git remote get-url origin
    echo ""
    read -p "Do you want to push to this remote? (y/n): " push_confirm
    if [ "$push_confirm" = "y" ]; then
        echo ""
        echo "📤 Pushing to GitHub..."
        git push -u origin main
    fi
else
    echo "📝 No remote repository configured."
    echo ""
    echo "Please follow these steps:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: digital-twin-workshop"
    echo "3. Don't initialize with README, .gitignore, or license"
    echo "4. Click 'Create repository'"
    echo ""
    read -p "Enter your GitHub username: " gh_user
    
    repo_url="https://github.com/${gh_user}/digital-twin-workshop.git"
    
    echo ""
    echo "🔗 Adding remote: $repo_url"
    git remote add origin "$repo_url"
    
    echo ""
    echo "📤 Pushing to GitHub..."
    git branch -M main
    git push -u origin main
fi

echo ""
echo "✅ Done! Check your repository at:"
echo "   https://github.com/$(git config --global user.name)/digital-twin-workshop"
