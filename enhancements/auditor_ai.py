#!/usr/bin/env python3
"""
Auditor AI Employee
Monitors website 24/7, checks for bugs, errors, and legal compliance
"""

import os
import sys
import time
import json
import sqlite3
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class AuditorAI:
    def __init__(self):
        self.website_url = "https://fueltheaura.com"
        self.data_dir = "/opt/fueltheaura-ai/data/audits"
        os.makedirs(self.data_dir, exist_ok=True)
        
    def check_website_status(self):
        """Check if website is accessible"""
        try:
            response = requests.get(self.website_url, timeout=10)
            return {
                "status": "online" if response.status_code == 200 else "error",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            return {
                "status": "offline",
                "error": str(e)
            }
    
    def check_blog_posts(self):
        """Check blog posts for issues"""
        issues = []
        
        try:
            # Check blog listing page
            response = requests.get(f"{self.website_url}/blog/", timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check for broken links
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href and href.startswith('/blog/posts/'):
                    full_url = f"{self.website_url}{href}"
                    try:
                        post_response = requests.get(full_url, timeout=5)
                        if post_response.status_code != 200:
                            issues.append({
                                "type": "broken_link",
                                "url": full_url,
                                "status_code": post_response.status_code
                            })
                    except Exception as e:
                        issues.append({
                            "type": "broken_link",
                            "url": full_url,
                            "error": str(e)
                        })
            
            return issues
        except Exception as e:
            return [{"type": "audit_error", "error": str(e)}]
    
    def check_legal_compliance(self):
        """Check for required legal disclaimers"""
        compliance_issues = []
        
        try:
            # Check for Terms of Service
            response = requests.get(f"{self.website_url}/terms", timeout=10)
            if response.status_code != 200:
                compliance_issues.append({
                    "type": "missing_terms",
                    "severity": "high",
                    "message": "Terms of Service page not accessible"
                })
            
            # Check blog posts for medical disclaimers
            blog_response = requests.get(f"{self.website_url}/blog/", timeout=10)
            soup = BeautifulSoup(blog_response.content, 'html.parser')
            
            # Sample check on first blog post
            first_post_link = soup.find('a', href=lambda x: x and '/blog/posts/' in x)
            if first_post_link:
                post_url = f"{self.website_url}{first_post_link['href']}"
                post_response = requests.get(post_url, timeout=10)
                post_content = post_response.text.lower()
                
                # Check for disclaimer keywords
                if 'disclaimer' not in post_content and 'medical advice' not in post_content:
                    compliance_issues.append({
                        "type": "missing_disclaimer",
                        "severity": "medium",
                        "url": post_url,
                        "message": "Blog post may be missing medical disclaimer"
                    })
            
            return compliance_issues
        except Exception as e:
            return [{"type": "compliance_check_error", "error": str(e)}]
    
    def run_audit(self):
        """Run complete audit"""
        print(f"🔍 Starting audit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        audit_results = {
            "timestamp": datetime.now().isoformat(),
            "website_status": self.check_website_status(),
            "blog_issues": self.check_blog_posts(),
            "compliance_issues": self.check_legal_compliance()
        }
        
        # Save audit results
        filename = f"{self.data_dir}/audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(audit_results, f, indent=2)
        
        # Print summary
        total_issues = len(audit_results['blog_issues']) + len(audit_results['compliance_issues'])
        
        if audit_results['website_status']['status'] == 'online':
            print(f"✅ Website: ONLINE ({audit_results['website_status']['response_time']:.2f}s)")
        else:
            print(f"❌ Website: OFFLINE")
        
        print(f"📊 Issues found: {total_issues}")
        print(f"💾 Audit saved: {filename}")
        
        return audit_results

def main():
    """Main audit loop"""
    auditor = AuditorAI()
    
    print("🤖 Auditor AI Employee Started")
    print("Monitoring website every 4 hours...")
    print()
    
    while True:
        try:
            auditor.run_audit()
            print("⏰ Next audit in 4 hours...")
            print()
            time.sleep(4 * 60 * 60)  # 4 hours
        except KeyboardInterrupt:
            print("\n👋 Auditor AI stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Retrying in 1 hour...")
            time.sleep(60 * 60)

if __name__ == "__main__":
    main()