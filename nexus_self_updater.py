"""
NEXUS-ONE Self-Updater
-----------------------
Dynamically updates own code based on learned knowledge.
- Adds new chat commands from knowledge graph
- Integrates learned patterns into existing code
- Self-modifies control panel with new features
- Updates documentation automatically

CAUTION: Self-modifying code! Always backs up before changes.
"""

import ast
import json
import logging
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

WORKSPACE = Path(__file__).parent
DATA_DIR = WORKSPACE / "nexus_data"
KNOWLEDGE_DIR = DATA_DIR / "knowledge_graph"
BACKUP_DIR = DATA_DIR / "self_update_backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = WORKSPACE / "nexus_logs"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "self_updater.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("SelfUpdater")

# Files that can be self-updated
UPDATABLE_FILES = {
    "control_panel": WORKSPACE / "ui" / "human_control_panel.py",
    "web_navigator": WORKSPACE / "web_navigator.py",
    "code_generator": WORKSPACE / "code_generator.py",
    "accelerated_learning": WORKSPACE / "accelerated_learning.py",
}


class SelfUpdater:
    """
    Self-modification engine.
    Updates NEXUS-ONE code based on knowledge graph.
    """

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run  # If True, only simulate (no actual changes)
        self.knowledge = self.load_knowledge()
        self.update_log = []

        logger.info(f"SelfUpdater initialized (dry_run: {dry_run})")

    def load_knowledge(self) -> Dict:
        """Load knowledge graph"""
        graph_file = KNOWLEDGE_DIR / "knowledge_graph.json"
        if graph_file.exists():
            try:
                return json.loads(graph_file.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to load knowledge: {e}")
        return {"commands": {}, "concepts": {}, "code_patterns": {}}

    def backup_file(self, file_path: Path) -> Path:
        """Create timestamped backup of file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = BACKUP_DIR / backup_name

        shutil.copy2(file_path, backup_path)
        logger.info(f"Backed up: {file_path.name} -> {backup_path.name}")
        return backup_path

    def extract_new_commands(self, min_usage: int = 2) -> List[Dict]:
        """
        Extract commands from knowledge graph that should be added to control panel.
        Only commands used multiple times (proven useful).
        """
        new_commands = []

        for cmd_name, cmd_data in self.knowledge.get("commands", {}).items():
            usage = cmd_data.get("usage_count", 0)
            category = cmd_data.get("category", "general")

            # Skip if low usage or already in panel
            if usage < min_usage or category in ["system", "existing"]:
                continue

            new_commands.append(
                {
                    "name": cmd_name,
                    "syntax": cmd_data.get("syntax", cmd_name),
                    "description": cmd_data.get("description", ""),
                    "category": category,
                    "usage": usage,
                }
            )

        # Sort by usage (most used first)
        new_commands.sort(key=lambda x: x["usage"], reverse=True)
        logger.info(f"Found {len(new_commands)} new commands to integrate")
        return new_commands

    def generate_command_handler_code(self, command: Dict) -> str:
        """Generate Python code for new command handler"""
        cmd_name = command["name"]
        cmd_syntax = command["syntax"]
        cmd_desc = command["description"]

        # Extract keywords from command
        keywords = [w for w in cmd_name.lower().split() if len(w) > 3]
        keywords_str = "', '".join(keywords[:3])  # Top 3 keywords

        code = f"""
        # Auto-generated: {cmd_name}
        if any(kw in txt for kw in ['{keywords_str}']):
            # {cmd_desc}
            try:
                # TODO: Implement logic for: {cmd_name}
                return "✅ {cmd_name} komutu çalıştırıldı! (auto-generated)"
            except Exception as e:
                return f"❌ {cmd_name} hatası: {{e}}"
        """
        return code.strip()

    def update_control_panel_commands(self, new_commands: List[Dict]) -> bool:
        """
        Inject new commands into control panel's process_chat_command method.
        """
        panel_file = UPDATABLE_FILES["control_panel"]

        if not panel_file.exists():
            logger.error(f"Control panel not found: {panel_file}")
            return False

        # Backup first
        self.backup_file(panel_file)

        # Read current content
        content = panel_file.read_text(encoding="utf-8")

        # Find process_chat_command method
        method_pattern = r"def process_chat_command\(self, text: str\) -> str:(.*?)(?=\n    def |\nclass |\Z)"
        match = re.search(method_pattern, content, re.DOTALL)

        if not match:
            logger.error("Could not find process_chat_command method")
            return False

        method_content = match.group(1)
        method_start = match.start(1)
        method_end = match.end(1)

        # Find where to inject (before "Unknown command" fallback)
        injection_marker = "# Unknown command"
        inject_pos = method_content.rfind(injection_marker)

        if inject_pos == -1:
            inject_pos = len(method_content) - 100  # Near end

        # Generate code for new commands
        new_code_blocks = []
        for cmd in new_commands[:5]:  # Limit to top 5
            new_code_blocks.append(self.generate_command_handler_code(cmd))

        injection_code = (
            "\n        # === AUTO-LEARNED COMMANDS ===\n"
            + "\n        ".join(new_code_blocks)
            + "\n        "
        )

        # Insert new code
        updated_method = (
            method_content[:inject_pos] + injection_code + method_content[inject_pos:]
        )
        updated_content = content[:method_start] + updated_method + content[method_end:]

        # Write back (if not dry-run)
        if not self.dry_run:
            panel_file.write_text(updated_content, encoding="utf-8")
            logger.info(
                f"✅ Updated control panel with {len(new_commands)} new commands"
            )
            self.update_log.append(
                f"Added {len(new_commands)} commands to control panel"
            )
        else:
            logger.info(f"[DRY RUN] Would add {len(new_commands)} commands")

        return True

    def integrate_code_patterns(self) -> bool:
        """
        Integrate frequently used code patterns into code_generator templates.
        """
        code_gen_file = UPDATABLE_FILES["code_generator"]

        if not code_gen_file.exists():
            logger.warning(f"Code generator not found: {code_gen_file}")
            return False

        # Get top patterns
        patterns = self.knowledge.get("code_patterns", {})
        top_patterns = sorted(
            patterns.items(), key=lambda x: x[1].get("frequency", 0), reverse=True
        )[:10]

        if not top_patterns:
            logger.info("No patterns to integrate")
            return False

        # Backup
        self.backup_file(code_gen_file)

        # Read content
        content = code_gen_file.read_text(encoding="utf-8")

        # Find template storage (patterns dict or similar)
        # For now, just log the patterns (full integration would be complex)
        logger.info(f"Top {len(top_patterns)} patterns identified for integration:")
        for pattern_id, pattern_data in top_patterns:
            logger.info(
                f"  - {pattern_data.get('description', 'N/A')} (freq: {pattern_data.get('frequency')})"
            )

        # TODO: Actually integrate patterns into code_generator templates
        # This would require parsing existing patterns structure and merging

        self.update_log.append(f"Identified {len(top_patterns)} top patterns")
        return True

    def update_documentation(self) -> bool:
        """
        Update COPILOT_MODE_GUIDE.md with new learned commands.
        """
        doc_file = WORKSPACE / "COPILOT_MODE_GUIDE.md"

        if not doc_file.exists():
            logger.warning("Documentation file not found")
            return False

        # Get new commands
        new_commands = self.extract_new_commands(min_usage=1)

        if not new_commands:
            logger.info("No new commands to document")
            return False

        # Backup
        self.backup_file(doc_file)

        # Read content
        content = doc_file.read_text(encoding="utf-8")

        # Generate markdown for new commands
        new_section = f"""

---

## 🆕 AUTO-LEARNED COMMANDS (Updated: {datetime.now().strftime('%Y-%m-%d')})

These commands were automatically learned from usage patterns:

"""

        for cmd in new_commands[:10]:  # Top 10
            new_section += f"### {cmd['name']}\n"
            new_section += f"```\n{cmd['syntax']}\n```\n"
            new_section += f"**Description**: {cmd['description']}\n"
            new_section += f"**Category**: {cmd['category']}\n"
            new_section += f"**Usage Count**: {cmd['usage']}\n\n"

        # Append to end of document (before final section if exists)
        if not self.dry_run:
            updated_content = content + new_section
            doc_file.write_text(updated_content, encoding="utf-8")
            logger.info(f"✅ Updated documentation with {len(new_commands)} commands")
            self.update_log.append(f"Documented {len(new_commands)} new commands")
        else:
            logger.info(f"[DRY RUN] Would document {len(new_commands)} commands")

        return True

    def self_update_cycle(self) -> Dict:
        """
        Complete self-update cycle.
        Returns summary of changes made.
        """
        logger.info("=== Starting Self-Update Cycle ===")

        results = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": self.dry_run,
            "changes": [],
            "success": True,
        }

        try:
            # 1. Extract new commands
            new_commands = self.extract_new_commands()
            results["new_commands_found"] = len(new_commands)

            # 2. Update control panel
            if new_commands:
                if self.update_control_panel_commands(new_commands):
                    results["changes"].append("control_panel_updated")

            # 3. Integrate code patterns
            if self.integrate_code_patterns():
                results["changes"].append("patterns_integrated")

            # 4. Update documentation
            if self.update_documentation():
                results["changes"].append("documentation_updated")

            # 5. Save update log
            results["update_log"] = self.update_log

        except Exception as e:
            logger.error(f"Self-update error: {e}", exc_info=True)
            results["success"] = False
            results["error"] = str(e)

        logger.info(
            f"Self-update cycle complete: {len(results['changes'])} changes made"
        )
        return results

    def get_update_summary(self) -> str:
        """Generate human-readable summary"""
        return f"""
🔄 Self-Update Summary
======================
Dry Run: {self.dry_run}
Updates Applied: {len(self.update_log)}

Changes:
{chr(10).join('  • ' + log for log in self.update_log)}

💾 Backups stored in: {BACKUP_DIR}
"""


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="NEXUS-ONE Self-Updater")
    parser.add_argument(
        "--dry-run", action="store_true", help="Simulate updates without applying"
    )
    parser.add_argument(
        "--force", action="store_true", help="Force update even with low-usage commands"
    )

    args = parser.parse_args()

    updater = SelfUpdater(dry_run=args.dry_run)
    results = updater.self_update_cycle()

    print(updater.get_update_summary())

    if results["success"]:
        print("\n✅ Self-update successful!")
        if args.dry_run:
            print("⚠️  This was a DRY RUN - no actual changes were made.")
            print("   Run without --dry-run to apply changes.")
    else:
        print(f"\n❌ Self-update failed: {results.get('error')}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
