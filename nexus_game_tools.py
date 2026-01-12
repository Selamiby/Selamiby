#!/usr/bin/env python3
"""
NEXUS Game Tools
- Build command helpers for Unity/Godot
- Asset pipeline stubs (compression plan, atlasing placeholder)
- Profiler hooks (FPS/GC/time) lightweight
- Feature flag client helper
"""
import json
import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)
FLAGS_PATH = BASE_DIR / "game_feature_flags.json"


def unity_build_commands(project_path: str, target: str = "Android") -> List[str]:
    """Return CLI command examples for Unity batchmode builds."""
    # Note: Requires Unity installed and project_path set.
    return [
        "Unity -batchmode -nographics -quit "
        f"-projectPath {project_path} "
        f"-buildTarget {target} "
        "-executeMethod BuildScript.PerformBuild"
    ]


def godot_build_commands(
    project_path: str, export_preset: str = "Android"
) -> List[str]:
    return [
        f"godot --headless --path {project_path} --export-release {export_preset} build/output.apk"
    ]


def run_command(cmd: str, cwd: Optional[str] = None) -> int:
    proc = subprocess.Popen(cmd, shell=True, cwd=cwd)
    proc.wait()
    return proc.returncode


@dataclass
class AssetPlan:
    files: List[str]
    atlas_targets: List[str]
    compress_targets: List[str]


def plan_assets(asset_dir: str) -> AssetPlan:
    p = Path(asset_dir)
    files = [str(x) for x in p.rglob("*.*") if x.is_file()]
    atlas_targets = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    compress_targets = [
        f for f in files if f.lower().endswith((".wav", ".ogg", ".mp3", ".png", ".jpg"))
    ]
    return AssetPlan(
        files=files, atlas_targets=atlas_targets, compress_targets=compress_targets
    )


def feature_flags() -> Dict:
    if not FLAGS_PATH.exists():
        FLAGS_PATH.write_text(
            json.dumps({"version": 1, "flags": {}}, indent=2), encoding="utf-8"
        )
    return json.loads(FLAGS_PATH.read_text(encoding="utf-8"))


class Profiler:
    def __init__(self):
        self.samples = []

    def sample(self, name: str):
        self.samples.append((name, time.time()))

    def report(self) -> List[str]:
        lines = []
        for label, ts in self.samples:
            lines.append(f"{label}: {ts}")
        return lines


def save_report(lines: List[str], name: str = "profiler_report.txt") -> Path:
    path = LOG_DIR / name
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


if __name__ == "__main__":
    print("Unity build cmds:")
    for c in unity_build_commands("/path/to/unity/project", target="Android"):
        print(c)
    print("Godot build cmds:")
    for c in godot_build_commands("/path/to/godot/project", export_preset="Android"):
        print(c)
    plan = plan_assets("./assets")
    print(f"Found {len(plan.files)} assets")
