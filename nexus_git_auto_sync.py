#!/usr/bin/env python3
"""
AUTONOMOUS GIT SYNC & COMMIT LOOP
==================================
Runs continuously - automatically commits all changes
NEXUS-ONE controls, COPILOT executes - NO USER QUESTIONS
"""

import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).parent
LOG_DIR = WORKSPACE / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] GIT-AUTO - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "git_auto_commit.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("GitAutoCommit")


class AutonomousGitSync:
    """Automatically sync and commit - NEXUS controls"""

    def __init__(self):
        self.commit_count = 0
        logger.info("🔄 AUTONOMOUS GIT SYNC STARTED - ZERO QUESTIONS MODE")
        logger.info("Will auto-commit every 60 seconds with ALL changes")

    def run_loop(self, duration_minutes=300):
        """Run commit loop for duration (default 5 hours)"""
        start = time.time()
        end_time = start + (duration_minutes * 60)

        while time.time() < end_time:
            try:
                # Add all changes
                result = subprocess.run(
                    ["git", "add", "."], cwd=WORKSPACE, capture_output=True, text=True
                )

                if result.returncode != 0:
                    logger.warning(f"Git add failed: {result.stderr}")
                else:
                    logger.info("✅ Git add completed")

                # Check for changes
                status_result = subprocess.run(
                    ["git", "status", "--short"],
                    cwd=WORKSPACE,
                    capture_output=True,
                    text=True,
                )

                changes_count = (
                    len(status_result.stdout.strip().split("\n"))
                    if status_result.stdout.strip()
                    else 0
                )

                if changes_count > 0:
                    self.commit_count += 1
                    commit_msg = f"Auto Commit #{self.commit_count}: NEXUS autonomous development ({changes_count} files)"

                    # Commit automatically
                    commit_result = subprocess.run(
                        ["git", "commit", "-m", commit_msg],
                        cwd=WORKSPACE,
                        capture_output=True,
                        text=True,
                    )

                    if commit_result.returncode == 0:
                        logger.info(
                            f"✅ COMMIT #{self.commit_count}: {changes_count} files committed"
                        )
                    else:
                        logger.debug(f"Git commit result: {commit_result.stdout}")
                else:
                    logger.info("⏭️  No changes to commit")

                # Wait 60 seconds before next commit
                logger.info(
                    f"⏳ Waiting 60 seconds... (Total commits: {self.commit_count})"
                )
                time.sleep(60)

            except Exception as e:
                logger.error(f"❌ Error in commit loop: {e}")
                time.sleep(60)

        logger.info(f"✅ GIT SYNC COMPLETE - Total commits: {self.commit_count}")


if __name__ == "__main__":
    sync = AutonomousGitSync()
    sync.run_loop(duration_minutes=300)  # 5 hours
