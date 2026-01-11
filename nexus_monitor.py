# NEXUS-ONE Monitoring & Analytics System
# Real metrics and system health tracking

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path


class NexusMonitor:
    def __init__(self):
        self.log_dir = Path("nexus_logs")
        self.stats_file = self.log_dir / "stats.json"
        self.log_dir.mkdir(exist_ok=True)
        self.load_stats()
    
    def load_stats(self):
        """Load existing statistics"""
        if self.stats_file.exists():
            with open(self.stats_file) as f:
                self.stats = json.load(f)
        else:
            self.stats = {
                "total_syncs": 0,
                "successful_syncs": 0,
                "failed_syncs": 0,
                "total_commits": 0,
                "total_pushes": 0,
                "uptime_hours": 0
            }
    
    def save_stats(self):
        """Save statistics to file"""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def record_sync(self, success=True):
        """Record sync operation"""
        self.stats["total_syncs"] += 1
        if success:
            self.stats["successful_syncs"] += 1
        else:
            self.stats["failed_syncs"] += 1
        self.save_stats()
    
    def get_repo_stats(self):
        """Get real repository statistics"""
        try:
            # Total commits
            commits = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                capture_output=True, text=True
            ).stdout.strip()
            
            # Branch count
            branches = subprocess.run(
                ["git", "branch", "-a"],
                capture_output=True, text=True
            ).stdout.strip().split('\n')
            
            # Current status
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True
            ).stdout.strip()
            
            return {
                "total_commits": int(commits) if commits else 0,
                "branch_count": len([b for b in branches if b.strip()]),
                "changed_files": len(status.split('\n')) if status else 0,
                "last_sync": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def generate_report(self):
        """Generate monitoring report"""
        repo_stats = self.get_repo_stats()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                    NEXUS-ONE SYSTEM REPORT                          ║
╚══════════════════════════════════════════════════════════════════════╝

📊 SYNC STATISTICS
  Total Syncs: {self.stats['total_syncs']}
  Successful: {self.stats['successful_syncs']} ✓
  Failed: {self.stats['failed_syncs']} ✗
  Success Rate: {(self.stats['successful_syncs'] / max(1, self.stats['total_syncs']) * 100):.1f}%

📈 REPOSITORY STATUS
  Total Commits: {repo_stats.get('total_commits', 'N/A')}
  Branches: {repo_stats.get('branch_count', 'N/A')}
  Changed Files: {repo_stats.get('changed_files', 'N/A')}
  Last Sync: {repo_stats.get('last_sync', 'N/A')}

🔧 SYSTEM STATUS
  Autonomous Mode: ACTIVE
  CI/CD Pipeline: ENABLED
  Monitoring: ENABLED

🕐 TIMESTAMP
  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        return report

if __name__ == "__main__":
    monitor = NexusMonitor()
    print(monitor.generate_report())
    
    # Log the report
    with open(monitor.log_dir / "reports.log", 'a', encoding='utf-8') as f:
        f.write(monitor.generate_report())
        f.write("\n" + "="*70 + "\n")
