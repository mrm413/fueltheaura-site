#!/usr/bin/env python3
"""
Advanced Supervisor AI Employee
- Auto-updates code from GitHub
- Improves SEO automatically
- Optimizes website performance
- Enhances site design and UX
- Self-learning quality improvements
"""

import os
import sys
import time
import json
import subprocess
import requests
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import re
from bs4 import BeautifulSoup
from github import Github
import shutil

class AdvancedSupervisorAI:
    def __init__(self):
        self.base_dir = "/opt/fueltheaura-ai"
        self.data_dir = f"{self.base_dir}/data"
        self.backup_dir = f"{self.base_dir}/backups"
        self.reports_dir = f"{self.data_dir}/supervisor_reports"
        self.improvements_dir = f"{self.data_dir}/improvements"
        
        # GitHub configuration
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo_name = "mrm413/fueltheaura-site"
        
        # Create directories
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.improvements_dir, exist_ok=True)
        
        # Initialize databases
        self.init_databases()
    
    def init_databases(self):
        """Initialize improvement tracking database"""
        db_path = f"{self.data_dir}/supervisor_improvements.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
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
        conn.close()
    
    def auto_update_code(self):
        """Automatically pull latest code from GitHub"""
        print("🔄 Auto-updating code from GitHub...")
        
        try:
            # Pull latest changes
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if "Already up to date" in result.stdout:
                status = "up_to_date"
                changes = 0
            else:
                status = "updated"
                # Count changed files
                changes = len(re.findall(r'\d+ file[s]? changed', result.stdout))
            
            # Log improvement
            self.log_improvement(
                category="code_update",
                improvement_type="auto_update",
                description="Pulled latest code from GitHub",
                before_value="outdated",
                after_value="current",
                impact_score=0.8 if status == "updated" else 0.0
            )
            
            return {
                "status": status,
                "changes": changes,
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def analyze_seo(self):
        """Analyze SEO and suggest improvements"""
        print("🔍 Analyzing SEO...")
        
        improvements = []
        
        try:
            # Get all blog posts
            blog_dir = f"{self.base_dir}/src/blog/posts"
            if not os.path.exists(blog_dir):
                return {"status": "error", "error": "Blog directory not found"}
            
            posts = [f for f in os.listdir(blog_dir) if f.endswith('.njk')]
            
            for post_file in posts[:10]:  # Analyze first 10 posts
                post_path = os.path.join(blog_dir, post_file)
                
                with open(post_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract frontmatter
                frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
                if not frontmatter_match:
                    continue
                
                frontmatter = frontmatter_match.group(1)
                
                # Check title length
                title_match = re.search(r'title:\s*"([^"]+)"', frontmatter)
                if title_match:
                    title = title_match.group(1)
                    title_length = len(title)
                    
                    if title_length < 30 or title_length > 60:
                        improvements.append({
                            "file": post_file,
                            "type": "title_length",
                            "issue": f"Title length {title_length} (optimal: 30-60)",
                            "suggestion": "Adjust title length for better SEO"
                        })
                
                # Check meta description
                desc_match = re.search(r'description:\s*"([^"]+)"', frontmatter)
                if desc_match:
                    description = desc_match.group(1)
                    desc_length = len(description)
                    
                    if desc_length < 120 or desc_length > 160:
                        improvements.append({
                            "file": post_file,
                            "type": "meta_description",
                            "issue": f"Description length {desc_length} (optimal: 120-160)",
                            "suggestion": "Adjust meta description length"
                        })
                
                # Check for keywords
                keywords_match = re.search(r'keywords:\s*\[(.*?)\]', frontmatter)
                if not keywords_match:
                    improvements.append({
                        "file": post_file,
                        "type": "missing_keywords",
                        "issue": "No keywords defined",
                        "suggestion": "Add relevant keywords for SEO"
                    })
                
                # Check content length
                body_content = content.split('---', 2)[2] if content.count('---') >= 2 else content
                word_count = len(body_content.split())
                
                if word_count < 1500:
                    improvements.append({
                        "file": post_file,
                        "type": "content_length",
                        "issue": f"Word count {word_count} (optimal: 2000+)",
                        "suggestion": "Expand content for better SEO"
                    })
            
            # Save SEO report
            report_file = f"{self.improvements_dir}/seo_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(improvements, f, indent=2)
            
            return {
                "status": "success",
                "improvements_found": len(improvements),
                "report_file": report_file,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def optimize_performance(self):
        """Optimize website performance"""
        print("⚡ Optimizing performance...")
        
        optimizations = []
        
        try:
            # Check image sizes
            images_dir = f"{self.base_dir}/src/assets/images"
            if os.path.exists(images_dir):
                for root, dirs, files in os.walk(images_dir):
                    for file in files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                            file_path = os.path.join(root, file)
                            file_size = os.path.getsize(file_path) / 1024  # KB
                            
                            if file_size > 500:  # Larger than 500KB
                                optimizations.append({
                                    "type": "image_optimization",
                                    "file": file,
                                    "size_kb": round(file_size, 2),
                                    "suggestion": "Compress image to reduce load time"
                                })
            
            # Check CSS files
            css_dir = f"{self.base_dir}/src/assets/css"
            if os.path.exists(css_dir):
                for file in os.listdir(css_dir):
                    if file.endswith('.css'):
                        file_path = os.path.join(css_dir, file)
                        file_size = os.path.getsize(file_path) / 1024  # KB
                        
                        if file_size > 100:  # Larger than 100KB
                            optimizations.append({
                                "type": "css_optimization",
                                "file": file,
                                "size_kb": round(file_size, 2),
                                "suggestion": "Minify CSS to improve load time"
                            })
            
            # Check JavaScript files
            js_dir = f"{self.base_dir}/src/assets/js"
            if os.path.exists(js_dir):
                for file in os.listdir(js_dir):
                    if file.endswith('.js'):
                        file_path = os.path.join(js_dir, file)
                        file_size = os.path.getsize(file_path) / 1024  # KB
                        
                        if file_size > 100:  # Larger than 100KB
                            optimizations.append({
                                "type": "js_optimization",
                                "file": file,
                                "size_kb": round(file_size, 2),
                                "suggestion": "Minify JavaScript to improve load time"
                            })
            
            # Log improvements
            for opt in optimizations:
                self.log_improvement(
                    category="performance",
                    improvement_type=opt["type"],
                    description=opt["suggestion"],
                    before_value=f"{opt['size_kb']} KB",
                    after_value="optimized",
                    impact_score=0.6
                )
            
            return {
                "status": "success",
                "optimizations_found": len(optimizations),
                "optimizations": optimizations,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def enhance_design(self):
        """Analyze and enhance website design"""
        print("🎨 Enhancing design...")
        
        enhancements = []
        
        try:
            # Check for consistent color scheme
            css_files = []
            css_dir = f"{self.base_dir}/src/assets/css"
            
            if os.path.exists(css_dir):
                for file in os.listdir(css_dir):
                    if file.endswith('.css'):
                        css_files.append(os.path.join(css_dir, file))
            
            # Analyze color usage
            colors_used = set()
            for css_file in css_files:
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Find hex colors
                    hex_colors = re.findall(r'#[0-9A-Fa-f]{6}', content)
                    colors_used.update(hex_colors)
            
            if len(colors_used) > 10:
                enhancements.append({
                    "type": "color_consistency",
                    "issue": f"Too many colors used ({len(colors_used)})",
                    "suggestion": "Reduce to 5-7 primary colors for consistency"
                })
            
            # Check for responsive design
            has_media_queries = False
            for css_file in css_files:
                with open(css_file, 'r', encoding='utf-8') as f:
                    if '@media' in f.read():
                        has_media_queries = True
                        break
            
            if not has_media_queries:
                enhancements.append({
                    "type": "responsive_design",
                    "issue": "No media queries found",
                    "suggestion": "Add responsive breakpoints for mobile devices"
                })
            
            # Check for accessibility
            html_files = []
            src_dir = f"{self.base_dir}/src"
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    if file.endswith(('.html', '.njk')):
                        html_files.append(os.path.join(root, file))
            
            missing_alt_tags = 0
            for html_file in html_files[:10]:  # Check first 10 files
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Check for images without alt tags
                    img_tags = re.findall(r'<img[^>]*>', content)
                    for img in img_tags:
                        if 'alt=' not in img:
                            missing_alt_tags += 1
            
            if missing_alt_tags > 0:
                enhancements.append({
                    "type": "accessibility",
                    "issue": f"{missing_alt_tags} images missing alt tags",
                    "suggestion": "Add descriptive alt tags for accessibility"
                })
            
            # Save design report
            report_file = f"{self.improvements_dir}/design_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(enhancements, f, indent=2)
            
            return {
                "status": "success",
                "enhancements_found": len(enhancements),
                "report_file": report_file,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def analyze_content_quality(self):
        """Analyze content quality and suggest improvements"""
        print("📊 Analyzing content quality...")
        
        try:
            # Connect to content database
            db_path = f"{self.data_dir}/content_intelligence.db"
            if not os.path.exists(db_path):
                return {"status": "error", "error": "Content database not found"}
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get recent posts
            cursor.execute('''
                SELECT title, content, quality_score, created_at
                FROM blog_posts
                ORDER BY created_at DESC
                LIMIT 20
            ''')
            
            posts = cursor.fetchall()
            conn.close()
            
            quality_issues = []
            
            for title, content, quality_score, created_at in posts:
                # Check quality score
                if quality_score < 0.7:
                    quality_issues.append({
                        "title": title,
                        "issue": f"Low quality score: {quality_score}",
                        "suggestion": "Regenerate with higher quality standards"
                    })
                
                # Check content length
                word_count = len(content.split())
                if word_count < 1500:
                    quality_issues.append({
                        "title": title,
                        "issue": f"Short content: {word_count} words",
                        "suggestion": "Expand to 2000+ words for better SEO"
                    })
                
                # Check for citations
                if '[' not in content or ']' not in content:
                    quality_issues.append({
                        "title": title,
                        "issue": "No citations found",
                        "suggestion": "Add scientific references for credibility"
                    })
            
            return {
                "status": "success",
                "quality_issues": len(quality_issues),
                "issues": quality_issues,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def implement_auto_improvements(self):
        """Automatically implement safe improvements"""
        print("🔧 Implementing automatic improvements...")
        
        improvements_made = []
        
        try:
            # Auto-fix: Add missing alt tags to images
            src_dir = f"{self.base_dir}/src"
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    if file.endswith(('.html', '.njk')):
                        file_path = os.path.join(root, file)
                        
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Find images without alt tags
                        modified = False
                        new_content = content
                        
                        img_tags = re.findall(r'<img([^>]*)>', content)
                        for img_attrs in img_tags:
                            if 'alt=' not in img_attrs:
                                # Add generic alt tag
                                old_tag = f'<img{img_attrs}>'
                                new_tag = f'<img{img_attrs} alt="Health and wellness image">'
                                new_content = new_content.replace(old_tag, new_tag)
                                modified = True
                        
                        if modified:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            
                            improvements_made.append({
                                "file": file,
                                "improvement": "Added alt tags to images",
                                "impact": "Improved accessibility and SEO"
                            })
            
            # Auto-fix: Optimize CSS (remove comments and extra whitespace)
            css_dir = f"{self.base_dir}/src/assets/css"
            if os.path.exists(css_dir):
                for file in os.listdir(css_dir):
                    if file.endswith('.css'):
                        file_path = os.path.join(css_dir, file)
                        
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Remove comments
                        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
                        
                        # Remove extra whitespace
                        content = re.sub(r'\s+', ' ', content)
                        content = re.sub(r'\s*{\s*', '{', content)
                        content = re.sub(r'\s*}\s*', '}', content)
                        content = re.sub(r'\s*:\s*', ':', content)
                        content = re.sub(r'\s*;\s*', ';', content)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        improvements_made.append({
                            "file": file,
                            "improvement": "Optimized CSS file",
                            "impact": "Reduced file size and load time"
                        })
            
            # Log all improvements
            for improvement in improvements_made:
                self.log_improvement(
                    category="auto_improvement",
                    improvement_type=improvement["improvement"],
                    description=improvement["impact"],
                    before_value="unoptimized",
                    after_value="optimized",
                    impact_score=0.7
                )
            
            return {
                "status": "success",
                "improvements_made": len(improvements_made),
                "details": improvements_made,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def log_improvement(self, category, improvement_type, description, before_value, after_value, impact_score):
        """Log improvement to database"""
        try:
            db_path = f"{self.data_dir}/supervisor_improvements.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO improvements 
                (timestamp, category, improvement_type, description, before_value, after_value, impact_score, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                category,
                improvement_type,
                description,
                before_value,
                after_value,
                impact_score,
                "completed"
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"  ⚠️ Error logging improvement: {e}")
    
    def generate_improvement_report(self):
        """Generate comprehensive improvement report"""
        print("📋 Generating improvement report...")
        
        try:
            db_path = f"{self.data_dir}/supervisor_improvements.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get improvements from last 24 hours
            yesterday = (datetime.now() - timedelta(days=1)).isoformat()
            
            cursor.execute('''
                SELECT category, COUNT(*), AVG(impact_score)
                FROM improvements
                WHERE timestamp > ?
                GROUP BY category
            ''', (yesterday,))
            
            improvements_by_category = cursor.fetchall()
            
            cursor.execute('''
                SELECT COUNT(*), AVG(impact_score)
                FROM improvements
                WHERE timestamp > ?
            ''', (yesterday,))
            
            total_improvements, avg_impact = cursor.fetchone()
            
            conn.close()
            
            report = {
                "timestamp": datetime.now().isoformat(),
                "period": "last_24_hours",
                "total_improvements": total_improvements or 0,
                "average_impact_score": round(avg_impact or 0, 2),
                "improvements_by_category": [
                    {
                        "category": cat,
                        "count": count,
                        "avg_impact": round(avg_imp, 2)
                    }
                    for cat, count, avg_imp in improvements_by_category
                ]
            }
            
            # Save report
            report_file = f"{self.reports_dir}/improvement_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            return report
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def run_advanced_supervision(self):
        """Run complete advanced supervision cycle"""
        print(f"🤖 Advanced Supervisor AI - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "code_update": self.auto_update_code(),
            "seo_analysis": self.analyze_seo(),
            "performance_optimization": self.optimize_performance(),
            "design_enhancement": self.enhance_design(),
            "content_quality": self.analyze_content_quality(),
            "auto_improvements": self.implement_auto_improvements(),
            "improvement_summary": self.generate_improvement_report()
        }
        
        # Save comprehensive report
        filename = f"{self.reports_dir}/advanced_supervisor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print(f"\n📊 Advanced Supervision Summary:")
        print(f"  Code updates: {report['code_update'].get('status', 'N/A')}")
        print(f"  SEO improvements found: {report['seo_analysis'].get('improvements_found', 0)}")
        print(f"  Performance optimizations: {report['performance_optimization'].get('optimizations_found', 0)}")
        print(f"  Design enhancements: {report['design_enhancement'].get('enhancements_found', 0)}")
        print(f"  Content quality issues: {report['content_quality'].get('quality_issues', 0)}")
        print(f"  Auto-improvements made: {report['auto_improvements'].get('improvements_made', 0)}")
        print(f"  Total improvements (24h): {report['improvement_summary'].get('total_improvements', 0)}")
        print(f"  Report saved: {filename}")
        print()
        
        return report

def main():
    """Main supervision loop"""
    supervisor = AdvancedSupervisorAI()
    
    print("🤖 Advanced Supervisor AI Employee Started")
    print("Running advanced supervision every 6 hours...")
    print()
    
    while True:
        try:
            supervisor.run_advanced_supervision()
            print("⏰ Next advanced supervision in 6 hours...")
            print()
            time.sleep(6 * 60 * 60)  # 6 hours
        except KeyboardInterrupt:
            print("\n👋 Advanced Supervisor AI stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Retrying in 1 hour...")
            time.sleep(60 * 60)

if __name__ == "__main__":
    main()