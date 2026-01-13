import logging
import multiprocessing as mp
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

import psutil
from config.config import get_config, setup_directories

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
        
        # 1. Start Safeguards First (Resource Guard)
        self.start_subsystem("ResourceGuard", "nexus_resource_guard.py")
        time.sleep(2) # Give it time to stabilize

        # 2. Start Learning Engine (Infinite Learner)
        self.start_subsystem("LearningEngine", "nexus_infinite_learner.py")

        # 3. Start Evolution Engine (Continuous Improver)
        self.start_subsystem("EvolutionEngine", "nexus_continuous_improver.py")

        # 4. Start Health/Sync (Auto Healer & Git Sync)
        # Note: Auto Healer can be periodic, merged into Improver or started separate
        self.start_subsystem("AutoHealer", "nexus_auto_healer.py")

        logger.info("🌟 ALL SYSTEMS REAL & AUTONOMOUS. Nexus-One is now fully independent.")
        
        try:
            while True:
                # Core monitoring loop
                cpu = psutil.cpu_percent(interval=5)
                active_count = sum(1 for p in self.processes.values() if p.poll() is None)
                logger.info(f"💓 Core Heartbeat - Active Subsystems: {active_count}/{len(self.processes)} | CPU: {cpu}%")
                
                # If any critical system died, restart it
                for name, proc in self.processes.items():
                    if proc.poll() is not None:
                        logger.warning(f"⚠️ {name} has stopped. Restarting...")
                        if name == "ResourceGuard": self.start_subsystem(name, "nexus_resource_guard.py")
                        elif name == "LearningEngine": self.start_subsystem(name, "nexus_infinite_learner.py")
                        elif name == "EvolutionEngine": self.start_subsystem(name, "nexus_continuous_improver.py")
                
                time.sleep(60) # Central tick is slow to save CPU
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down Nexus-One Core...")
            for p in self.processes.values(): p.terminate()

if __name__ == "__main__":
    core = NexusOneCore()
    core.run()
