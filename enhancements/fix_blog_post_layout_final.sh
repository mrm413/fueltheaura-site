#!/bin/bash

# Fix Blog Post Layout - Update AI System to Use blog-post.njk
# This ensures all future AI-generated posts use the styled blog-post layout

echo "🔧 Fixing blog post layout in AI system..."

cd /opt/fueltheaura-ai

# Backup the current file
cp premium_ai_system.py premium_ai_system.py.layout_backup

# Update the layout in premium_ai_system.py
sed -i 's/layout: "main.njk"/layout: "blog-post.njk"/' premium_ai_system.py

echo "✅ Updated AI system to use blog-post.njk layout"
echo ""
echo "🔄 Restarting content generation service..."
systemctl restart fueltheaura-ai.service

echo ""
echo "✅ All done! Future blog posts will now have proper styling."
echo ""
echo "📊 Check status with:"
echo "   systemctl status fueltheaura-ai.service"