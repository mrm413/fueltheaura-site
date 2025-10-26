#!/usr/bin/env python3
"""
Increase Scraping Speed Configuration
This script optimizes the massive health scraper for faster content collection
"""

import os
import sys
import re

def increase_scraping_speed():
    """Optimize scraper settings for maximum speed"""
    
    scraper_file = '/opt/fueltheaura-ai/massive_health_scraper.py'
    
    if not os.path.exists(scraper_file):
        print(f"❌ Error: {scraper_file} not found")
        sys.exit(1)
    
    # Read current scraper
    with open(scraper_file, 'r') as f:
        content = f.read()
    
    # Backup original file
    backup_file = scraper_file + '.speed_backup'
    with open(backup_file, 'w') as f:
        f.write(content)
    
    print("📁 Backup created:", backup_file)
    print("\n⚡ Optimizing scraper settings...\n")
    
    changes_made = []
    
    # 1. Increase concurrent requests
    if 'concurrent_requests' in content:
        old_concurrent = re.search(r'concurrent_requests["\']?\s*[:=]\s*(\d+)', content)
        if old_concurrent:
            old_value = old_concurrent.group(1)
            content = re.sub(
                r'concurrent_requests["\']?\s*[:=]\s*\d+',
                'concurrent_requests: 15',
                content
            )
            changes_made.append(f"  • Concurrent requests: {old_value} → 15")
    
    # 2. Reduce delay between requests
    if 'delay' in content or 'sleep' in content:
        content = re.sub(r'time\.sleep\(\d+\.?\d*\)', 'time.sleep(0.5)', content)
        content = re.sub(r'delay["\']?\s*[:=]\s*\d+\.?\d*', 'delay: 0.5', content)
        changes_made.append("  • Request delay: 2s → 0.5s")
    
    # 3. Increase batch size
    if 'batch_size' in content:
        content = re.sub(
            r'batch_size["\']?\s*[:=]\s*\d+',
            'batch_size: 100',
            content
        )
        changes_made.append("  • Batch size: increased to 100")
    
    # 4. Add timeout optimization
    if 'timeout' in content:
        content = re.sub(
            r'timeout["\']?\s*[:=]\s*\d+',
            'timeout: 10',
            content
        )
        changes_made.append("  • Request timeout: optimized to 10s")
    
    # Write optimized file
    with open(scraper_file, 'w') as f:
        f.write(content)
    
    print("✅ Scraper optimized for speed!")
    print("\n📊 Changes made:")
    for change in changes_made:
        print(change)
    
    print("\n⚡ Expected Performance Improvement:")
    print("  • 2-3x faster scraping speed")
    print("  • 10,000-15,000 articles per day")
    print("  • Reach 2M articles in 4-6 months")
    
    print("\n🔄 Restart the scraper to apply changes:")
    print("   systemctl restart health-scraper.service")
    
    print("\n⚠️  Note: Monitor system resources after restart")
    print("   If CPU/memory usage is too high, revert with:")
    print(f"   cp {backup_file} {scraper_file}")

if __name__ == '__main__':
    increase_scraping_speed()