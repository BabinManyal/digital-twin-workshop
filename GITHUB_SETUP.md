# GitHub Repository Setup Guide

## ✅ Git Initialized

Your local git repository has been successfully initialized with all project files committed!

## 🚀 Next Steps: Push to GitHub

### Option 1: Create Repository via GitHub Website

1. **Go to GitHub:**
   - Visit https://github.com/new
   - Or click the "+" icon in the top right → "New repository"

2. **Create Repository:**
   - **Repository name:** `digital-twin-workshop` (or your preferred name)
   - **Description:** "AI-powered professional profile assistant using RAG with Upstash Vector and Groq"
   - **Visibility:** Choose Public or Private
   - ⚠️ **DO NOT** initialize with README, .gitignore, or license (we already have these)

3. **Click "Create repository"**

4. **Push your code:**
   ```bash
   cd /Users/mclovin/digital-twin-workshop
   
   # Add the remote repository
   git remote add origin https://github.com/YOUR_USERNAME/digital-twin-workshop.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

### Option 2: Create Repository via GitHub CLI (gh)

If you have GitHub CLI installed:

```bash
cd /Users/mclovin/digital-twin-workshop

# Login to GitHub (if not already)
gh auth login

# Create repository and push
gh repo create digital-twin-workshop --public --source=. --push

# Or for private repository
gh repo create digital-twin-workshop --private --source=. --push
```

## 📝 Configure Git User (Optional)

Set your git identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# If you want to update the commit author
git commit --amend --reset-author --no-edit
```

## 🔑 GitHub Authentication

### HTTPS (Recommended for beginners)

Use a Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use token as password when pushing

### SSH (Recommended for frequent use)

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add SSH key
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard (macOS)
pbcopy < ~/.ssh/id_ed25519.pub

# Add to GitHub:
# Settings → SSH and GPG keys → New SSH key
# Paste the key and save

# Update remote to use SSH
git remote set-url origin git@github.com:YOUR_USERNAME/digital-twin-workshop.git
```

## 📊 Useful Git Commands

### Checking Status
```bash
# View current status
git status

# View commit history
git log --oneline --graph --all

# View remote repositories
git remote -v
```

### Making Changes
```bash
# Stage changes
git add .
git add filename.py

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

### Branching
```bash
# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# List branches
git branch -a

# Push branch to GitHub
git push -u origin feature/new-feature

# Merge branch
git checkout main
git merge feature/new-feature
```

### Undoing Changes
```bash
# Discard changes in working directory
git checkout -- filename.py

# Unstage file
git reset HEAD filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

## 🔒 Important Files Already Ignored

The `.gitignore` file already excludes:
- ✅ `.env` files (sensitive API keys)
- ✅ `.venv/` (Python virtual environment)
- ✅ `node_modules/` (Node.js dependencies)
- ✅ `.next/` (Next.js build files)
- ✅ `dist/` (Compiled MCP server)
- ✅ `.DS_Store` and IDE files

## 📋 Recommended Repository Settings

After pushing to GitHub, configure:

1. **Branch Protection:**
   - Settings → Branches → Add rule for `main`
   - Enable "Require a pull request before merging"

2. **Repository Topics:**
   - Add topics: `ai`, `rag`, `nextjs`, `typescript`, `python`, `mcp`, `groq`, `upstash`

3. **About Section:**
   - Add description and website URL
   - Add topics for discoverability

4. **GitHub Actions (Optional):**
   - Set up CI/CD for automatic testing and deployment

## 🎯 Common Workflows

### Making Updates
```bash
# 1. Make your changes to files
# 2. Stage and commit
git add .
git commit -m "Add new feature or fix bug"

# 3. Push to GitHub
git push
```

### Working with Others
```bash
# Before starting work, get latest changes
git pull

# Create feature branch
git checkout -b feature/your-feature

# Make changes, commit, and push
git add .
git commit -m "Your changes"
git push -u origin feature/your-feature

# Create Pull Request on GitHub
# After review and merge, update main
git checkout main
git pull
git branch -d feature/your-feature
```

## 📖 Resources

- [GitHub Documentation](https://docs.github.com)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Conventional Commits](https://www.conventionalcommits.org/)

## ✅ Current Status

- ✅ Git repository initialized
- ✅ Initial commit created (27 files)
- ✅ `.gitignore` configured
- ✅ Ready to push to GitHub

**Next step:** Create a GitHub repository and push your code!
