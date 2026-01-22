# GitHub Push Script for Windows
# This PowerShell script helps you push InsightPro to GitHub

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "InsightPro - GitHub Push Script (Windows)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    git --version | Out-Null
    Write-Host "✅ Git is installed" -ForegroundColor Green
}
catch {
    Write-Host "❌ Git is not installed. Please install git first." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 1: Initialize if needed
if (!(Test-Path ".git")) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git initialized" -ForegroundColor Green
    Write-Host ""
}
else {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
    Write-Host ""
}

# Step 2: Add all files
Write-Host "📝 Adding all files to git..." -ForegroundColor Yellow
git add .
Write-Host "✅ Files added" -ForegroundColor Green
Write-Host ""

# Step 3: Check git status
Write-Host "📋 Current git status:" -ForegroundColor Yellow
git status --short
Write-Host ""

# Step 4: Commit
Write-Host "💾 Creating commit..." -ForegroundColor Yellow
git commit -m "feat: InsightPro v2.1 - Production Ready SaaS Platform

- Real-time inventory management with ML analytics
- AI-powered supply chain insights via Google Gemini
- Interactive dashboard with Plotly visualization
- Predictive stockout forecasting
- Premium glassmorphic UI
- Comprehensive documentation and CI/CD setup" -ErrorAction SilentlyContinue

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Commit created" -ForegroundColor Green
}
else {
    Write-Host "⚠️ Nothing to commit" -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Add remote
Write-Host "🔗 Adding remote repository..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin "https://github.com/Nishant17s/MS_ELEVATE-COPILOT-PROJECT-.git"
Write-Host "✅ Remote added" -ForegroundColor Green
Write-Host ""

# Step 6: Rename branch to main
Write-Host "🌿 Setting default branch to main..." -ForegroundColor Yellow
git branch -M main
Write-Host "✅ Branch renamed to main" -ForegroundColor Green
Write-Host ""

# Step 7: Push to GitHub
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
}
else {
    Write-Host "❌ Push failed. Check your repository URL and credentials." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🎉 InsightPro is now on GitHub!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Repository: https://github.com/Nishant17s/MS_ELEVATE-COPILOT-PROJECT-.git" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Visit your GitHub repository"
Write-Host "2. Go to Settings → General"
Write-Host "3. Set About with description"
Write-Host "4. Add topics: streamlit, inventory-management, ml, saas"
Write-Host "5. Enable GitHub Pages (optional)"
Write-Host ""
Write-Host "Share the link with your reviewers!" -ForegroundColor Green
Write-Host ""
