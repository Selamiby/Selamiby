import logging
import multiprocessing as mp
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

import psutil

from config.config import get_config, setup_directories
from nexus_brain import NexusBrain

# Setup logging
LOG_DIR = Path(__file__).parent / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] 🧠 NEXUS-CORE: %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "nexus_core.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("NexusCore")

class NexusOneCore:
    """
    Advanced Autonomous AI Core - Unified command center.
    Links Learning, Action, and Safeguards.
    """
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.processes = {}
        setup_directories()
        
        # Define all managed subsystems
        self.subsystems = {
            "ResourceGuard": "nexus_resource_guard.py",
            "LearningEngine": "nexus_infinite_learner.py",
            "EvolutionEngine": "nexus_continuous_improver.py",
            "AutoHealer": "nexus_auto_healer.py",
            "GitSync": "nexus_git_auto_sync.py",
            "APIServer": "nexus_api_server.py"
        }
        logger.info("🚀 NEXUS-ONE: Advanced Autonomous AI Core initialized.")

    def start_subsystem(self, name: str, script_name: str):
        """Starts a Nexus subsystem in the background."""
        script_path = self.workspace / script_name
        if not script_path.exists():
            logger.error(f"Missing subsystem: {script_name}")
            return

        logger.info(f"🔄 Starting {name}...")
        try:
            # Run using the same python interpreter
            proc = subprocess.Popen(
                [psutil.Process().exe(), str(script_path)],
                cwd=self.workspace,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            self.processes[name] = proc
            logger.info(f"✅ {name} resides in background (PID: {proc.pid})")
        except Exception as e:
            logger.error(f"Failed to start {name}: {e}")

    def run(self):
        """Orchestrates the entire autonomous cycle."""
        logger.info("✨ NEXUS-ONE is evolving to Advanced Autonomy...")
        
        # Initial launch of all systems
        for name, script in self.subsystems.items():
            self.start_subsystem(name, script)
            time.sleep(3) # Increased staggered launch to avoid race conditions

        logger.info("🌟 ALL SYSTEMS REAL & AUTONOMOUS. Nexus-One is now fully independent.")
        
        try:
            while True:
                # Core monitoring loop
                cpu = psutil.cpu_percent(interval=5)
                active_count = sum(1 for p in self.processes.values() if p.poll() is None)
                knowledge_count = len(list(self.workspace.glob("infinite_knowledge/*.json")))
                
                # Dynamic Activity Message
                if active_count == len(self.subsystems):
                    status_emoji = "🟢 FULL ACTIVE"
                else:
                    status_emoji = f"🟡 {active_count}/{len(self.subsystems)} ACTIVE"

                logger.info(f"💓 Heartbeat: {status_emoji} | 📚 Knowledge Base: {knowledge_count} Topics | ⚡ CPU: {cpu}%")
                
                # If any system died, restart it
                for name, proc in self.processes.items():
                    if proc.poll() is not None:
                        exit_code = proc.poll()
                        logger.warning(f"⚠️ {name} has stopped (Exit Code: {exit_code}). Restarting...")
                        self.start_subsystem(name, self.subsystems[name])
                
                time.sleep(30) # Tick every 30 seconds
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down Nexus-One Core...")
            for p in self.processes.values(): p.terminate()

if __name__ == "__main__":
    core = NexusOneCore()
    core.run()
