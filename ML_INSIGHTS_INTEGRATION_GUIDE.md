# ML Insights Integration Guide

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
