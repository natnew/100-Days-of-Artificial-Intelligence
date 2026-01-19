
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Task:
    id: str
    content: str
    assigned_to: Optional[str] = None
    status: str = "pending" # pending, in_progress, completed, failed, escalated

class WorkerAgent:
    def __init__(self, name: str, capability: str):
        self.name = name
        self.capability = capability

    def execute(self, task: Task) -> str:
        """
        Simulates task execution.
        Fails if task content contains 'hard'.
        """
        if "hard" in task.content.lower():
            task.status = "escalated"
            return f"{self.name}: Task too hard, escalating."
        
        task.status = "completed"
        return f"{self.name}: Completed '{task.content}'."

class SupervisorAgent:
    def __init__(self, workers: List[WorkerAgent]):
        self.workers = {w.name: w for w in workers}
        self.task_log: List[Task] = []

    def assign_task(self, task: Task) -> str:
        """
        Assigns task to a worker based on simple logic (round robin or capability).
        For simplicity, assigns to first available or handles escalation.
        """
        self.task_log.append(task)
        
        # Simple assignment logic
        target_worker_name = task.assigned_to
        if not target_worker_name:
             # Default to first worker
             target_worker_name = list(self.workers.keys())[0]

        worker = self.workers.get(target_worker_name)
        if not worker:
            return "Error: Worker not found."
            
        print(f"[Supervisor] Assigning task '{task.id}' to {worker.name}")
        result = worker.execute(task)
        
        if task.status == "escalated":
            return self.handle_escalation(task, worker.name)
            
        return result

    def handle_escalation(self, task: Task, worker_name: str) -> str:
        print(f"[Supervisor] Handling escalation for task '{task.id}' from {worker_name}")
        # Supervisor logic: Retry with different worker, or do it themself
        # Here we simulate 'Supervisor Override'
        task.status = "completed"
        return f"[Supervisor] Override: Completed escalation of '{task.content}' manually."
