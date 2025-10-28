#!/usr/bin/env python3
"""
Script to populate content_intelligence.db with sample data
This will allow the content quality predictor model to train
"""

import sqlite3
import random
from datetime import datetime, timedelta

# Configuration
DB_PATH = "/opt/fueltheaura-ai/data/content_intelligence.db"

def create_tables(conn):
    """Create the required tables if they don't exist"""
    cursor = conn.cursor()
    
    # Blog posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blog_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            title TEXT,
            quality_score REAL,
            word_count INTEGER,
            engagement_score REAL
        )
    ''')
    
    conn.commit()

def generate_sample_blog_posts(conn, num_records=50):
    """Generate sample blog post records"""
    cursor = conn.cursor()
    
    titles = [
        'Cognitive Behavioral Techniques for Daily Life',
        'Exercise Routines for Busy Professionals',
        'Immune System Strengthening Techniques',
        'PTSD Healing Strategies for Veterans',
        'Sleep Optimization Transform Your Rest Quality',
        'Stress Reduction Through Breathing Exercises',
        'Understanding Depression and Self-Help Methods',
        'Mindfulness Meditation for Beginners',
        'Nutrition Tips for Mental Health',
        'Building Healthy Habits That Last',
        'Managing Anxiety in the Workplace',
        'The Science of Happiness',
        'Overcoming Procrastination',
        'Improving Focus and Concentration',
        'Work-Life Balance Strategies'
    ]
    
    # Generate records over the past 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    for i in range(num_records):
        # Random timestamp within the date range
        random_days = random.randint(0, 90)
        created_at = (start_date + timedelta(days=random_days)).isoformat()
        
        title = random.choice(titles)
        
        # Quality score between 0.5 and 1.0 (higher is better)
        quality_score = round(random.uniform(0.5, 1.0), 2)
        
        # Word count between 1500 and 3000
        word_count = random.randint(1500, 3000)
        
        # Engagement score between 0.3 and 1.0
        engagement_score = round(random.uniform(0.3, 1.0), 2)
        
        cursor.execute('''
            INSERT INTO blog_posts 
            (created_at, title, quality_score, word_count, engagement_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (created_at, title, quality_score, word_count, engagement_score))
    
    conn.commit()
    print(f"✅ Generated {num_records} sample blog post records")

def main():
    """Main function to populate the database"""
    print("🚀 Populating content_intelligence.db with sample data...")
    print("=" * 60)
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        
        # Create tables
        print("📋 Creating tables...")
        create_tables(conn)
        
        # Check if data already exists
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM blog_posts")
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            print(f"⚠️  Database already contains {existing_count} blog post records")
            response = input("Do you want to add more sample data? (y/n): ")
            if response.lower() != 'y':
                print("❌ Cancelled")
                conn.close()
                return
        
        # Generate sample data
        print("\n📊 Generating sample data...")
        generate_sample_blog_posts(conn, num_records=50)
        
        # Verify data was inserted
        cursor.execute("SELECT COUNT(*) FROM blog_posts")
        posts_count = cursor.fetchone()[0]
        
        print("\n" + "=" * 60)
        print("✅ Sample data population complete!")
        print("=" * 60)
        print(f"📊 Total Records:")
        print(f"   - Blog Posts: {posts_count}")
        print("\n🎯 The content quality predictor should now have enough data to train!")
        print("   Run the ML analytics script to start generating content predictions.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())