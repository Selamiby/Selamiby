"""
Seviye 3: İLERİ OTONOM SİSTEMLER
Görev Zinciri Oluşturma - Kompleks işleri parçalara bölme, bağımlılık yönetimi, paralel işlem
"""

import json
import threading
import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from queue import Queue
from typing import Any, Callable, Dict, List, Optional


class TaskStatus(Enum):
    """Görev durumu"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class Task:
    """Tek görev"""

    def __init__(
        self,
        task_id: str,
        name: str,
        action: Callable,
        dependencies: Optional[List[str]] = None,
        priority: int = 0,
    ):
        self.id = task_id
        self.name = name
        self.action = action
        self.dependencies = dependencies or []
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.start_time = None
        self.end_time = None

    def execute(self, context: Optional[Dict] = None) -> Dict:
        """Görevi çalıştır"""
        self.status = TaskStatus.RUNNING
        self.start_time = datetime.now()

        try:
            result = self.action(context or {})
            self.result = result
            self.status = TaskStatus.COMPLETED
            return {"success": True, "result": result}
        except Exception as e:
            self.error = str(e)
            self.status = TaskStatus.FAILED
            return {"success": False, "error": str(e)}
        finally:
            self.end_time = datetime.now()

    def to_dict(self) -> Dict:
        """Görevü sözlüğe dönüştür"""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "priority": self.priority,
            "result": self.result,
            "error": self.error,
            "duration": (
                (self.end_time - self.start_time).total_seconds()
                if self.end_time and self.start_time
                else None
            ),
        }


class WorkflowEngine:
    """Görev akış motoru"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.workflows: Dict[str, Dict] = {}

    def add_task(
        self,
        task_id: str,
        name: str,
        action: Callable,
        dependencies: Optional[List[str]] = None,
        priority: int = 0,
    ) -> Dict:
        """Görev ekle"""
        if task_id in self.tasks:
            return {"error": f"Task {task_id} already exists"}

        task = Task(task_id, name, action, dependencies, priority)
        self.tasks[task_id] = task

        return {"success": True, "task_id": task_id, "name": name}

    def create_workflow(self, workflow_id: str, description: str = "") -> Dict:
        """Akış oluştur"""
        self.workflows[workflow_id] = {
            "id": workflow_id,
            "description": description,
            "tasks": [],
            "status": "created",
            "created_at": datetime.now().isoformat(),
        }

        return {"success": True, "workflow_id": workflow_id}

    def add_tasks_to_workflow(self, workflow_id: str, task_ids: List[str]) -> Dict:
        """Akışa görevler ekle"""
        if workflow_id not in self.workflows:
            return {"error": f"Workflow {workflow_id} not found"}

        self.workflows[workflow_id]["tasks"] = task_ids

        return {"success": True, "added": len(task_ids)}

    def execute_workflow(self, workflow_id: str, parallel: bool = False) -> Dict:
        """Akışı çalıştır"""
        if workflow_id not in self.workflows:
            return {"error": f"Workflow {workflow_id} not found"}

        workflow = self.workflows[workflow_id]
        task_ids = workflow["tasks"]

        results = {
            "workflow_id": workflow_id,
            "status": "running",
            "tasks": {},
            "started_at": datetime.now().isoformat(),
        }

        if parallel:
            results = self._execute_parallel(task_ids, results)
        else:
            results = self._execute_sequential(task_ids, results)

        results["completed_at"] = datetime.now().isoformat()
        workflow["status"] = "completed"

        return results

    def execute_with_dependencies(self, workflow_id: str) -> Dict:
        """Bağımlılıkları göz önüne alarak çalıştır"""
        if workflow_id not in self.workflows:
            return {"error": f"Workflow {workflow_id} not found"}

        workflow = self.workflows[workflow_id]
        task_ids = workflow["tasks"]

        # Bağımlılık sırasını oluştur
        execution_order = self._get_execution_order(task_ids)

        results = {
            "workflow_id": workflow_id,
            "status": "running",
            "tasks": {},
            "execution_order": execution_order,
            "started_at": datetime.now().isoformat(),
        }

        context = {}

        for task_id in execution_order:
            if task_id not in self.tasks:
                continue

            task = self.tasks[task_id]

            # Bağımlılıklar tamamlandı mı?
            if not self._check_dependencies_completed(task.dependencies, results):
                task.status = TaskStatus.SKIPPED
                results["tasks"][task_id] = {
                    "status": "skipped",
                    "reason": "Dependencies failed",
                }
                continue

            # Görevi çalıştır
            result = task.execute(context)
            context[task_id] = result.get("result")
            results["tasks"][task_id] = task.to_dict()

        results["completed_at"] = datetime.now().isoformat()
        workflow["status"] = "completed"

        return results

    def _execute_sequential(self, task_ids: List[str], results: Dict) -> Dict:
        """Sırayla çalıştır"""
        context = {}

        for task_id in task_ids:
            if task_id not in self.tasks:
                continue

            task = self.tasks[task_id]
            result = task.execute(context)
            context[task_id] = result.get("result")
            results["tasks"][task_id] = task.to_dict()

        return results

    def _execute_parallel(self, task_ids: List[str], results: Dict) -> Dict:
        """Paralel çalıştır"""
        threads = []
        context = {}
        lock = threading.Lock()

        def task_wrapper(task_id):
            if task_id not in self.tasks:
                return

            task = self.tasks[task_id]
            result = task.execute(context)

            with lock:
                context[task_id] = result.get("result")
                results["tasks"][task_id] = task.to_dict()

        for task_id in task_ids:
            thread = threading.Thread(target=task_wrapper, args=(task_id,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results

    def _get_execution_order(self, task_ids: List[str]) -> List[str]:
        """Bağımlılıklara göre çalıştırma sırası belirle"""
        order = []
        visited = set()
        visiting = set()

        def visit(task_id):
            if task_id in visited:
                return
            if task_id in visiting:
                # Döngü tespit
                return

            visiting.add(task_id)

            task = self.tasks.get(task_id)
            if task:
                for dep in task.dependencies:
                    if dep in self.tasks:
                        visit(dep)

            visiting.remove(task_id)
            visited.add(task_id)
            order.append(task_id)

        for task_id in task_ids:
            visit(task_id)

        return order

    def _check_dependencies_completed(
        self, dependencies: List[str], results: Dict
    ) -> bool:
        """Bağımlılıklar tamamlandı mı"""
        for dep in dependencies:
            if dep not in results["tasks"]:
                return False

            task_result = results["tasks"][dep]
            if task_result.get("status") == TaskStatus.FAILED.value:
                return False

        return True

    def get_workflow_status(self, workflow_id: str) -> Dict:
        """Akış durumunu al"""
        if workflow_id not in self.workflows:
            return {"error": f"Workflow {workflow_id} not found"}

        workflow = self.workflows[workflow_id]

        return {
            "workflow_id": workflow_id,
            "status": workflow["status"],
            "task_count": len(workflow["tasks"]),
            "created_at": workflow["created_at"],
        }


class TaskBuilder:
    """Görev oluşturucu"""

    @staticmethod
    def create_file_task(task_id: str, file_path: str, content: str) -> Callable:
        """Dosya oluşturma görev"""

        def action(context):
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w") as f:
                f.write(content)
            return {"file": file_path, "size": len(content)}

        return action

    @staticmethod
    def create_process_task(task_id: str, processor: Callable) -> Callable:
        """Veri işleme görev"""

        def action(context):
            return processor(context)

        return action

    @staticmethod
    def create_check_task(task_id: str, condition: Callable) -> Callable:
        """Kontrol görev"""

        def action(context):
            return {"check_passed": condition(context)}

        return action


# Global instance
workflow_engine = WorkflowEngine()
