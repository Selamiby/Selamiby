"""
Task Management from Auto-GPT
"""
import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Task:
    id: str
    name: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)
    result: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
class TaskManager:
    """Otonom görev yöneticisi"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_queue = asyncio.Queue()
        self.is_running = False
        self.worker_task = None
        
    def create_task(self, name: str, description: str, **kwargs) -> str:
        """Yeni görev oluştur"""
        task_id = str(uuid.uuid4())[:8]
        
        task = Task(
            id=task_id,
            name=name,
            description=description,
            **kwargs
        )
        
        self.tasks[task_id] = task
        return task_id
    
    async def execute_task(self, task: Task) -> Any:
        """Görevi yürüt (template method)"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        
        try:
            # Görev tipine göre yürütme
            if "dosya" in task.description.lower():
                result = await self._execute_file_task(task)
            elif "web" in task.description.lower():
                result = await self._execute_web_task(task)
            elif "analiz" in task.description.lower():
                result = await self._execute_analysis_task(task)
            else:
                result = await self._execute_general_task(task)
                
            task.status = TaskStatus.COMPLETED
            task.result = result
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            raise
            
        finally:
            task.completed_at = datetime.now()
            
        return task.result
    
    async def _execute_file_task(self, task: Task) -> Dict:
        """Dosya görevini yürüt"""
        return {
            "type": "file_operation",
            "task": task.name,
            "status": "completed",
            "details": "File operation executed"
        }
    
    async def _execute_web_task(self, task: Task) -> Dict:
        """Web görevini yürüt"""
        return {
            "type": "web_operation",
            "task": task.name,
            "status": "completed",
            "details": "Web operation executed"
        }
    
    async def _execute_analysis_task(self, task: Task) -> Dict:
        """Analiz görevini yürüt"""
        return {
            "type": "analysis",
            "task": task.name,
            "status": "completed",
            "details": "Analysis completed"
        }
    
    async def _execute_general_task(self, task: Task) -> Dict:
        """Genel görevi yürüt"""
        return {
            "type": "general",
            "task": task.name,
            "status": "completed",
            "details": "Task executed successfully"
        }
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Görevi getir"""
        return self.tasks.get(task_id)
    
    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """Görevleri listele"""
        if status:
            return [task for task in self.tasks.values() if task.status == status]
        return list(self.tasks.values())
    
    async def run_worker(self):
        """Görev çalıştırıcı"""
        self.is_running = True
        
        while self.is_running:
            try:
                task_id = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                
                task = self.tasks.get(task_id)
                if task and task.status == TaskStatus.PENDING:
                    await self.execute_task(task)
                    
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Worker error: {e}")
                
    def start(self):
        """Çalıştırıcıyı başlat"""
        if not self.is_running:
            self.worker_task = asyncio.create_task(self.run_worker())
            
    def stop(self):
        """Çalıştırıcıyı durdur"""
        self.is_running = False
        if self.worker_task:
            self.worker_task.cancel()
