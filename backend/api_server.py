"""
backend/api_server.py - GERÇEK API SERVER
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Çalışma dizinini kök dizine ekle
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.ai_orchestrator import AIOrchestrator
from backend.auth_manager import AuthManager
from backend.cluster_ready import ClusterManager
from backend.database_manager import DatabaseManager
from backend.enterprise_features import EnterpriseManager
from backend.nexus_core import NexusCore
from backend.system_monitor import SystemMonitor
from modules.backup_manager import BackupManager

# AUTH API entegrasyonu
from aetheros_live.backend.auth_api import router as auth_router

# Uygulama
app = FastAPI(
    # Auth API router'ını ekle
    app.include_router(auth_router, prefix="/api/auth")
    title="AETHEROS API",
    description="Autonomous System Management Platform",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
nexus_core = None
backup_manager = None
system_monitor = None

# Models
class BackupRequest(BaseModel):
    name: Optional[str] = None
    incremental: bool = False
    paths: Optional[List[str]] = None

class RestoreRequest(BaseModel):
    backup_name: str
    restore_path: Optional[str] = None
    verify: bool = True

class ModuleControl(BaseModel):
    module: str
    action: str  # start, stop, restart

class CommandRequest(BaseModel):
    command: str
    params: Optional[Dict[str, Any]] = None

# Startup event
@app.on_event("startup")
async def startup_event():
    """Uygulama başlangıcında çalışır"""
    global nexus_core, backup_manager, system_monitor
    
    logging.info("🚀 Starting AETHEROS API Server...")
    
    try:
        # Nexus Core'u başlat
        nexus_core = NexusCore("config/nexus_config.json")
        nexus_core.start()
        
        # Modülleri al
        if "backup_manager" in nexus_core.modules:
            backup_manager = nexus_core.modules["backup_manager"]
        
        if "system_monitor" in nexus_core.modules:
            system_monitor = nexus_core.modules["system_monitor"]
        
        logging.info("✅ AETHEROS API Server started successfully")
        
    except Exception as e:
        logging.error(f"❌ Startup failed: {e}")
        raise

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Uygulama kapanışında çalışır"""
    logging.info("🛑 Shutting down AETHEROS API Server...")
    
    if nexus_core:
        nexus_core.shutdown()
    
    logging.info("✅ AETHEROS API Server stopped")

