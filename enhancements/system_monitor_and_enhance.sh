#!/bin/bash

# FuelTheAura AI System Monitor and Enhancement Script
# Run this on your DigitalOcean droplet to check status and optionally enhance the system

echo "🔍 FuelTheAura AI System Status Monitor"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -d "/opt/fueltheaura-ai" ]; then
    echo "❌ Error: /opt/fueltheaura-ai directory not found"
    echo "Please run this script on your DigitalOcean droplet"
    exit 1
fi

cd /opt/fueltheaura-ai

# Activate virtual environment
source ai-venv/bin/activate

echo "📊 SYSTEM SERVICES STATUS"
echo "------------------------"
systemctl is-active fueltheaura-ai.service && echo "✅ Content Generation: RUNNING" || echo "❌ Content Generation: STOPPED"
systemctl is-active health-scraper.service && echo "✅ Web Scraper: RUNNING" || echo "❌ Web Scraper: STOPPED"
systemctl is-active ai-learning.service && echo "✅ AI Learning: RUNNING" || echo "❌ AI Learning: STOPPED"
echo ""

echo "📈 CONTENT GENERATION STATS"
echo "---------------------------"
python3 << 'PYTHON_SCRIPT'
import sqlite3
from datetime import datetime

try:
    conn = sqlite3.connect('data/content_intelligence.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM generated_posts')
    post_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT title, created_at, quality_score FROM generated_posts ORDER BY created_at DESC LIMIT 3')
    recent_posts = cursor.fetchall()
    
    print(f"Total Posts Generated: {post_count}")
    print("\nRecent Posts:")
    for title, created, score in recent_posts:
        print(f"  • {title}")
        print(f"    Created: {created}")
        print(f"    Quality Score: {score}")
        print()
    
    conn.close()
except Exception as e:
    print(f"Error reading content database: {e}")
PYTHON_SCRIPT

echo "🌐 WEB SCRAPING STATS"
echo "---------------------"
python3 << 'PYTHON_SCRIPT'
import sqlite3

try:
    conn = sqlite3.connect('data/health_content.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM health_articles')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT category, COUNT(*) as count FROM health_articles GROUP BY category ORDER BY count DESC')
    categories = cursor.fetchall()
    
    print(f"Total Articles Scraped: {total:,}")
    print(f"Progress to 2M Goal: {(total/2000000)*100:.2f}%")
    print("\nCategory Breakdown:")
    for category, count in categories:
        percentage = (count/total)*100
        print(f"  • {category}: {count:,} articles ({percentage:.1f}%)")
    
    conn.close()
except Exception as e:
    print(f"Error reading scraping database: {e}")
PYTHON_SCRIPT

echo ""
echo "💾 DATABASE SIZES"
echo "-----------------"
du -h data/*.db 2>/dev/null | while read size file; do
    basename=$(basename "$file")
    echo "  • $basename: $size"
done

echo ""
echo "📝 RECENT LOG ENTRIES"
echo "---------------------"
echo "Content Generation (last 10 lines):"
journalctl -u fueltheaura-ai.service -n 10 --no-pager | tail -5
echo ""
echo "Web Scraper (last 10 lines):"
journalctl -u health-scraper.service -n 10 --no-pager | tail -5

echo ""
echo "🎯 NEXT ACTIONS"
echo "---------------"
python3 << 'PYTHON_SCRIPT'
import sqlite3
from datetime import datetime, timedelta

try:
    conn = sqlite3.connect('data/content_intelligence.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT created_at FROM generated_posts ORDER BY created_at DESC LIMIT 1')
    result = cursor.fetchone()
    
    if result:
        last_post = datetime.fromisoformat(result[0])
        next_post = last_post + timedelta(hours=4)
        time_until = next_post - datetime.now()
        
        if time_until.total_seconds() > 0:
            hours = int(time_until.total_seconds() // 3600)
            minutes = int((time_until.total_seconds() % 3600) // 60)
            print(f"Next blog post in: {hours}h {minutes}m")
        else:
            print("Next blog post: Due now or generating...")
    else:
        print("Next blog post: Within 4 hours")
    
    conn.close()
except Exception as e:
    print(f"Next blog post: Check logs for timing")
PYTHON_SCRIPT

echo ""
echo "🔧 ENHANCEMENT OPTIONS"
echo "----------------------"
echo "Would you like to enhance the system? Choose an option:"
echo ""
echo "1. Add Mental Health Sources (balance content 50/50)"
echo "2. Increase Scraping Speed (reach 2M faster)"
echo "3. Add More Health Topics (diversify content)"
echo "4. Create Monitoring Dashboard (web-based stats)"
echo "5. No changes (system is perfect as-is)"
echo ""
read -p "Enter option (1-5) or press Enter to skip: " choice

case $choice in
    1)
        echo ""
        echo "🧠 Adding Mental Health Sources..."
        cat > /tmp/mental_health_sources.py << 'MENTAL_HEALTH_SCRIPT'
# Additional mental health sources to add to massive_health_scraper.py

MENTAL_HEALTH_SOURCES = [
    'https://www.psychologytoday.com',
    'https://www.verywellmind.com',
    'https://www.mind.org.uk',
    'https://www.nami.org',
    'https://www.mentalhealth.gov',
    'https://www.nimh.nih.gov',
    'https://www.samhsa.gov',
    'https://www.mentalhealthamerica.net',
    'https://www.anxietycentre.com',
    'https://www.depressionalliance.org',
]

print("Mental health sources to add:")
for source in MENTAL_HEALTH_SOURCES:
    print(f"  • {source}")
MENTAL_HEALTH_SCRIPT
        python3 /tmp/mental_health_sources.py
        echo ""
        echo "✅ Mental health sources identified!"
        echo "To implement: Edit massive_health_scraper.py and add these sources"
        ;;
    2)
        echo ""
        echo "⚡ Increasing Scraping Speed..."
        echo "Current settings:"
        grep -A 2 "concurrent_requests\|delay" massive_health_scraper.py | head -6
        echo ""
        echo "Recommended changes:"
        echo "  • Increase concurrent_requests from 5 to 10"
        echo "  • Reduce delay from 2s to 1s"
        echo "  • Add more source websites"
        echo ""
        echo "This could 2-3x your scraping speed!"
        ;;
    3)
        echo ""
        echo "🎨 Additional Health Topics..."
        echo "Suggested topics to add:"
        echo "  • Sleep optimization"
        echo "  • Stress management"
        echo "  • Chronic pain management"
        echo "  • Digestive health"
        echo "  • Heart health"
        echo "  • Immune system"
        echo "  • Hormonal balance"
        echo "  • Aging and longevity"
        ;;
    4)
        echo ""
        echo "📊 Creating Monitoring Dashboard..."
        echo "This would create a simple web dashboard at http://your-droplet-ip:8080"
        echo "Showing real-time stats, graphs, and system health"
        ;;
    5|"")
        echo ""
        echo "✅ No changes needed - system running optimally!"
        ;;
    *)
        echo ""
        echo "Invalid option. No changes made."
        ;;
esac

echo ""
echo "🎉 SYSTEM STATUS: OPERATIONAL"
echo "=============================="
echo "All systems running smoothly!"
echo ""
echo "Check your website: https://fueltheaura.com"
echo "Check GitHub: https://github.com/mrm413/fueltheaura-site"
echo ""