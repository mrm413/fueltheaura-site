#!/usr/bin/env python3
"""
Analyst AI Employee
Reviews blogs and suggests improvements for stronger content
"""

import os
import sys
import time
import json
import sqlite3
from datetime import datetime
import requests
from bs4 import BeautifulSoup

class AnalystAI:
    def __init__(self):
        self.base_dir = "/opt/fueltheaura-ai"
        self.data_dir = f"{self.base_dir}/data"
        self.reports_dir = f"{self.data_dir}/analyst_reports"
        self.website_url = "https://fueltheaura.com"
        
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def analyze_blog_post(self, post_url):
        """Analyze a single blog post"""
        try:
            response = requests.get(post_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract content
            content = soup.find('div', class_='post-body')
            if not content:
                return None
            
            text = content.get_text()
            
            # Analysis metrics
            analysis = {
                "url": post_url,
                "word_count": len(text.split()),
                "paragraph_count": len(content.find_all('p')),
                "heading_count": len(content.find_all(['h1', 'h2', 'h3', 'h4'])),
                "list_count": len(content.find_all(['ul', 'ol'])),
                "link_count": len(content.find_all('a')),
                "image_count": len(content.find_all('img')),
            }
            
            # Generate suggestions
            suggestions = []
            
            if analysis['word_count'] < 1500:
                suggestions.append({
                    "type": "length",
                    "severity": "medium",
                    "message": f"Post is {analysis['word_count']} words. Consider expanding to 2000+ words for better SEO."
                })
            
            if analysis['heading_count'] < 5:
                suggestions.append({
                    "type": "structure",
                    "severity": "low",
                    "message": "Add more headings (H2, H3) to improve readability and SEO."
                })
            
            if analysis['list_count'] == 0:
                suggestions.append({
                    "type": "formatting",
                    "severity": "low",
                    "message": "Consider adding bullet points or numbered lists for better readability."
                })
            
            if analysis['link_count'] < 3:
                suggestions.append({
                    "type": "seo",
                    "severity": "medium",
                    "message": "Add more internal and external links to improve SEO and provide value."
                })
            
            if analysis['image_count'] == 0:
                suggestions.append({
                    "type": "engagement",
                    "severity": "low",
                    "message": "Consider adding images to increase engagement."
                })
            
            analysis['suggestions'] = suggestions
            analysis['quality_score'] = self.calculate_quality_score(analysis)
            
            return analysis
            
        except Exception as e:
            return {
                "url": post_url,
                "error": str(e)
            }
    
    def calculate_quality_score(self, analysis):
        """Calculate overall quality score (0-100)"""
        score = 50  # Base score
        
        # Word count (max +20)
        if analysis['word_count'] >= 2000:
            score += 20
        elif analysis['word_count'] >= 1500:
            score += 15
        elif analysis['word_count'] >= 1000:
            score += 10
        
        # Structure (max +15)
        if analysis['heading_count'] >= 8:
            score += 15
        elif analysis['heading_count'] >= 5:
            score += 10
        elif analysis['heading_count'] >= 3:
            score += 5
        
        # Formatting (max +10)
        if analysis['list_count'] >= 3:
            score += 10
        elif analysis['list_count'] >= 1:
            score += 5
        
        # Links (max +10)
        if analysis['link_count'] >= 10:
            score += 10
        elif analysis['link_count'] >= 5:
            score += 7
        elif analysis['link_count'] >= 3:
            score += 4
        
        # Images (max +5)
        if analysis['image_count'] >= 3:
            score += 5
        elif analysis['image_count'] >= 1:
            score += 3
        
        return min(score, 100)
    
    def get_recent_posts(self):
        """Get list of recent blog posts"""
        try:
            response = requests.get(f"{self.website_url}/blog/", timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            posts = []
            for link in soup.find_all('a', href=lambda x: x and '/blog/posts/' in x):
                href = link.get('href')
                if href and href not in [p['url'] for p in posts]:
                    posts.append({
                        'url': f"{self.website_url}{href}",
                        'title': link.get_text().strip()
                    })
            
            return posts[:5]  # Return 5 most recent
        except Exception as e:
            print(f"Error getting posts: {e}")
            return []
    
    def run_analysis(self):
        """Run complete analysis"""
        print(f"📊 Analyst AI - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Get recent posts
        print("🔍 Fetching recent blog posts...")
        posts = self.get_recent_posts()
        
        if not posts:
            print("⚠️  No posts found to analyze")
            return
        
        print(f"Found {len(posts)} posts to analyze\n")
        
        # Analyze each post
        analyses = []
        for post in posts:
            print(f"Analyzing: {post['title'][:50]}...")
            analysis = self.analyze_blog_post(post['url'])
            if analysis:
                analyses.append(analysis)
                print(f"  Quality Score: {analysis.get('quality_score', 'N/A')}/100")
                print(f"  Suggestions: {len(analysis.get('suggestions', []))}")
            print()
        
        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "posts_analyzed": len(analyses),
            "analyses": analyses,
            "average_quality": sum(a.get('quality_score', 0) for a in analyses) / len(analyses) if analyses else 0
        }
        
        # Save report
        filename = f"{self.reports_dir}/analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Analysis Summary:")
        print(f"  Posts analyzed: {report['posts_analyzed']}")
        print(f"  Average quality: {report['average_quality']:.1f}/100")
        print(f"  Report saved: {filename}")
        print()
        
        return report

def main():
    """Main analysis loop"""
    analyst = AnalystAI()
    
    print("🤖 Analyst AI Employee Started")
    print("Running analysis every 12 hours...")
    print()
    
    while True:
        try:
            analyst.run_analysis()
            print("⏰ Next analysis in 12 hours...")
            print()
            time.sleep(12 * 60 * 60)  # 12 hours
        except KeyboardInterrupt:
            print("\n👋 Analyst AI stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Retrying in 1 hour...")
            time.sleep(60 * 60)

if __name__ == "__main__":
    main()