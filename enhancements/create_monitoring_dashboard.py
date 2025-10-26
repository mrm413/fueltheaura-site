#!/usr/bin/env python3
"""
FuelTheAura AI System Monitoring Dashboard
Creates a simple web-based dashboard to monitor system performance
"""

import os
from flask import Flask, render_template_string
import sqlite3
from datetime import datetime, timedelta
import json

# Create Flask app
app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FuelTheAura AI System Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        .stat-card h3 {
            color: #667eea;
            font-size: 1.2em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .stat-card .icon {
            font-size: 1.5em;
            margin-right: 10px;
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
            margin: 10px 0;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        .progress-bar {
            width: 100%;
            height: 10px;
            background: #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 10px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.5s ease;
        }
        .recent-posts {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .recent-posts h3 {
            color: #667eea;
            font-size: 1.5em;
            margin-bottom: 20px;
        }
        .post-item {
            padding: 15px;
            border-left: 4px solid #667eea;
            background: #f8f9fa;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        .post-title {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .post-meta {
            color: #666;
            font-size: 0.9em;
        }
        .category-breakdown {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .category-breakdown h3 {
            color: #667eea;
            font-size: 1.5em;
            margin-bottom: 20px;
        }
        .category-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .category-name {
            font-weight: 500;
            color: #333;
        }
        .category-count {
            color: #667eea;
            font-weight: bold;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-active {
            background: #4caf50;
            box-shadow: 0 0 10px #4caf50;
        }
        .refresh-info {
            text-align: center;
            color: white;
            margin-top: 20px;
            font-size: 0.9em;
        }
    </style>
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(function() {
            location.reload();
        }, 30000);
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 FuelTheAura AI System</h1>
            <p>Real-time monitoring dashboard for autonomous content generation</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <h3><span class="icon">📝</span> Blog Posts Generated</h3>
                <div class="stat-value">{{ stats.total_posts }}</div>
                <div class="stat-label">Total articles created</div>
                <div class="stat-label" style="margin-top: 10px;">
                    Next post in: {{ stats.next_post_time }}
                </div>
            </div>

            <div class="stat-card">
                <h3><span class="icon">🌐</span> Articles Scraped</h3>
                <div class="stat-value">{{ stats.total_scraped|format_number }}</div>
                <div class="stat-label">Health articles collected</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ stats.progress_percent }}%"></div>
                </div>
                <div class="stat-label" style="margin-top: 5px;">
                    {{ stats.progress_percent }}% to 2M goal
                </div>
            </div>

            <div class="stat-card">
                <h3><span class="icon">💾</span> Database Size</h3>
                <div class="stat-value">{{ stats.db_size }}</div>
                <div class="stat-label">Total storage used</div>
            </div>

            <div class="stat-card">
                <h3><span class="icon">⚡</span> System Status</h3>
                <div style="margin-top: 15px;">
                    <div style="margin-bottom: 10px;">
                        <span class="status-indicator status-active"></span>
                        <span>Content Generation</span>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="status-indicator status-active"></span>
                        <span>Web Scraper</span>
                    </div>
                    <div>
                        <span class="status-indicator status-active"></span>
                        <span>AI Learning</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="recent-posts">
            <h3>📰 Recent Blog Posts</h3>
            {% for post in recent_posts %}
            <div class="post-item">
                <div class="post-title">{{ post.title }}</div>
                <div class="post-meta">
                    Created: {{ post.created_at }} | Quality Score: {{ post.quality_score }}
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="category-breakdown">
            <h3>📊 Content Categories</h3>
            {% for category in categories %}
            <div class="category-item">
                <span class="category-name">{{ category.name }}</span>
                <span class="category-count">{{ category.count|format_number }} articles</span>
            </div>
            {% endfor %}
        </div>

        <div class="refresh-info">
            🔄 Dashboard auto-refreshes every 30 seconds | Last updated: {{ current_time }}
        </div>
    </div>
</body>
</html>
"""

def format_number(value):
    """Format number with commas"""
    return f"{value:,}"

app.jinja_env.filters['format_number'] = format_number

@app.route('/')
def dashboard():
    """Main dashboard route"""
    
    # Get content generation stats
    try:
        conn = sqlite3.connect('/opt/fueltheaura-ai/data/content_intelligence.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM generated_posts')
        total_posts = cursor.fetchone()[0]
        
        cursor.execute('SELECT title, created_at, quality_score FROM generated_posts ORDER BY created_at DESC LIMIT 5')
        recent_posts = [
            {
                'title': row[0],
                'created_at': row[1],
                'quality_score': f"{row[2]:.2f}"
            }
            for row in cursor.fetchall()
        ]
        
        # Calculate next post time
        cursor.execute('SELECT created_at FROM generated_posts ORDER BY created_at DESC LIMIT 1')
        result = cursor.fetchone()
        if result:
            last_post = datetime.fromisoformat(result[0])
            next_post = last_post + timedelta(hours=4)
            time_until = next_post - datetime.now()
            if time_until.total_seconds() > 0:
                hours = int(time_until.total_seconds() // 3600)
                minutes = int((time_until.total_seconds() % 3600) // 60)
                next_post_time = f"{hours}h {minutes}m"
            else:
                next_post_time = "Generating now..."
        else:
            next_post_time = "Within 4 hours"
        
        conn.close()
    except Exception as e:
        total_posts = 0
        recent_posts = []
        next_post_time = "Unknown"
    
    # Get scraping stats
    try:
        conn = sqlite3.connect('/opt/fueltheaura-ai/data/health_content.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM health_articles')
        total_scraped = cursor.fetchone()[0]
        
        cursor.execute('SELECT category, COUNT(*) as count FROM health_articles GROUP BY category ORDER BY count DESC')
        categories = [
            {
                'name': row[0].replace('_', ' ').title(),
                'count': row[1]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
    except Exception as e:
        total_scraped = 0
        categories = []
    
    # Calculate progress
    progress_percent = (total_scraped / 2000000) * 100
    
    # Get database size
    try:
        import subprocess
        result = subprocess.run(
            ['du', '-sh', '/opt/fueltheaura-ai/data/'],
            capture_output=True,
            text=True
        )
        db_size = result.stdout.split()[0]
    except:
        db_size = "Unknown"
    
    stats = {
        'total_posts': total_posts,
        'total_scraped': total_scraped,
        'progress_percent': f"{progress_percent:.2f}",
        'db_size': db_size,
        'next_post_time': next_post_time
    }
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template_string(
        DASHBOARD_HTML,
        stats=stats,
        recent_posts=recent_posts,
        categories=categories,
        current_time=current_time
    )

if __name__ == '__main__':
    print("🚀 Starting FuelTheAura AI Dashboard...")
    print("📊 Dashboard will be available at: http://your-droplet-ip:8080")
    print("🔄 Auto-refreshes every 30 seconds")
    print("\nPress Ctrl+C to stop")
    app.run(host='0.0.0.0', port=8080, debug=False)