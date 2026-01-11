#!/usr/bin/env python3
"""
NEXUS-ONE Defensive Security Agent (Windows only)
- Monitors processes and network connections (psutil)
- Learns patterns and optionally auto-blocks via Windows Firewall
- Integrates with Windows Defender for updates and quick scans
- Performs safe cleanup of temp directories (excludes workspace)

This agent is defensive-only. It does not perform any offensive actions.
"""
import os
import sys
import json
import time
import shutil
import subprocess
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
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}\n"
    try:
        LOG_DIR.mkdir(exist_ok=True)
        with SEC_LOG.open('a', encoding='utf-8') as f:
            f.write(line)
    except Exception:
        pass

def load_config():
    default = {
        "exclude_paths": [str(WORKSPACE)],
        "auto_block": True,
        "learning_mode": True,
        "cleanup_enabled": True,
        "cleanup_paths": [os.environ.get('TEMP', ''), r"C:\\Windows\\Temp"],
        "cleanup_max_age_days": 7,
        "firewall_blocklist": [],
        "log_level": "info",
    }
    try:
        if CONFIG_FILE.exists():
            cfg = json.loads(CONFIG_FILE.read_text(encoding='utf-8'))
            default.update(cfg)
    except Exception as e:
        log(f"config_load_error: {e}")
    return default

CFG = load_config()
EXCLUDES = {Path(p).resolve() for p in CFG.get('exclude_paths', []) if p}

# --- Windows utilities ---
POWERSHELL = "powershell"

def run_ps(cmd: str) -> tuple[int, str]:
    try:
        p = subprocess.run([POWERSHELL, '-ExecutionPolicy', 'Bypass', '-NoProfile', '-Command', cmd], capture_output=True, text=True)
        out = (p.stdout or '') + (p.stderr or '')
        return p.returncode, out.strip()
    except Exception as e:
        return 1, str(e)

def defender_update_and_quick_scan():
    if sys.platform != 'win32':
        return
    log("defender_update_start")
    rc, out = run_ps('Update-MpSignature')
    log(f"defender_update_rc={rc} out={out[:500]}")
    log("defender_quickscan_start")
    rc, out = run_ps('Start-MpScan -ScanType QuickScan')
    log(f"defender_quickscan_rc={rc} out={out[:500]}")
    rc, out = run_ps('Get-MpThreat | Select-Object ThreatName,SeverityID,ActionSuccess | ConvertTo-Json')
    if rc == 0 and out:
        log(f"defender_threats={out}")

def firewall_block_ip(ip: str, name: str | None = None):
    if sys.platform != 'win32':
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
    if not CFG.get('cleanup_enabled', True):
        return
    cutoff = datetime.now() - timedelta(days=max_age_days)
    cleaned = 0
    for raw in CFG.get('cleanup_paths', []):
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

# --- Monitoring ---

def suspicious_connection(conn) -> str | None:
    try:
        raddr = getattr(conn, 'raddr', None)
        laddr = getattr(conn, 'laddr', None)
        status = getattr(conn, 'status', '')
        if not raddr or not getattr(raddr, 'ip', None):
            return None
        ip = raddr.ip
        # Simple heuristic: external IP on uncommon ports or many TIME_WAIT
        if raddr and raddr.port not in {80, 443, 53} and status in {'ESTABLISHED', 'SYN_SENT'}:
            return ip
    except Exception:
        return None
    return None

KNOWN_SAFE_DIRS = [
    Path(os.environ.get('ProgramFiles', 'C:/Program Files')),
    Path(os.environ.get('ProgramFiles(x86)', 'C:/Program Files (x86)')),
    Path('C:/Windows'),
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
            if sys.platform == 'win32' and now - last_defender > 6 * 3600:
                defender_update_and_quick_scan()
                last_defender = now

            # Cleanup once per hour
            if int(now) % 3600 < 5:
                cleanup_temp(CFG.get('cleanup_max_age_days', 7))

            # Process + net checks
            for p in psutil.process_iter(['pid', 'name']):
                pid = p.info.get('pid')
                name = p.info.get('name') or ''
                # Check connections
                suspicious_ips = set()
                try:
                    for c in p.connections(kind='inet'):
                        ip = suspicious_connection(c)
                        if ip:
                            suspicious_ips.add(ip)
                except Exception:
                    pass

                if suspicious_ips:
                    sp = ",".join(sorted(list(suspicious_ips)))
                    log(f"proc_suspicious pid={pid} name={name} ips={sp}")
                    if CFG.get('auto_block', True):
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

if __name__ == '__main__':
    if sys.platform != 'win32':
        print("Windows only")
        sys.exit(0)
    monitor_loop()
