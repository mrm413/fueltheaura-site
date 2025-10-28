#!/usr/bin/env python3
"""
Script to populate supervisor_improvements.db with sample data
This will allow the ML system to begin training and generating predictions
"""

import sqlite3
import random
from datetime import datetime, timedelta

# Configuration
DB_PATH = "/opt/fueltheaura-ai/data/supervisor_improvements.db"

def create_tables(conn):
    """Create the required tables if they don't exist"""
    cursor = conn.cursor()
    
    # Improvements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS improvements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            category TEXT,
            improvement_type TEXT,
            description TEXT,
            before_value TEXT,
            after_value TEXT,
            impact_score REAL,
            status TEXT
        )
    ''')
    
    # SEO metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seo_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            page_url TEXT,
            title_length INTEGER,
            meta_description_length INTEGER,
            h1_count INTEGER,
            image_alt_count INTEGER,
            internal_links INTEGER,
            external_links INTEGER,
            word_count INTEGER,
            keyword_density REAL,
            page_speed_score REAL,
            mobile_friendly INTEGER
        )
    ''')
    
    # Performance metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            metric_name TEXT,
            metric_value REAL,
            target_value REAL,
            status TEXT
        )
    ''')
    
    conn.commit()

def generate_sample_improvements(conn, num_records=100):
    """Generate sample improvement records"""
    cursor = conn.cursor()
    
    categories = ['SEO', 'Performance', 'Design', 'Content', 'UX']
    improvement_types = [
        'Meta Description Update',
        'Title Optimization',
        'Image Optimization',
        'Code Minification',
        'Cache Implementation',
        'Mobile Responsiveness',
        'Accessibility Enhancement',
        'Content Quality Improvement',
        'Internal Linking',
        'Page Speed Optimization'
    ]
    statuses = ['completed', 'in_progress', 'planned']
    
    # Generate records over the past 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    for i in range(num_records):
        # Random timestamp within the date range
        random_days = random.randint(0, 90)
        timestamp = (start_date + timedelta(days=random_days)).isoformat()
        
        category = random.choice(categories)
        improvement_type = random.choice(improvement_types)
        description = f"Implemented {improvement_type} for {category}"
        
        # Generate realistic before/after values
        if 'Speed' in improvement_type or 'Performance' in category:
            before_value = f"{random.randint(40, 70)}/100"
            after_value = f"{random.randint(75, 95)}/100"
        elif 'SEO' in category:
            before_value = f"{random.randint(50, 70)} score"
            after_value = f"{random.randint(75, 95)} score"
        else:
            before_value = "Not optimized"
            after_value = "Optimized"
        
        # Impact score between 0.3 and 1.0
        impact_score = round(random.uniform(0.3, 1.0), 2)
        
        status = random.choice(statuses)
        
        cursor.execute('''
            INSERT INTO improvements 
            (timestamp, category, improvement_type, description, before_value, after_value, impact_score, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, category, improvement_type, description, before_value, after_value, impact_score, status))
    
    conn.commit()
    print(f"✅ Generated {num_records} sample improvement records")

