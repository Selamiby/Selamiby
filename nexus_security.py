import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:16
🚀 Status: ACTIVE / PRODUCTION
"""

#!/usr/bin/env python3
"""
NEXUS-ONE Defensive Security Agent (Windows only)
- Monitors processes and network connections (psutil)
- Learns patterns and optionally auto-blocks via Windows Firewall
- Integrates with Windows Defender for updates and quick scans
- Performs safe cleanup of temp directories (excludes workspace)

This agent is defensive-only. It does not perform any offensive actions.
"""
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    import psutil
except Exception:
    psutil = None

WORKSPACE = Path.cwd()
DATA_DIR = WORKSPACE / "nexus_data"
LOG_DIR = WORKSPACE / "nexus_logs"
SEC_LOG = LOG_DIR / "security.log"
CONFIG_FILE = DATA_DIR / "security_config.json"


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    try:
        LOG_DIR.mkdir(exist_ok=True)
        with SEC_LOG.open("a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


def load_config():
    default = {
        "exclude_paths": [str(WORKSPACE)],
        "auto_block": True,
        "learning_mode": True,
        "cleanup_enabled": True,
        "cleanup_paths": [os.environ.get("TEMP", ""), r"C:\\Windows\\Temp"],
        "cleanup_max_age_days": 7,
        "extended_cleanup_enabled": False,
        "browser_cache_cleanup": False,
        "prefetch_cleanup": False,
        "recycle_bin_cleanup": False,
        "firewall_blocklist": [],
        "learned_threats": [],
        "log_level": "info",
    }
    try:
        if CONFIG_FILE.exists():
            cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            default.update(cfg)
    except Exception as e:
        log(f"config_load_error: {e}")
    return default


CFG = load_config()
EXCLUDES = {Path(p).resolve() for p in CFG.get("exclude_paths", []) if p}

# --- Windows utilities ---
POWERSHELL = "powershell"


def run_ps(cmd: str) -> tuple[int, str]:
    try:
        p = subprocess.run(
            [POWERSHELL, "-ExecutionPolicy", "Bypass", "-NoProfile", "-Command", cmd],
            capture_output=True,
            text=True,
        )
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode, out.strip()
    except Exception as e:
        return 1, str(e)


def defender_update_and_quick_scan():
    if sys.platform != "win32":
        return
    log("defender_update_start")
    rc, out = run_ps("Update-MpSignature")
    log(f"defender_update_rc={rc} out={out[:500]}")
    log("defender_quickscan_start")
    rc, out = run_ps("Start-MpScan -ScanType QuickScan")
    log(f"defender_quickscan_rc={rc} out={out[:500]}")
    rc, out = run_ps(
        "Get-MpThreat | Select-Object ThreatName,SeverityID,ActionSuccess | ConvertTo-Json"
    )
    if rc == 0 and out:
        log(f"defender_threats={out}")


def firewall_block_ip(ip: str, name: str | None = None):
    if sys.platform != "win32":
        return False
    rule_name = name or f"NEXUS_BLOCK_{ip}"
    cmd = f"New-NetFirewallRule -DisplayName '{rule_name}' -Direction Outbound -RemoteAddress {ip} -Action Block -Profile Any"
    rc, out = run_ps(cmd)
    log(f"firewall_block_ip {ip} rc={rc} out={out[:500]}")
    return rc == 0


# --- Cleanup ---


def is_excluded(path: Path) -> bool:
    try:
        rp = path.resolve()
        for ex in EXCLUDES:
            try:
                if rp == ex or ex in rp.parents:
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False


def cleanup_temp(max_age_days: int):
    if not CFG.get("cleanup_enabled", True):
        return
    cutoff = datetime.now() - timedelta(days=max_age_days)
    cleaned = 0
    for raw in CFG.get("cleanup_paths", []):
        p_str = os.path.expandvars(raw)
        if not p_str:
            continue
        p = Path(p_str)
        if not p.exists():
            continue
        for root, dirs, files in os.walk(p):
            root_path = Path(root)
            if is_excluded(root_path):
                continue
            for f in files:
                fp = root_path / f
                try:
                    stat = fp.stat()
                    mtime = datetime.fromtimestamp(stat.st_mtime)
                    if mtime < cutoff:
                        fp.unlink(missing_ok=True)
                        cleaned += 1
                except Exception:
                    continue
    log(f"cleanup_temp_done count={cleaned}")


def cleanup_browser_cache():
    """Clean browser caches (Chrome, Edge, Firefox) - safe mode"""
    if not CFG.get("browser_cache_cleanup", False):
        return
    cleaned = 0
    user_profile = Path(os.environ.get("USERPROFILE", ""))
    if not user_profile.exists():
        return

    # Chrome/Edge cache
    cache_paths = [
        user_profile
        / "AppData"
        / "Local"
        / "Google"
        / "Chrome"
        / "User Data"
        / "Default"
        / "Cache",
        user_profile
        / "AppData"
        / "Local"
        / "Microsoft"
        / "Edge"
        / "User Data"
        / "Default"
        / "Cache",
        user_profile / "AppData" / "Local" / "Mozilla" / "Firefox" / "Profiles",
    ]
    cutoff = datetime.now() - timedelta(days=CFG.get("cleanup_max_age_days", 7))
    for cp in cache_paths:
        if not cp.exists() or is_excluded(cp):
            continue
        try:
            for root, dirs, files in os.walk(cp):
                for f in files:
                    fp = Path(root) / f
                    try:
                        if datetime.fromtimestamp(fp.stat().st_mtime) < cutoff:
                            fp.unlink(missing_ok=True)
                            cleaned += 1
                    except Exception:
                        continue
        except Exception:
            continue
    log(f"cleanup_browser_cache_done count={cleaned}")


def cleanup_prefetch():
    """Clean Windows Prefetch folder (requires admin)"""
    if not CFG.get("prefetch_cleanup", False):
        return
    prefetch_dir = Path("C:/Windows/Prefetch")
    if not prefetch_dir.exists():
        return
    cleaned = 0
    cutoff = datetime.now() - timedelta(days=CFG.get("cleanup_max_age_days", 7))
    try:
        for f in prefetch_dir.glob("*.pf"):
            try:
                if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
                    f.unlink(missing_ok=True)
                    cleaned += 1
            except Exception:
                continue
    except Exception:
        pass
    log(f"cleanup_prefetch_done count={cleaned}")


def cleanup_recycle_bin():
    """Empty Recycle Bin (PowerShell)"""
    if not CFG.get("recycle_bin_cleanup", False):
        return
    if sys.platform != "win32":
        return
    log("cleanup_recycle_bin_start")
    rc, out = run_ps("Clear-RecycleBin -Force -ErrorAction SilentlyContinue")
    log(f"cleanup_recycle_bin_rc={rc}")


def extended_cleanup():
    """Run all extended cleanup tasks"""
    if not CFG.get("extended_cleanup_enabled", False):
        return
    cleanup_browser_cache()
    cleanup_prefetch()
    cleanup_recycle_bin()


# --- Dynamic Learning ---


def learn_from_logs():
    """Analyze security logs and update threat patterns"""
    if not CFG.get("learning_mode", True):
        return
    if not SEC_LOG.exists():
        return

    try:
        recent_threats = CFG.get("learned_threats", [])
        text = SEC_LOG.read_text(encoding="utf-8")
        lines = text.splitlines()[-1000:]  # Last 1000 lines

        # Extract suspicious IPs from logs
        new_ips = set()
        for line in lines:
            if "proc_suspicious" in line and "ips=" in line:
                try:
                    ips_part = line.split("ips=")[1].strip()
                    for ip in ips_part.split(","):
                        ip = ip.strip()
                        if ip and ip not in recent_threats:
                            new_ips.add(ip)
                except Exception:
                    continue

        # Update config with learned threats
        if new_ips:
            recent_threats.extend(list(new_ips)[:50])  # Keep last 50
            recent_threats = recent_threats[-100:]  # Max 100
            CFG["learned_threats"] = recent_threats
            try:
                CONFIG_FILE.write_text(json.dumps(CFG, indent=2), encoding="utf-8")
                log(
                    f"learning_update threats_added={len(new_ips)} total={len(recent_threats)}"
                )
            except Exception as e:
                log(f"learning_error: {e}")
    except Exception as e:
        log(f"learn_from_logs_error: {e}")


# --- Monitoring ---


def suspicious_connection(conn) -> str | None:
    try:
        raddr = getattr(conn, "raddr", None)
        laddr = getattr(conn, "laddr", None)
        status = getattr(conn, "status", "")
        if not raddr or not getattr(raddr, "ip", None):
            return None
        ip = raddr.ip
        # Simple heuristic: external IP on uncommon ports or many TIME_WAIT
        if (
            raddr
            and raddr.port not in {80, 443, 53}
            and status in {"ESTABLISHED", "SYN_SENT"}
        ):
            return ip
    except Exception:
        return None
    return None


KNOWN_SAFE_DIRS = [
    Path(os.environ.get("ProgramFiles", "C:/Program Files")),
    Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")),
    Path("C:/Windows"),
]


def is_process_path_suspicious(p: psutil.Process) -> bool:
    try:
        exe = Path(p.exe())
        if any((sd in exe.parents) for sd in KNOWN_SAFE_DIRS):
            return False
        if is_excluded(exe):
            return False
        return True
    except Exception:
        return False


def monitor_loop():
    if not psutil:
        log("psutil_missing")
        return
    log("monitor_start")
    last_defender = 0.0
    while True:
        try:
            # Periodic Defender update/scan (every ~6h)
            now = time.time()
            if sys.platform == "win32" and now - last_defender > 6 * 3600:
                defender_update_and_quick_scan()
                last_defender = now

            # Cleanup once per hour
            if int(now) % 3600 < 5:
                cleanup_temp(CFG.get("cleanup_max_age_days", 7))
                extended_cleanup()

            # Learning every 30 min
            if int(now) % 1800 < 5:
                learn_from_logs()

            # Process + net checks
            for p in psutil.process_iter(["pid", "name"]):
                pid = p.info.get("pid")
                name = p.info.get("name") or ""
                # Check connections
                suspicious_ips = set()
                try:
                    for c in p.connections(kind="inet"):
                        ip = suspicious_connection(c)
                        if ip:
                            suspicious_ips.add(ip)
                except Exception:
                    pass

                if suspicious_ips:
                    sp = ",".join(sorted(list(suspicious_ips)))
                    log(f"proc_suspicious pid={pid} name={name} ips={sp}")
                    if CFG.get("auto_block", True):
                        for ip in suspicious_ips:
                            firewall_block_ip(ip)

                # Suspicious binary path outside system dirs
                if is_process_path_suspicious(p):
                    log(f"proc_path_suspicious pid={pid} name={name} exe={p.exe()}")

            time.sleep(5)
        except KeyboardInterrupt:
            log("monitor_stop_user")
            break
        except Exception as e:
            log(f"monitor_error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    if sys.platform != "win32":
        print("Windows only")
        sys.exit(0)
    monitor_loop()
