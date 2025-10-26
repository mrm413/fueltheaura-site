#!/usr/bin/env python3
"""
Reporter AI Employee
Generates detailed operational reports
"""

import os
import sys
import time
import json
import sqlite3
from datetime import datetime, timedelta

class ReporterAI:
    def __init__(self):
        self.base_dir = "/opt/fueltheaura-ai"
        self.data_dir = f"{self.base_dir}/data"
        self.reports_dir = f"{self.data_dir}/reports"
        
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def get_content_stats(self):
        """Get content generation statistics"""
        try:
            conn = sqlite3.connect(f"{self.data_dir}/content_intelligence.db")
            cursor = conn.cursor()
            
            # Total posts
            cursor.execute("SELECT COUNT(*) FROM generated_posts")
            total_posts = cursor.fetchone()[0]
            
            # Posts in last 24 hours
            yesterday = (datetime.now() - timedelta(days=1)).isoformat()
            cursor.execute("SELECT COUNT(*) FROM generated_posts WHERE created_at > ?", (yesterday,))
            posts_24h = cursor.fetchone()[0]
            
            # Posts in last 7 days
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            cursor.execute("SELECT COUNT(*) FROM generated_posts WHERE created_at > ?", (week_ago,))
            posts_7d = cursor.fetchone()[0]
            
            # Average quality score
            cursor.execute("SELECT AVG(quality_score) FROM generated_posts")
            avg_quality = cursor.fetchone()[0] or 0
            
            conn.close()
            
            return {
                "total_posts": total_posts,
                "posts_last_24h": posts_24h,
                "posts_last_7d": posts_7d,
                "average_quality": round(avg_quality, 2)
            }
        except Exception as e:
            return {
                "error": str(e)
            }
    
    def get_scraping_stats(self):
        """Get web scraping statistics"""
        try:
            conn = sqlite3.connect(f"{self.data_dir}/health_content.db")
            cursor = conn.cursor()
            
            # Total articles
            cursor.execute("SELECT COUNT(*) FROM health_articles")
            total_articles = cursor.fetchone()[0]
            
            # Articles by category
            cursor.execute("SELECT category, COUNT(*) FROM health_articles GROUP BY category ORDER BY COUNT(*) DESC")
            categories = dict(cursor.fetchall())
            
            # Database size
            db_size = os.path.getsize(f"{self.data_dir}/health_content.db") / (1024 * 1024)  # MB
            
            conn.close()
            
            return {
                "total_articles": total_articles,
                "categories": categories,
                "database_size_mb": round(db_size, 2)
            }
        except Exception as e:
            return {
                "error": str(e)
            }
    
    def get_audit_summary(self):
        """Get audit summary"""
        try:
            audit_dir = f"{self.data_dir}/audits"
            if not os.path.exists(audit_dir):
                return {"audits_available": 0}
            
            audit_files = [f for f in os.listdir(audit_dir) if f.endswith('.json')]
            
            if not audit_files:
                return {"audits_available": 0}
            
            # Get most recent audit
            latest_audit = sorted(audit_files)[-1]
            with open(f"{audit_dir}/{latest_audit}", 'r') as f:
                audit_data = json.load(f)
            
            return {
                "audits_available": len(audit_files),
                "latest_audit": latest_audit,
                "website_status": audit_data.get('website_status', {}).get('status', 'unknown'),
                "issues_found": len(audit_data.get('blog_issues', [])) + len(audit_data.get('compliance_issues', []))
            }
        except Exception as e:
            return {
                "error": str(e)
            }
    
    def get_supervisor_summary(self):
        """Get supervisor summary"""
        try:
            supervisor_dir = f"{self.data_dir}/supervisor_reports"
            if not os.path.exists(supervisor_dir):
                return {"reports_available": 0}
            
            report_files = [f for f in os.listdir(supervisor_dir) if f.endswith('.json')]
            
            if not report_files:
                return {"reports_available": 0}
            
            # Get most recent report
            latest_report = sorted(report_files)[-1]
            with open(f"{supervisor_dir}/{latest_report}", 'r') as f:
                report_data = json.load(f)
            
            return {
                "reports_available": len(report_files),
                "latest_report": latest_report,
                "backups_created": len(report_data.get('backups', {}).get('backups_created', [])),
                "disk_space_free_gb": report_data.get('disk_space', {}).get('free_space_gb', 'N/A')
            }
        except Exception as e:
            return {
                "error": str(e)
            }
    
    def get_analyst_summary(self):
        """Get analyst summary"""
        try:
            analyst_dir = f"{self.data_dir}/analyst_reports"
            if not os.path.exists(analyst_dir):
                return {"analyses_available": 0}
            
            analysis_files = [f for f in os.listdir(analyst_dir) if f.endswith('.json')]
            
            if not analysis_files:
                return {"analyses_available": 0}
            
            # Get most recent analysis
            latest_analysis = sorted(analysis_files)[-1]
            with open(f"{analyst_dir}/{latest_analysis}", 'r') as f:
                analysis_data = json.load(f)
            
            return {
                "analyses_available": len(analysis_files),
                "latest_analysis": latest_analysis,
                "posts_analyzed": analysis_data.get('posts_analyzed', 0),
                "average_quality": analysis_data.get('average_quality', 0)
            }
        except Exception as e:
            return {
                "error": str(e)
            }
    
    def generate_report(self):
        """Generate comprehensive operational report"""
        print(f"📝 Reporter AI - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "report_period": "24 hours",
            "content_generation": self.get_content_stats(),
            "web_scraping": self.get_scraping_stats(),
            "auditor": self.get_audit_summary(),
            "supervisor": self.get_supervisor_summary(),
            "analyst": self.get_analyst_summary()
        }
        
        # Save report
        filename = f"{self.reports_dir}/operational_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n📊 Operational Report Summary:")
        print(f"\n📝 Content Generation:")
        print(f"  Total posts: {report['content_generation'].get('total_posts', 'N/A')}")
        print(f"  Posts (24h): {report['content_generation'].get('posts_last_24h', 'N/A')}")
        print(f"  Posts (7d): {report['content_generation'].get('posts_last_7d', 'N/A')}")
        print(f"  Avg quality: {report['content_generation'].get('average_quality', 'N/A')}")
        
        print(f"\n🌐 Web Scraping:")
        print(f"  Total articles: {report['web_scraping'].get('total_articles', 'N/A')}")
        print(f"  Database size: {report['web_scraping'].get('database_size_mb', 'N/A')} MB")
        
        print(f"\n🔍 Auditor:")
        print(f"  Audits available: {report['auditor'].get('audits_available', 'N/A')}")
        print(f"  Website status: {report['auditor'].get('website_status', 'N/A')}")
        
        print(f"\n🤖 Supervisor:")
        print(f"  Reports available: {report['supervisor'].get('reports_available', 'N/A')}")
        print(f"  Disk space free: {report['supervisor'].get('disk_space_free_gb', 'N/A')} GB")
        
        print(f"\n📊 Analyst:")
        print(f"  Analyses available: {report['analyst'].get('analyses_available', 'N/A')}")
        print(f"  Average quality: {report['analyst'].get('average_quality', 'N/A')}")
        
        print(f"\n💾 Report saved: {filename}")
        print()
        
        return report

def main():
    """Main reporting loop"""
    reporter = ReporterAI()
    
    print("🤖 Reporter AI Employee Started")
    print("Generating reports every 24 hours...")
    print()
    
    while True:
        try:
            reporter.generate_report()
            print("⏰ Next report in 24 hours...")
            print()
            time.sleep(24 * 60 * 60)  # 24 hours
        except KeyboardInterrupt:
            print("\n👋 Reporter AI stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Retrying in 1 hour...")
            time.sleep(60 * 60)

if __name__ == "__main__":
    main()
