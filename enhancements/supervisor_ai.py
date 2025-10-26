#!/usr/bin/env python3
"""
Supervisor AI Employee
Updates systems, performs security scanning, manages backups
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime
import shutil

class SupervisorAI:
    def __init__(self):
        self.base_dir = "/opt/fueltheaura-ai"
        self.data_dir = f"{self.base_dir}/data"
        self.backup_dir = f"{self.base_dir}/backups"
        self.reports_dir = f"{self.data_dir}/supervisor_reports"
        
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def check_system_updates(self):
        """Check for system updates"""
        print("🔄 Checking for system updates...")
        
        try:
            # Check for package updates
            result = subprocess.run(
                ['apt', 'list', '--upgradable'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            updates_available = len(result.stdout.split('\n')) - 1
            
            return {
                "updates_available": updates_available,
                "status": "checked",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def backup_databases(self):
        """Backup all databases"""
        print("💾 Creating database backups...")
        
        backups_created = []
        
        try:
            # Backup content intelligence database
            if os.path.exists(f"{self.data_dir}/content_intelligence.db"):
                backup_name = f"content_intelligence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                shutil.copy2(
                    f"{self.data_dir}/content_intelligence.db",
                    f"{self.backup_dir}/{backup_name}"
                )
                backups_created.append(backup_name)
            
            # Backup health content database
            if os.path.exists(f"{self.data_dir}/health_content.db"):
                backup_name = f"health_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                shutil.copy2(
                    f"{self.data_dir}/health_content.db",
                    f"{self.backup_dir}/{backup_name}"
                )
                backups_created.append(backup_name)
            
            # Backup AI learning database
            if os.path.exists(f"{self.data_dir}/ai_learning.db"):
                backup_name = f"ai_learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                shutil.copy2(
                    f"{self.data_dir}/ai_learning.db",
                    f"{self.backup_dir}/{backup_name}"
                )
                backups_created.append(backup_name)
            
            # Clean old backups (keep last 7 days)
            self.cleanup_old_backups()
            
            return {
                "status": "success",
                "backups_created": backups_created,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def cleanup_old_backups(self):
        """Remove backups older than 7 days"""
        try:
            current_time = time.time()
            for filename in os.listdir(self.backup_dir):
                filepath = os.path.join(self.backup_dir, filename)
                if os.path.isfile(filepath):
                    file_age = current_time - os.path.getmtime(filepath)
                    if file_age > 7 * 24 * 60 * 60:  # 7 days
                        os.remove(filepath)
                        print(f"  🗑️  Removed old backup: {filename}")
        except Exception as e:
            print(f"  ⚠️  Cleanup error: {e}")
    
    def check_disk_space(self):
        """Check available disk space"""
        print("💿 Checking disk space...")
        
        try:
            stat = os.statvfs(self.base_dir)
            free_space_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
            total_space_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)
            used_percent = ((total_space_gb - free_space_gb) / total_space_gb) * 100
            
            return {
                "free_space_gb": round(free_space_gb, 2),
                "total_space_gb": round(total_space_gb, 2),
                "used_percent": round(used_percent, 2),
                "status": "warning" if used_percent > 80 else "ok"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def check_service_health(self):
        """Check health of all AI services"""
        print("🏥 Checking service health...")
        
        services = [
            "fueltheaura-ai.service",
            "health-scraper.service",
            "ai-learning.service"
        ]
        
        service_status = {}
        
        for service in services:
            try:
                result = subprocess.run(
                    ['systemctl', 'is-active', service],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                service_status[service] = result.stdout.strip()
            except Exception as e:
                service_status[service] = f"error: {e}"
        
        return service_status
    
    def run_supervision(self):
        """Run complete supervision cycle"""
        print(f"🤖 Supervisor AI - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "system_updates": self.check_system_updates(),
            "backups": self.backup_databases(),
            "disk_space": self.check_disk_space(),
            "service_health": self.check_service_health()
        }
        
        # Save report
        filename = f"{self.reports_dir}/supervisor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print(f"\n📊 Supervision Summary:")
        print(f"  Updates available: {report['system_updates'].get('updates_available', 'N/A')}")
        print(f"  Backups created: {len(report['backups'].get('backups_created', []))}")
        print(f"  Disk space: {report['disk_space'].get('free_space_gb', 'N/A')} GB free")
        print(f"  Report saved: {filename}")
        print()
        
        return report

def main():
    """Main supervision loop"""
    supervisor = SupervisorAI()
    
    print("🤖 Supervisor AI Employee Started")
    print("Running supervision every 6 hours...")
    print()
    
    while True:
        try:
            supervisor.run_supervision()
            print("⏰ Next supervision in 6 hours...")
            print()
            time.sleep(6 * 60 * 60)  # 6 hours
        except KeyboardInterrupt:
            print("\n👋 Supervisor AI stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Retrying in 1 hour...")
            time.sleep(60 * 60)

if __name__ == "__main__":
    main()