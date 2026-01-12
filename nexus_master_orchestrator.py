#!/usr/bin/env python3
"""
NEXUS-ONE Master Orchestrator
==============================
Coordinates all NEXUS systems and GitHub Copilot collaboration
- Manages all learning modules (self-learner, social-learner, code-generator)
- Facilitates Copilot<->NEXUS communication
- Monitors system health
- Optimizes performance
- 3-hour intensive development session manager
"""

import asyncio
import json
import logging
import multiprocessing as mp
import os
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Setup
WORKSPACE = Path(__file__).parent
DATA_DIR = WORKSPACE / "nexus_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = WORKSPACE / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(name)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "master_orchestrator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MasterOrchestrator")

# Import NEXUS modules
try:
    from copilot_nexus_collaboration import CollaborationEngine
    COLLAB_AVAILABLE = True
except ImportError:
    COLLAB_AVAILABLE = False
    logger.warning("Collaboration engine not available")

try:
    from code_generator import CodeGenerator
    CODE_GEN_AVAILABLE = True
except ImportError:
    CODE_GEN_AVAILABLE = False

try:
    from nexus_self_learner import KnowledgeGraph, SelfLearner
    SELF_LEARNER_AVAILABLE = True
except ImportError:
    SELF_LEARNER_AVAILABLE = False

try:
    from social_learner import SocialLearner
    SOCIAL_AVAILABLE = True
except ImportError:
    SOCIAL_AVAILABLE = False