def generate_sample_seo_metrics(conn, num_records=100):
    """Generate sample SEO metrics records"""
    cursor = conn.cursor()
    
    pages = [
        '/blog/cognitive-behavioral-techniques',
        '/blog/exercise-routines-for-busy-professionals',
        '/blog/immune-system-strengthening',
        '/blog/ptsd-healing-strategies',
        '/blog/sleep-optimization',
        '/blog/stress-reduction-breathing',
        '/blog/understanding-depression',
        '/about',
        '/store',
        '/'
    ]
    
    # Generate records over the past 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    for i in range(num_records):
        # Random timestamp within the date range
        random_days = random.randint(0, 90)
        timestamp = (start_date + timedelta(days=random_days)).isoformat()
        
        page_url = random.choice(pages)
        title_length = random.randint(40, 70)
        meta_description_length = random.randint(120, 160)
        h1_count = random.randint(1, 3)
        image_alt_count = random.randint(3, 10)
        internal_links = random.randint(5, 20)
        external_links = random.randint(2, 8)
        word_count = random.randint(1500, 3000)
        keyword_density = round(random.uniform(1.0, 3.5), 2)
        page_speed_score = round(random.uniform(70, 95), 1)
        mobile_friendly = 1
        
        cursor.execute('''
            INSERT INTO seo_metrics 
            (timestamp, page_url, title_length, meta_description_length, h1_count, 
             image_alt_count, internal_links, external_links, word_count, 
             keyword_density, page_speed_score, mobile_friendly)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, page_url, title_length, meta_description_length, h1_count,
              image_alt_count, internal_links, external_links, word_count,
              keyword_density, page_speed_score, mobile_friendly))
    
    conn.commit()
    print(f"✅ Generated {num_records} sample SEO metrics records")

def generate_sample_performance_metrics(conn, num_records=100):
    """Generate sample performance metrics records"""
    cursor = conn.cursor()
    
    metrics = [
        ('Page Load Time', 's', 2.0),
        ('Time to First Byte', 'ms', 200),
        ('First Contentful Paint', 's', 1.5),
        ('Largest Contentful Paint', 's', 2.5),
        ('Cumulative Layout Shift', 'score', 0.1),
        ('Total Blocking Time', 'ms', 300),
        ('Server Response Time', 'ms', 150)
    ]
    
    statuses = ['good', 'needs_improvement', 'poor']
    
    # Generate records over the past 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    for i in range(num_records):
        # Random timestamp within the date range
        random_days = random.randint(0, 90)
        timestamp = (start_date + timedelta(days=random_days)).isoformat()
        
        metric_name, unit, target = random.choice(metrics)
        
        # Generate metric value around the target
        if unit == 's':
            metric_value = round(random.uniform(target * 0.8, target * 1.5), 2)
        elif unit == 'ms':
            metric_value = round(random.uniform(target * 0.7, target * 1.8), 1)
        else:  # score
            metric_value = round(random.uniform(target * 0.5, target * 2.0), 3)
        
        # Determine status based on how close to target
        if metric_value <= target:
            status = 'good'
        elif metric_value <= target * 1.3:
            status = 'needs_improvement'
        else:
            status = 'poor'
        
        cursor.execute('''
            INSERT INTO performance_metrics 
            (timestamp, metric_name, metric_value, target_value, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, metric_name, metric_value, target, status))
    
    conn.commit()
    print(f"✅ Generated {num_records} sample performance metrics records")

def main():
    """Main function to populate the database"""
    print("🚀 Populating supervisor_improvements.db with sample data...")
    print("=" * 60)
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        
        # Create tables
        print("📋 Creating tables...")
        create_tables(conn)
        
        # Check if data already exists
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM improvements")
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            print(f"⚠️  Database already contains {existing_count} improvement records")
            response = input("Do you want to add more sample data? (y/n): ")
            if response.lower() != 'y':
                print("❌ Cancelled")
                conn.close()
                return
        
        # Generate sample data
        print("\n📊 Generating sample data...")
        generate_sample_improvements(conn, num_records=100)
        generate_sample_seo_metrics(conn, num_records=100)
        generate_sample_performance_metrics(conn, num_records=100)
        
        # Verify data was inserted
        cursor.execute("SELECT COUNT(*) FROM improvements")
        improvements_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM seo_metrics")
        seo_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM performance_metrics")
        performance_count = cursor.fetchone()[0]
        
        print("\n" + "=" * 60)
        print("✅ Sample data population complete!")
        print("=" * 60)
        print(f"📊 Total Records:")
        print(f"   - Improvements: {improvements_count}")
        print(f"   - SEO Metrics: {seo_count}")
        print(f"   - Performance Metrics: {performance_count}")
        print("\n🎯 The ML system should now have enough data to begin training!")
        print("   Run the ML analytics script to start generating predictions.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())