# Health check
@app.get("/", response_class=HTMLResponse)
async def root():
    """Ana sayfa"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AETHEROS Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #0f172a; color: white; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; }
            .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .card { background: #1e293b; padding: 20px; border-radius: 10px; }
            .card h3 { color: #60a5fa; margin-top: 0; }
            .status { display: inline-block; padding: 5px 10px; border-radius: 5px; }
            .running { background: #10b981; }
            .stopped { background: #ef4444; }
            .btn { display: inline-block; padding: 10px 20px; background: #3b82f6; color: white; 
                   text-decoration: none; border-radius: 5px; margin: 5px; }
            .btn:hover { background: #2563eb; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 AETHEROS Dashboard</h1>
                <p>Autonomous System Management Platform</p>
                <div class="status running">🟢 System Running</div>
            </div>
            
            <div class="cards">
                <div class="card">
                    <h3>📊 System Status</h3>
                    <p>Check system health and metrics</p>
                    <a href="/api/health" class="btn">Health Check</a>
                    <a href="/api/system/status" class="btn">System Status</a>
                </div>
                
                <div class="card">
                    <h3>💾 Backup Management</h3>
                    <p>Manage backups and restores</p>
                    <a href="/api/backup/list" class="btn">List Backups</a>
                    <a href="/api/docs#/default/create_backup_api_backup_create_post" class="btn">Create Backup</a>
                </div>
                
                <div class="card">
                    <h3>📈 Monitoring</h3>
                    <p>Real-time system monitoring</p>
                    <a href="/api/system/metrics" class="btn">View Metrics</a>
                    <a href="/api/system/processes" class="btn">View Processes</a>
                </div>
                
                <div class="card">
                    <h3>🔧 API Documentation</h3>
                    <p>Full API documentation</p>
                    <a href="/api/docs" class="btn">Swagger UI</a>
                    <a href="/api/redoc" class="btn">ReDoc</a>
                </div>
            </div>
            
            <div style="margin-top: 40px; text-align: center;">
                <p>📚 <a href="/api/docs" style="color: #60a5fa;">API Documentation</a> | 
                   🐛 <a href="https://github.com/your-repo/issues" style="color: #60a5fa;">Report Issues</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Health endpoint
@app.get("/api/health")
async def health_check():
    """Sistem sağlık durumu"""
    return {
        "status": "healthy",
        "service": "AETHEROS API",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "nexus_core": "running" if nexus_core and nexus_core.is_running else "stopped",
            "backup_manager": "available" if backup_manager else "unavailable",
            "system_monitor": "available" if system_monitor else "unavailable"
        }
    }

# System status
@app.get("/api/system/status")
async def get_system_status():
    """Sistem durumunu getir"""
    if not nexus_core:
        raise HTTPException(status_code=503, detail="Nexus Core not available")
    
    status = nexus_core.get_system_status()
    return {"success": True, "data": status}

# Backup endpoints
@app.post("/api/backup/create")
async def create_backup(request: BackupRequest, background_tasks: BackgroundTasks):
    """Yeni backup oluştur"""
    if not backup_manager:
        raise HTTPException(status_code=503, detail="Backup Manager not available")
    
    try:
        def run_backup():
            backup_manager.create_backup(
                source_path=request.paths[0] if request.paths else "data",
                name=request.name,
                backup_type="incremental" if request.incremental else "full"
            )
        background_tasks.add_task(run_backup)
        return {
            "success": True,
            "message": "Backup process started in background. You can check backup list for status."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/backup/list")
async def list_backups(limit: int = 20):
    """Backup listesini getir"""
    if not backup_manager:
        raise HTTPException(status_code=503, detail="Backup Manager not available")
    
    try:
        backups = backup_manager.get_backup_list(limit=limit)
        return {"success": True, "data": backups, "count": len(backups)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/backup/restore")
async def restore_backup(request: RestoreRequest):
    """Backup'tan geri yükle"""
    if not backup_manager:
        raise HTTPException(status_code=503, detail="Backup Manager not available")
    
    try:
        def run_restore():
            backup_manager.restore_backup(
                backup_name=request.backup_name,
                restore_path=request.restore_path
            )
        background_tasks = BackgroundTasks()
        background_tasks.add_task(run_restore)
        return {
            "success": True,
            "message": "Restore process started in background. You can check target directory for result."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# System monitoring endpoints
@app.get("/api/system/metrics")
async def get_system_metrics():
    """Sistem metriklerini getir"""
    if not system_monitor:
        raise HTTPException(status_code=503, detail="System Monitor not available")
    
    try:
        summary = system_monitor.get_summary()
        return {"success": True, "data": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/system/processes")
async def get_top_processes(limit: int = 10):
    """En çok kaynak kullanan process'leri getir"""
    if not system_monitor:
        raise HTTPException(status_code=503, detail="System Monitor not available")
    
    try:
        processes = system_monitor.get_top_processes(count=limit)
        return {"success": True, "data": processes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/system/alerts")
async def get_system_alerts():
    """Sistem alert'larını getir"""
    if not system_monitor:
        raise HTTPException(status_code=503, detail="System Monitor not available")
    
    try:
        summary = system_monitor.get_summary()
        alerts = summary.get("active_alerts", [])
        return {"success": True, "data": alerts, "count": len(alerts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Module control
@app.post("/api/module/control")
async def control_module(control: ModuleControl):
    """Modül kontrolü"""
    if not nexus_core:
        raise HTTPException(status_code=503, detail="Nexus Core not available")
    
    try:
        if control.action == "start":
            success = nexus_core.start_module(control.module)
            message = f"Module {control.module} started" if success else f"Failed to start {control.module}"
        elif control.action == "stop":
            success = nexus_core.stop_module(control.module)
            message = f"Module {control.module} stopped" if success else f"Failed to stop {control.module}"
        elif control.action == "restart":
            nexus_core.stop_module(control.module)
            # Kısa bekle
            await asyncio.sleep(2)
            success = nexus_core.start_module(control.module)
            message = f"Module {control.module} restarted" if success else f"Failed to restart {control.module}"
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
        
        return {"success": success, "message": message}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Command execution
@app.post("/api/command")
async def execute_command(command: CommandRequest):
    """Komut çalıştır"""
    if not nexus_core:
        raise HTTPException(status_code=503, detail="Nexus Core not available")
    
    try:
        result = nexus_core.execute_command(
            command=command.command,
            params=command.params
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global error handler"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

# Main entry point
if __name__ == "__main__":
    # Logging setup
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/api_server.log'),
            logging.StreamHandler()
        ]
    )
    
    # Server'ı başlat
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
