#!/usr/bin/env python3
"""
ML Insights Integration Script
Automatically integrates ML insights into website content
"""

import os
import sys
import sqlite3
import json
from datetime import datetime
from pathlib import Path

class MLInsightsIntegration:
    def __init__(self):
        self.base_dir = "/opt/fueltheaura-ai"
        self.data_dir = f"{self.base_dir}/data"
        self.ml_db_path = f"{self.data_dir}/ml_predictions.db"
        self.supervisor_db_path = f"{self.data_dir}/supervisor_improvements.db"
        self.website_dir = "/workspace/fueltheaura-site"
        self.insights_file = f"{self.website_dir}/src/_data/mlInsights.json"
        
    def get_active_insights(self):
        """Get active ML insights from database"""
        try:
            conn = sqlite3.connect(self.ml_db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    insight_type,
                    insight_category,
                    description,
                    confidence,
                    recommended_action,
                    priority,
                    timestamp
                FROM ml_insights
                WHERE status='active'
                ORDER BY 
                    CASE priority 
                        WHEN 'high' THEN 1 
                        WHEN 'medium' THEN 2 
                        ELSE 3 
                    END,
                    confidence DESC
            """)
            
            insights = []
            for row in cursor.fetchall():
                insights.append({
                    'type': row[0],
                    'category': row[1],
                    'description': row[2],
                    'confidence': row[3],
                    'action': row[4],
                    'priority': row[5],
                    'timestamp': row[6]
                })
            
            conn.close()
            return insights
            
        except Exception as e:
            print(f"❌ Error getting insights: {e}")
            return []
    
    def get_recent_predictions(self, limit=10):
        """Get recent predictions from database"""
        try:
            conn = sqlite3.connect(self.ml_db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    prediction_type,
                    prediction_date,
                    predicted_value,
                    confidence_score
                FROM predictions
                ORDER BY prediction_date DESC
                LIMIT ?
            """, (limit,))
            
            predictions = []
            for row in cursor.fetchall():
                predictions.append({
                    'type': row[0],
                    'date': row[1],
                    'value': row[2],
                    'confidence': row[3]
                })
            
            conn.close()
            return predictions
            
        except Exception as e:
            print(f"❌ Error getting predictions: {e}")
            return []
    
    def get_ml_stats(self):
        """Get ML system statistics"""
        try:
            stats = {}
            
            # Get predictions count
            conn = sqlite3.connect(self.ml_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM predictions")
            stats['totalPredictions'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ml_insights WHERE status='active'")
            stats['activeInsights'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT model_name) FROM model_performance")
            stats['modelsTrained'] = cursor.fetchone()[0]
            conn.close()
            
            # Get average impact
            conn = sqlite3.connect(self.supervisor_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT AVG(impact_score) FROM improvements")
            result = cursor.fetchone()[0]
            stats['avgImpact'] = round(result, 2) if result else 0
            conn.close()
            
            return stats
            
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return {}
    
    def export_insights_to_json(self):
        """Export insights to JSON file for website use"""
        try:
            # Ensure _data directory exists
            data_dir = f"{self.website_dir}/src/_data"
            os.makedirs(data_dir, exist_ok=True)
            
            # Get all data
            insights = self.get_active_insights()
            predictions = self.get_recent_predictions(20)
            stats = self.get_ml_stats()
            
            # Create data structure
            data = {
                'lastUpdated': datetime.now().isoformat(),
                'stats': stats,
                'insights': insights,
                'predictions': predictions
            }
            
            # Write to JSON file
            with open(self.insights_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Exported ML insights to {self.insights_file}")
            print(f"   - {len(insights)} active insights")
            print(f"   - {len(predictions)} recent predictions")
            print(f"   - Stats: {stats}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error exporting insights: {e}")
            return False
    
    def create_insights_widget(self):
        """Create an insights widget for homepage"""
        try:
            widget_file = f"{self.website_dir}/src/_includes/ml-insights-widget.njk"
            
            widget_html = """<!-- ML Insights Widget -->
<div class="ml-insights-widget">
    <div class="widget-header">
        <h3>🤖 AI-Powered Insights</h3>
        <a href="/ml-dashboard/" class="view-all-link">View Dashboard →</a>
    </div>
    
    <div class="widget-content">
        {% if mlInsights.insights.length > 0 %}
            {% for insight in mlInsights.insights | slice(0, 3) %}
            <div class="insight-item priority-{{ insight.priority }}">
                <div class="insight-icon">
                    {% if insight.priority == 'high' %}🔴{% elif insight.priority == 'medium' %}🟡{% else %}🔵{% endif %}
                </div>
                <div class="insight-text">
                    <strong>{{ insight.type }}:</strong> {{ insight.description }}
                </div>
                <div class="insight-confidence">
                    {{ (insight.confidence * 100) | round }}% confidence
                </div>
            </div>
            {% endfor %}
        {% else %}
            <p class="no-insights">ML system is learning... Check back soon for insights!</p>
        {% endif %}
    </div>
    
    <div class="widget-stats">
        <div class="stat-item">
            <span class="stat-value">{{ mlInsights.stats.totalPredictions }}</span>
            <span class="stat-label">Predictions</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{{ mlInsights.stats.activeInsights }}</span>
            <span class="stat-label">Active Insights</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{{ mlInsights.stats.avgImpact }}</span>
            <span class="stat-label">Avg Impact</span>
        </div>
    </div>
</div>

<style>
    .ml-insights-widget {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 2rem;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .widget-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .widget-header h3 {
        margin: 0;
        font-size: 1.5rem;
        color: white;
    }
    
    .view-all-link {
        color: white;
        text-decoration: none;
        font-weight: 600;
        transition: opacity 0.3s ease;
    }
    
    .view-all-link:hover {
        opacity: 0.8;
    }
    
    .widget-content {
        margin-bottom: 1.5rem;
    }
    
    .insight-item {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .insight-icon {
        font-size: 1.5rem;
    }
    
    .insight-text {
        flex: 1;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .insight-confidence {
        font-size: 0.85rem;
        opacity: 0.9;
        white-space: nowrap;
    }
    
    .no-insights {
        text-align: center;
        padding: 2rem;
        opacity: 0.8;
    }
    
    .widget-stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        display: block;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        display: block;
        font-size: 0.85rem;
        opacity: 0.9;
    }
    
    @media (max-width: 768px) {
        .ml-insights-widget {
            padding: 1.5rem;
        }
        
        .insight-item {
            flex-direction: column;
            text-align: center;
        }
        
        .widget-stats {
            grid-template-columns: 1fr;
        }
    }
</style>
"""
            
            with open(widget_file, 'w') as f:
                f.write(widget_html)
            
            print(f"✅ Created ML insights widget at {widget_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating widget: {e}")
            return False
    
    def create_integration_documentation(self):
        """Create documentation for ML insights integration"""
        try:
            doc_file = f"{self.website_dir}/ML_INSIGHTS_INTEGRATION_GUIDE.md"
            
            documentation = """# ML Insights Integration Guide

## Overview

This guide explains how ML insights are integrated into the FuelTheAura website.

## Architecture

### Data Flow
1. **ML Analytics System** generates predictions and insights
2. **Integration Script** exports data to JSON file
3. **Eleventy** reads JSON data during build
4. **Website Pages** display insights using Nunjucks templates

## Files Created

### 1. `ml_insights_integration.py`
Main integration script that:
- Reads ML insights from database
- Exports data to JSON format
- Creates reusable widgets
- Updates website content

### 2. `src/_data/mlInsights.json`
Data file containing:
- Active insights
- Recent predictions
- System statistics
- Last update timestamp

### 3. `src/_includes/ml-insights-widget.njk`
Reusable widget component for displaying insights on any page.

## Usage

### Running the Integration Script

```bash
# Run manually
python3 ml_insights_integration.py

# Run with cron (every hour)
0 * * * * cd /workspace/fueltheaura-site && python3 ml_insights_integration.py
```

### Adding Widget to Pages

Add this line to any Nunjucks template:

```njk
{% include "ml-insights-widget.njk" %}
```

Example locations:
- Homepage (`src/index.njk`)
- Blog index (`src/blog/index.njk`)
- About page (`src/about.njk`)

### Accessing Data in Templates

The ML insights data is available as `mlInsights` in all templates:

```njk
<!-- Display total predictions -->
{{ mlInsights.stats.totalPredictions }}

<!-- Loop through insights -->
{% for insight in mlInsights.insights %}
    <div>{{ insight.description }}</div>
{% endfor %}

<!-- Show recent predictions -->
{% for prediction in mlInsights.predictions %}
    <div>{{ prediction.date }}: {{ prediction.value }}</div>
{% endfor %}
```

## Data Structure

### mlInsights.json Format

```json
{
  "lastUpdated": "2025-10-27T19:30:00",
  "stats": {
    "totalPredictions": 56,
    "activeInsights": 4,
    "modelsTrained": 1,
    "avgImpact": 0.72
  },
  "insights": [
    {
      "type": "Improvement Pattern",
      "category": "optimization",
      "description": "UX improvements have highest impact",
      "confidence": 0.85,
      "action": "Prioritize UX improvements",
      "priority": "high",
      "timestamp": "2025-10-27T19:17:19"
    }
  ],
  "predictions": [
    {
      "type": "improvement_opportunities",
      "date": "2025-10-28",
      "value": 0.701,
      "confidence": 0.75
    }
  ]
}
```

## Automation

### Cron Job Setup

Add to crontab to update insights hourly:

```bash
# Edit crontab
crontab -e

# Add this line
0 * * * * cd /workspace/fueltheaura-site && python3 ml_insights_integration.py && cd /workspace/fueltheaura-site && npm run build
```

### Systemd Timer (Alternative)

Create `/etc/systemd/system/ml-insights-integration.timer`:

```ini
[Unit]
Description=ML Insights Integration Timer

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

Create `/etc/systemd/system/ml-insights-integration.service`:

```ini
[Unit]
Description=ML Insights Integration Service

[Service]
Type=oneshot
WorkingDirectory=/workspace/fueltheaura-site
ExecStart=/usr/bin/python3 ml_insights_integration.py
ExecStartPost=/usr/bin/npm run build
```

Enable and start:

```bash
sudo systemctl enable ml-insights-integration.timer
sudo systemctl start ml-insights-integration.timer
```

## Customization

### Styling the Widget

Edit the CSS in `src/_includes/ml-insights-widget.njk` to match your design.

### Filtering Insights

Show only high-priority insights:

```njk
{% for insight in mlInsights.insights %}
    {% if insight.priority == 'high' %}
        <!-- Display insight -->
    {% endif %}
{% endfor %}
```

### Custom Layouts

Create custom insight displays:

```njk
<div class="custom-insights">
    {% for insight in mlInsights.insights | slice(0, 5) %}
        <article class="insight-card">
            <h4>{{ insight.type }}</h4>
            <p>{{ insight.description }}</p>
            <button>{{ insight.action }}</button>
        </article>
    {% endfor %}
</div>
```

## Troubleshooting

### No Data Showing

1. Check if JSON file exists:
   ```bash
   cat src/_data/mlInsights.json
   ```

2. Run integration script manually:
   ```bash
   python3 ml_insights_integration.py
   ```

3. Rebuild website:
   ```bash
   npm run build
   ```

### Outdated Data

1. Check last update timestamp in JSON
2. Verify cron job is running
3. Check ML analytics system is generating insights

### Widget Not Displaying

1. Verify include path is correct
2. Check template syntax
3. Ensure mlInsights data is available
4. Check browser console for errors

## Best Practices

1. **Update Frequency**: Update insights hourly or when ML system runs
2. **Cache Busting**: Rebuild website after updating insights
3. **Error Handling**: Widget should gracefully handle missing data
4. **Performance**: Limit number of insights displayed
5. **Mobile**: Ensure widget is responsive

## Support

For issues or questions:
- Check ML Analytics logs
- Review integration script output
- Consult ML_ANALYTICS_GUIDE.md
- Check Eleventy build logs

---

**Last Updated:** October 27, 2025
"""
            
            with open(doc_file, 'w') as f:
                f.write(documentation)
            
            print(f"✅ Created integration documentation at {doc_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating documentation: {e}")
            return False
    
    def run(self):
        """Run the integration process"""
        print("\n" + "=" * 70)
        print("🔗 ML Insights Integration")
        print("=" * 70)
        
        # Export insights to JSON
        print("\n📊 Exporting ML insights...")
        self.export_insights_to_json()
        
        # Create widget
        print("\n🎨 Creating insights widget...")
        self.create_insights_widget()
        
        # Create documentation
        print("\n📝 Creating integration documentation...")
        self.create_integration_documentation()
        
        print("\n" + "=" * 70)
        print("✅ Integration complete!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Add widget to homepage: {% include 'ml-insights-widget.njk' %}")
        print("2. Rebuild website: npm run build")
        print("3. Set up cron job for automatic updates")
        print("\nSee ML_INSIGHTS_INTEGRATION_GUIDE.md for details")

def main():
    """Main entry point"""
    integration = MLInsightsIntegration()
    integration.run()

if __name__ == "__main__":
    main()