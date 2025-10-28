# ML Analytics System - Quick Reference Guide

## 🚀 Quick Start

### Check System Status
```bash
# Check if ML process is running
ps aux | grep ml_predictive_analytics

# View recent ML activity
tail -f /workspace/outputs/workspace_output_*.txt
```

### View Predictions
```bash
# Connect to ML database
sqlite3 /opt/fueltheaura-ai/data/ml_predictions.db

# View recent predictions
SELECT prediction_type, prediction_date, predicted_value, confidence_score 
FROM predictions 
ORDER BY timestamp DESC 
LIMIT 20;

# Exit
.quit
```

### View Insights
```bash
# Connect to ML database
sqlite3 /opt/fueltheaura-ai/data/ml_predictions.db

# View active high-priority insights
SELECT description, recommended_action, confidence 
FROM ml_insights 
WHERE priority='high' AND status='active' 
ORDER BY confidence DESC;

# Exit
.quit
```

### View Model Performance
```bash
# Connect to ML database
sqlite3 /opt/fueltheaura-ai/data/ml_predictions.db

# Check model accuracy
SELECT model_name, accuracy, rmse, r2_score, training_samples 
FROM model_performance 
ORDER BY timestamp DESC;

# Exit
.quit
```

---

## 📊 Database Locations

- **ML Predictions:** `/opt/fueltheaura-ai/data/ml_predictions.db`
- **Supervisor Improvements:** `/opt/fueltheaura-ai/data/supervisor_improvements.db`
- **Content Intelligence:** `/opt/fueltheaura-ai/data/content_intelligence.db`
- **ML Reports:** `/opt/fueltheaura-ai/data/ml_reports/`

---

## 🔧 Maintenance Commands

### Add More Sample Data
```bash
# Add more improvements data
python /workspace/populate_sample_data.py

# Add more content data
python /workspace/populate_content_data.py
```

### Verify Data
```bash
# Check all databases
python /workspace/verify_data.py

# Check ML predictions
python /workspace/check_db.py
```

### View Latest Report
```bash
# View most recent ML report
cat /opt/fueltheaura-ai/data/ml_reports/$(ls -t /opt/fueltheaura-ai/data/ml_reports/ | head -1)
```

---

## 📈 Understanding the Output

### Model Metrics

**RMSE (Root Mean Squared Error)**
- Lower is better
- Measures prediction error
- Target: < 0.15 for good accuracy

**R² Score (R-squared)**
- Range: -∞ to 1.0
- 1.0 = perfect predictions
- 0.7+ = good model
- Negative = needs more data

**Confidence Score**
- Range: 0.0 to 1.0
- 0.85+ = high confidence
- 0.70-0.84 = medium confidence
- < 0.70 = low confidence

### Insight Priorities

**High Priority**
- Confidence: 0.85+
- Immediate action recommended
- High impact potential

**Medium Priority**
- Confidence: 0.70-0.84
- Action recommended soon
- Moderate impact potential

**Low Priority**
- Confidence: < 0.70
- Monitor and consider
- Lower impact potential

---

## 🎯 Common Tasks

### Task 1: Check if ML system needs more data
```bash
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db "SELECT COUNT(*) FROM improvements;"
sqlite3 /opt/fueltheaura-ai/data/content_intelligence.db "SELECT COUNT(*) FROM blog_posts;"
```

**Minimum Requirements:**
- Improvements: 50+ records
- Blog Posts: 30+ records
- SEO Metrics: 50+ records

### Task 2: View prediction accuracy over time
```bash
sqlite3 /opt/fueltheaura-ai/data/ml_predictions.db << EOF
SELECT 
    model_name,
    timestamp,
    accuracy,
    training_samples
FROM model_performance
ORDER BY timestamp;
.quit
EOF
```

### Task 3: Export insights to file
```bash
sqlite3 /opt/fueltheaura-ai/data/ml_predictions.db << EOF
.mode csv
.output ml_insights_export.csv
SELECT * FROM ml_insights WHERE status='active';
.quit
EOF
```

### Task 4: Count predictions by type
```bash
sqlite3 /opt/fueltheaura-ai/data/ml_predictions.db << EOF
SELECT 
    prediction_type,
    COUNT(*) as count
FROM predictions
GROUP BY prediction_type;
.quit
EOF
```

---

## 🔍 Troubleshooting

### Problem: No predictions being generated

**Check 1:** Verify ML process is running
```bash
ps aux | grep ml_predictive_analytics
```

**Check 2:** Verify sufficient data exists
```bash
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db "SELECT COUNT(*) FROM improvements;"
```

**Solution:** If count < 50, run:
```bash
python /workspace/populate_sample_data.py
```

### Problem: Low model accuracy

**Check:** View model performance
```bash
sqlite3 /opt/fueltheaura-ai/data/ml_predictions.db "SELECT * FROM model_performance ORDER BY timestamp DESC LIMIT 1;"
```

**Solution:** 
- Wait for more data to accumulate (90+ days recommended)
- Models improve automatically as data grows
- Check back after next ML run (24 hours)

### Problem: Content quality predictor not training

**Check:** Verify blog post data
```bash
sqlite3 /opt/fueltheaura-ai/data/content_intelligence.db "SELECT COUNT(*) FROM blog_posts;"
```

**Solution:** If count < 30, run:
```bash
python /workspace/populate_content_data.py
```

---

## 📅 ML System Schedule

- **Training Frequency:** Every 24 hours
- **Prediction Generation:** After each training
- **Insight Discovery:** After each training
- **Report Generation:** After each training

**Next Run:** Check output files for timestamp

---

## 💾 Backup Recommendations

### Important Files to Backup
```bash
# Backup all databases
cp /opt/fueltheaura-ai/data/*.db /backup/location/

# Backup ML reports
cp -r /opt/fueltheaura-ai/data/ml_reports/ /backup/location/

# Backup trained models
cp -r /opt/fueltheaura-ai/data/ml_models/ /backup/location/
```

---

## 📞 Quick Help

**View this guide:**
```bash
cat /workspace/ML_SYSTEM_QUICK_REFERENCE.md
```

**View full documentation:**
```bash
cat /workspace/fueltheaura-site/ML_ANALYTICS_GUIDE.md
```

**View data population summary:**
```bash
cat /workspace/ML_DATA_POPULATION_SUMMARY.md
```

---

**Last Updated:** October 27, 2025