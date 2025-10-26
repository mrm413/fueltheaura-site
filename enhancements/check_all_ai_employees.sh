#!/bin/bash

# Complete AI Employee System Status Check
# Checks all AI employees: Content Generator, Auditor, Supervisor, Analyst, and Reporter

echo "🔍 FuelTheAura AI Employee System Status Check"
echo "=============================================="
echo ""

cd /opt/fueltheaura-ai

echo "📊 CHECKING SYSTEMD SERVICES"
echo "----------------------------"

# Check each service
services=(
    "fueltheaura-ai.service:Content Generator"
    "health-scraper.service:Web Scraper"
    "ai-learning.service:AI Learning System"
    "auditor-ai.service:Auditor AI"
    "supervisor-ai.service:Supervisor AI"
    "analyst-ai.service:Analyst AI"
    "reporter-ai.service:Reporter AI"
)

for service_info in "${services[@]}"; do
    IFS=':' read -r service_name display_name <<< "$service_info"
    
    if systemctl list-unit-files | grep -q "$service_name"; then
        if systemctl is-active --quiet "$service_name"; then
            echo "✅ $display_name ($service_name): RUNNING"
        else
            echo "❌ $display_name ($service_name): STOPPED"
        fi
    else
        echo "⚠️  $display_name ($service_name): NOT INSTALLED"
    fi
done

echo ""
echo "📁 CHECKING AI EMPLOYEE FILES"
echo "-----------------------------"

# Check for AI employee Python files
ai_files=(
    "premium_ai_system.py:Content Generator"
    "massive_health_scraper.py:Web Scraper"
    "ai_learning_system.py:AI Learning"
    "auditor_ai.py:Auditor AI"
    "supervisor_ai.py:Supervisor AI"
    "analyst_ai.py:Analyst AI"
    "reporter_ai.py:Reporter AI"
    "orchestrator.py:Orchestrator"
)

for file_info in "${ai_files[@]}"; do
    IFS=':' read -r filename display_name <<< "$file_info"
    
    if [ -f "$filename" ]; then
        size=$(ls -lh "$filename" | awk '{print $5}')
        echo "✅ $display_name ($filename): EXISTS ($size)"
    else
        echo "❌ $display_name ($filename): NOT FOUND"
    fi
done

echo ""
echo "📂 CHECKING DATA DIRECTORIES"
echo "----------------------------"

# Check data directories
if [ -d "data" ]; then
    echo "✅ Data directory exists"
    
    # Check databases
    if [ -f "data/content_intelligence.db" ]; then
        size=$(ls -lh data/content_intelligence.db | awk '{print $5}')
        echo "  ✅ Content Intelligence DB: $size"
    fi
    
    if [ -f "data/health_content.db" ]; then
        size=$(ls -lh data/health_content.db | awk '{print $5}')
        count=$(sqlite3 data/health_content.db "SELECT COUNT(*) FROM health_articles;" 2>/dev/null || echo "N/A")
        echo "  ✅ Health Content DB: $size ($count articles)"
    fi
    
    if [ -f "data/ai_learning.db" ]; then
        size=$(ls -lh data/ai_learning.db | awk '{print $5}')
        echo "  ✅ AI Learning DB: $size"
    fi
    
    # Check for audit logs
    if [ -d "data/audits" ]; then
        audit_count=$(ls -1 data/audits/*.json 2>/dev/null | wc -l)
        echo "  ✅ Audit logs: $audit_count files"
    else
        echo "  ⚠️  Audit logs directory: NOT FOUND"
    fi
    
    # Check for reports
    if [ -d "data/reports" ]; then
        report_count=$(ls -1 data/reports/*.json 2>/dev/null | wc -l)
        echo "  ✅ Reports: $report_count files"
    else
        echo "  ⚠️  Reports directory: NOT FOUND"
    fi
else
    echo "❌ Data directory not found"
fi

echo ""
echo "🔄 CHECKING RECENT ACTIVITY"
echo "--------------------------"

# Check recent blog posts
if [ -d "data" ]; then
    echo "Recent Content Generation:"
    sqlite3 data/content_intelligence.db "SELECT title, created_at FROM generated_posts ORDER BY created_at DESC LIMIT 3;" 2>/dev/null || echo "  ⚠️  No data available"
fi

echo ""
echo "📋 CHECKING LOG FILES"
echo "--------------------"

# Check systemd logs for each service
echo "Recent Content Generator activity:"
journalctl -u fueltheaura-ai.service --since "1 hour ago" --no-pager | tail -3 2>/dev/null || echo "  No logs found"

echo ""
echo "Recent Auditor activity:"
journalctl -u auditor-ai.service --since "1 hour ago" --no-pager | tail -3 2>/dev/null || echo "  No logs found"

echo ""
echo "Recent Supervisor activity:"
journalctl -u supervisor-ai.service --since "1 hour ago" --no-pager | tail -3 2>/dev/null || echo "  No logs found"

echo ""
echo "📊 SUMMARY"
echo "---------"

# Count what's working
working=0
total=7

for service_info in "${services[@]}"; do
    IFS=':' read -r service_name display_name <<< "$service_info"
    if systemctl is-active --quiet "$service_name" 2>/dev/null; then
        ((working++))
    fi
done

echo "Active Services: $working / $total"

if [ $working -eq $total ]; then
    echo "✅ ALL SYSTEMS OPERATIONAL"
elif [ $working -gt 0 ]; then
    echo "⚠️  PARTIAL SYSTEM OPERATIONAL"
    echo ""
    echo "🔧 MISSING SERVICES:"
    for service_info in "${services[@]}"; do
        IFS=':' read -r service_name display_name <<< "$service_info"
        if ! systemctl is-active --quiet "$service_name" 2>/dev/null; then
            echo "  ❌ $display_name"
        fi
    done
else
    echo "❌ NO SERVICES RUNNING"
fi

echo ""
echo "💡 NEXT STEPS"
echo "------------"
echo "If services are missing, they may need to be installed."
echo "Run this to see what needs to be set up:"
echo "  ls -la *.py"
echo ""
echo "To check individual service status:"
echo "  systemctl status [service-name]"
echo ""
echo "To view detailed logs:"
echo "  journalctl -u [service-name] -n 50"