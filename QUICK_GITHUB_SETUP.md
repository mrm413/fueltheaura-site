# Quick GitHub Setup - Copy & Paste Commands

## 🚀 Super Fast GitHub Deployment

Just copy and paste these commands in PowerShell!

## Step 1: Navigate to Your Folder

```powershell
cd F:\FuelTheAura\AI-System
```

## Step 2: Initialize Git and Push to GitHub

```powershell
# Initialize Git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Fuel The Aura AI Content System"

# Add your GitHub repository (REPLACE YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/fueltheaura-ai-system.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Done! 🎉

Your AI system is now on GitHub!

## 📥 To Download and Use on Any Computer

```powershell
# Clone the repository
git clone https://github.com/YOUR_USERNAME/fueltheaura-ai-system.git

# Navigate to folder
cd fueltheaura-ai-system

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Run the system
python INTEGRATED_AI_SYSTEM_FINAL.py
```

## 🔄 To Update After Making Changes

```powershell
git add .
git commit -m "Updated AI system"
git push origin main
```

That's it! Simple and fast! 🚀