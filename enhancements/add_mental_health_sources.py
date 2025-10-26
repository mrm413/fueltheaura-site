#!/usr/bin/env python3
"""
Add Mental Health Sources to Massive Health Scraper
This script enhances the scraper to balance physical and mental health content 50/50
"""

import os
import sys

def add_mental_health_sources():
    """Add comprehensive mental health sources to the scraper"""
    
    scraper_file = '/opt/fueltheaura-ai/massive_health_scraper.py'
    
    if not os.path.exists(scraper_file):
        print(f"❌ Error: {scraper_file} not found")
        sys.exit(1)
    
    # Read current scraper
    with open(scraper_file, 'r') as f:
        content = f.read()
    
    # Mental health sources to add
    mental_health_sources = """
    # Mental Health & Psychology Sources
    'https://www.psychologytoday.com': {
        'name': 'Psychology Today',
        'categories': ['mental_health', 'anxiety', 'depression', 'stress'],
        'selectors': {
            'article': 'article.node--type-blog-entry',
            'title': 'h1.page-title',
            'content': 'div.field--name-body'
        }
    },
    'https://www.verywellmind.com': {
        'name': 'Verywell Mind',
        'categories': ['mental_health', 'anxiety', 'depression', 'therapy'],
        'selectors': {
            'article': 'article',
            'title': 'h1',
            'content': 'div.article-body'
        }
    },
    'https://www.mind.org.uk': {
        'name': 'Mind UK',
        'categories': ['mental_health', 'wellbeing', 'support'],
        'selectors': {
            'article': 'article',
            'title': 'h1',
            'content': 'div.content'
        }
    },
    'https://www.nami.org': {
        'name': 'NAMI',
        'categories': ['mental_health', 'mental_illness', 'support'],
        'selectors': {
            'article': 'article',
            'title': 'h1',
            'content': 'div.field-name-body'
        }
    },
    'https://www.nimh.nih.gov': {
        'name': 'NIMH',
        'categories': ['mental_health', 'research', 'disorders'],
        'selectors': {
            'article': 'article',
            'title': 'h1',
            'content': 'div.content'
        }
    },
    'https://www.samhsa.gov': {
        'name': 'SAMHSA',
        'categories': ['mental_health', 'substance_abuse', 'treatment'],
        'selectors': {
            'article': 'article',
            'title': 'h1',
            'content': 'div.field-name-body'
        }
    },
    'https://www.mentalhealthamerica.net': {
        'name': 'Mental Health America',
        'categories': ['mental_health', 'advocacy', 'resources'],
        'selectors': {
            'article': 'article',
            'title': 'h1',
            'content': 'div.field-name-body'
        }
    },
    'https://www.anxietycentre.com': {
        'name': 'Anxiety Centre',
        'categories': ['anxiety', 'panic', 'stress'],
        'selectors': {
            'article': 'article',
            'title': 'h1',
            'content': 'div.entry-content'
        }
    },
    'https://www.headspace.com/blog': {
        'name': 'Headspace Blog',
        'categories': ['meditation', 'mindfulness', 'mental_health'],
        'selectors': {
            'article': 'article',
            'title': 'h1',
            'content': 'div.article-content'
        }
    },
    'https://www.calm.com/blog': {
        'name': 'Calm Blog',
        'categories': ['meditation', 'sleep', 'stress'],
        'selectors': {
            'article': 'article',
            'title': 'h1',
            'content': 'div.post-content'
        }
    },
"""
    
    # Find the HEALTH_SOURCES dictionary and add mental health sources
    if 'HEALTH_SOURCES = {' in content:
        # Find the end of the dictionary
        dict_start = content.find('HEALTH_SOURCES = {')
        dict_end = content.find('}', dict_start)
        
        # Insert mental health sources before the closing brace
        new_content = (
            content[:dict_end] + 
            mental_health_sources + 
            content[dict_end:]
        )
        
        # Backup original file
        backup_file = scraper_file + '.backup'
        with open(backup_file, 'w') as f:
            f.write(content)
        
        # Write updated file
        with open(scraper_file, 'w') as f:
            f.write(new_content)
        
        print("✅ Mental health sources added successfully!")
        print(f"📁 Backup saved to: {backup_file}")
        print("\n🧠 Added 10 mental health sources:")
        print("  • Psychology Today")
        print("  • Verywell Mind")
        print("  • Mind UK")
        print("  • NAMI")
        print("  • NIMH")
        print("  • SAMHSA")
        print("  • Mental Health America")
        print("  • Anxiety Centre")
        print("  • Headspace Blog")
        print("  • Calm Blog")
        print("\n🔄 Restart the scraper to apply changes:")
        print("   systemctl restart health-scraper.service")
        
    else:
        print("❌ Error: Could not find HEALTH_SOURCES dictionary")
        print("Manual addition required")

if __name__ == '__main__':
    add_mental_health_sources()