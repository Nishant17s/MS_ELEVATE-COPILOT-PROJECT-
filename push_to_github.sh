#!/bin/bash
# GitHub Push Script
# This script helps you push InsightPro to GitHub

set -e

echo "=========================================="
echo "InsightPro - GitHub Push Script"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Step 1: Initialize if needed
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
    echo ""
else
    echo "✅ Git repository already initialized"
    echo ""
fi

# Step 2: Add all files
echo "📝 Adding all files to git..."
git add .
echo "✅ Files added"
echo ""

# Step 3: Check git status
echo "📋 Current git status:"
git status --short
echo ""

# Step 4: Commit
echo "💾 Creating commit..."
git commit -m "feat: InsightPro v2.1 - Production Ready SaaS Platform

- Real-time inventory management with ML analytics
- AI-powered supply chain insights via Google Gemini
- Interactive dashboard with Plotly visualization
- Predictive stockout forecasting
- Premium glassmorphic UI
- Comprehensive documentation and CI/CD setup" || echo "⚠️ Nothing to commit"
echo "✅ Commit created"
echo ""

# Step 5: Ask for repository URL
read -p "🔗 Enter your GitHub repository URL (https://github.com/username/InsightPro.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ Repository URL is required"
    exit 1
fi

# Step 6: Add remote
echo "🔗 Adding remote repository..."
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"
echo "✅ Remote added"
echo ""

# Step 7: Rename branch to main
echo "🌿 Setting default branch to main..."
git branch -M main
echo "✅ Branch renamed to main"
echo ""

# Step 8: Push to GitHub
echo "🚀 Pushing to GitHub..."
git push -u origin main
echo "✅ Successfully pushed to GitHub!"
echo ""

echo "=========================================="
echo "🎉 InsightPro is now on GitHub!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Visit: $REPO_URL"
echo "2. Go to Settings → General"
echo "3. Set 'About' with description"
echo "4. Add topics: streamlit, inventory-management, ml"
echo "5. Enable GitHub Pages (optional)"
echo ""
echo "Share the link with your reviewers!"
echo ""