class MasterOrchestrator:
    """
    Master orchestrator that coordinates all NEXUS-ONE systems
    and manages Copilot collaboration
    """
    
    def __init__(self, session_duration_hours: float = 3.0):
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(hours=session_duration_hours)
        self.session_duration = session_duration_hours
        
        # Initialize components
        self.collaboration_engine = None
        self.knowledge_graph = None
        self.self_learner = None
        self.social_learner = None
        self.code_generator = None
        
        # Metrics
        self.metrics = {
            "session_start": self.start_time.isoformat(),
            "session_end_scheduled": self.end_time.isoformat(),
            "total_tasks_completed": 0,
            "code_files_analyzed": 0,
            "code_files_generated": 0,
            "knowledge_items_learned": 0,
            "social_trends_tracked": 0,
            "copilot_actions_processed": 0,
            "errors_encountered": 0,
            "errors_fixed": 0
        }
        
        # Task queue
        self.task_queue = []
        self.active_tasks = {}
        
        logger.info(f"🎯 Master Orchestrator initialized")
        logger.info(f"⏱️  Session: {session_duration_hours} hours ({self.end_time.strftime('%H:%M:%S')})")
        
    def initialize_systems(self):
        """Initialize all NEXUS systems"""
        logger.info("🚀 Initializing NEXUS systems...")
        
        # Collaboration Engine
        if COLLAB_AVAILABLE:
            try:
                self.collaboration_engine = CollaborationEngine()
                logger.info("✅ Collaboration Engine initialized")
            except Exception as e:
                logger.error(f"❌ Collaboration Engine failed: {e}")
        
        # Knowledge Graph
        if SELF_LEARNER_AVAILABLE:
            try:
                self.knowledge_graph = KnowledgeGraph()
                logger.info("✅ Knowledge Graph initialized")
            except Exception as e:
                logger.error(f"❌ Knowledge Graph failed: {e}")
        
        # Self Learner
        if SELF_LEARNER_AVAILABLE:
            try:
                self.self_learner = SelfLearner(str(WORKSPACE))
                logger.info("✅ Self Learner initialized")
            except Exception as e:
                logger.error(f"❌ Self Learner failed: {e}")
        
        # Social Learner
        if SOCIAL_AVAILABLE:
            try:
                self.social_learner = SocialLearner()
                logger.info("✅ Social Learner initialized")
            except Exception as e:
                logger.error(f"❌ Social Learner failed: {e}")
        
        # Code Generator
        if CODE_GEN_AVAILABLE:
            try:
                self.code_generator = CodeGenerator()
                logger.info("✅ Code Generator initialized")
            except Exception as e:
                logger.error(f"❌ Code Generator failed: {e}")
        
        logger.info("✅ All systems initialized\n")
    
    def record_copilot_action(self, action_type: str, details: Dict):
        """
        Record an action I (GitHub Copilot) take
        NEXUS will learn from it
        """
        if self.collaboration_engine:
            self.collaboration_engine.copilot_action(action_type, details)
            self.metrics["copilot_actions_processed"] += 1
    
    def get_nexus_context(self, query: str) -> Dict:
        """
        Get context from NEXUS to help me make better decisions
        """
        if self.collaboration_engine:
            return self.collaboration_engine.nexus_provides_context(query)
        return {}
    
    def analyze_workspace(self):
        """Deep analysis of workspace"""
        logger.info("🔍 Analyzing workspace...")
        
        analysis = {
            "python_files": list(WORKSPACE.rglob("*.py")),
            "powershell_files": list(WORKSPACE.rglob("*.ps1")),
            "markdown_files": list(WORKSPACE.rglob("*.md")),
            "json_files": list(WORKSPACE.rglob("*.json")),
        }
        
        for file_type, files in analysis.items():
            logger.info(f"  {file_type}: {len(files)} files")
            self.metrics["code_files_analyzed"] += len(files)
        
        # Record this action
        self.record_copilot_action("workspace_analysis", {
            "files_analyzed": sum(len(files) for files in analysis.values()),
            "file_types": list(analysis.keys())
        })
        
        return analysis
    
    def learn_from_existing_code(self):
        """Learn patterns from existing codebase"""
        logger.info("🧠 Learning from existing code...")
        
        if self.self_learner:
            try:
                # Analyze Python files
                py_files = list(WORKSPACE.rglob("*.py"))[:20]  # First 20 files
                
                for py_file in py_files:
                    try:
                        self.self_learner.analyze_python_file(str(py_file))
                        self.metrics["knowledge_items_learned"] += 1
                    except Exception as e:
                        logger.warning(f"Failed to analyze {py_file.name}: {e}")
                
                logger.info(f"✅ Learned from {len(py_files)} Python files")
                
                # Record action
                self.record_copilot_action("code_learning", {
                    "files_processed": len(py_files),
                    "patterns_extracted": self.metrics["knowledge_items_learned"]
                })
                
            except Exception as e:
                logger.error(f"Learning failed: {e}")
                self.metrics["errors_encountered"] += 1
    
    def track_social_trends(self):
        """Track trends from GitHub and YouTube"""
        logger.info("🌐 Tracking social trends...")
        
        if self.social_learner:
            try:
                # GitHub trends
                github_trends = self.social_learner.github_trends()
                logger.info(f"  GitHub: {len(github_trends)} trending repos")
                
                # YouTube trends (if available)
                try:
                    youtube_trends = self.social_learner.youtube_trends()
                    logger.info(f"  YouTube: {len(youtube_trends)} trending videos")
                except:
                    youtube_trends = []
                
                self.metrics["social_trends_tracked"] += len(github_trends) + len(youtube_trends)
                
                # Record action
                self.record_copilot_action("social_learning", {
                    "github_trends": len(github_trends),
                    "youtube_trends": len(youtube_trends)
                })
                
                return {"github": github_trends, "youtube": youtube_trends}
                
            except Exception as e:
                logger.error(f"Social learning failed: {e}")
                self.metrics["errors_encountered"] += 1
        
        return {}
    
    def improve_existing_code(self):
        """Identify and improve existing code"""
        logger.info("⚡ Improving existing code...")
        
        improvements = []
        py_files = list(WORKSPACE.glob("*.py"))[:10]  # Top-level Python files
        
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # Simple improvements detection
                issues = []
                if "print(" in code and "logging" not in code:
                    issues.append("Consider using logging instead of print")
                if "except:" in code:
                    issues.append("Avoid bare except clauses")
                if len(code.splitlines()) > 500:
                    issues.append("Large file - consider splitting")
                
                if issues:
                    improvements.append({
                        "file": py_file.name,
                        "issues": issues
                    })
                    
            except Exception as e:
                logger.warning(f"Failed to check {py_file.name}: {e}")
        
        logger.info(f"  Found {len(improvements)} files with improvement opportunities")
        
        # Record action
        self.record_copilot_action("code_improvement", {
            "files_checked": len(py_files),
            "improvements_found": len(improvements)
        })
        
        return improvements
    
    def run_iteration(self, iteration_num: int):
        """Run one iteration of the orchestration loop"""
        logger.info(f"\n{'='*70}")
        logger.info(f"🔄 Iteration {iteration_num}")
        logger.info(f"{'='*70}")
        
        remaining = (self.end_time - datetime.now()).total_seconds() / 60
        logger.info(f"⏱️  Time remaining: {remaining:.1f} minutes")
        
        # Rotate tasks
        tasks = [
            ("analyze_workspace", self.analyze_workspace),
            ("learn_code", self.learn_from_existing_code),
            ("track_trends", self.track_social_trends),
            ("improve_code", self.improve_existing_code),
        ]
        
        # Execute task based on iteration
        task_name, task_func = tasks[iteration_num % len(tasks)]
        
        try:
            logger.info(f"📋 Executing: {task_name}")
            result = task_func()
            self.metrics["total_tasks_completed"] += 1
            logger.info(f"✅ Task completed: {task_name}")
        except Exception as e:
            logger.error(f"❌ Task failed: {e}")
            self.metrics["errors_encountered"] += 1
        
        # Update collaboration engine
        if self.collaboration_engine:
            self.collaboration_engine.iterate()
        
        # Save metrics
        self.save_metrics()
    
    def save_metrics(self):
        """Save session metrics"""
        metrics_file = DATA_DIR / "orchestrator_metrics.json"
        self.metrics["last_updated"] = datetime.now().isoformat()
        
        try:
            with open(metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")
    
    def print_statistics(self):
        """Print session statistics"""
        duration = (datetime.now() - self.start_time).total_seconds() / 60
        
        print(f"\n{'='*70}")
        print("📊 SESSION STATISTICS")
        print(f"{'='*70}")
        print(f"Duration: {duration:.1f} minutes")
        print(f"Tasks completed: {self.metrics['total_tasks_completed']}")
        print(f"Files analyzed: {self.metrics['code_files_analyzed']}")
        print(f"Knowledge learned: {self.metrics['knowledge_items_learned']}")
        print(f"Copilot actions: {self.metrics['copilot_actions_processed']}")
        print(f"Social trends: {self.metrics['social_trends_tracked']}")
        print(f"Errors: {self.metrics['errors_encountered']}")
        print(f"{'='*70}\n")
    
    def run(self):
        """Main orchestration loop"""
        logger.info("🚀 Starting Master Orchestrator")
        logger.info(f"⏱️  Session duration: {self.session_duration} hours")
        
        self.initialize_systems()
        
        iteration = 0
        try:
            while datetime.now() < self.end_time:
                iteration += 1
                self.run_iteration(iteration)
                
                # Print stats every 5 iterations
                if iteration % 5 == 0:
                    self.print_statistics()
                
                # Sleep between iterations
                time.sleep(60)  # 1 minute intervals
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Session interrupted by user")
        
        # Final statistics
        logger.info("\n🏁 SESSION COMPLETE")
        self.print_statistics()
        
        # Save final metrics
        self.save_metrics()
        logger.info(f"✅ Metrics saved to: {DATA_DIR / 'orchestrator_metrics.json'}")


def main():
    """Main entry point"""
    print("🎯 NEXUS-ONE Master Orchestrator")
    print("=" * 70)
    print("🤝 GitHub Copilot + NEXUS-ONE Collaborative Session")
    print("=" * 70)
    
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description="NEXUS-ONE Master Orchestrator")
    parser.add_argument("--hours", type=float, default=3.0, help="Session duration in hours")
    args = parser.parse_args()
    
    # Create and run orchestrator
    orchestrator = MasterOrchestrator(session_duration_hours=args.hours)
    orchestrator.run()


if __name__ == "__main__":
    main()
