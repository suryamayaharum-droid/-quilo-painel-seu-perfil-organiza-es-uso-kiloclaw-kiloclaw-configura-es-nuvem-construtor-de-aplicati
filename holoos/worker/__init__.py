"""
HoloOS Background Worker
=========================
Async task processing (Celery-like).
"""

import asyncio
import logging
from typing import Dict, Any, Callable
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("holoos-worker")


class Task:
    def __init__(self, task_id: str, func: Callable, args: tuple = (), kwargs: dict = None):
        self.task_id = task_id
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.status = "pending"
        self.result = None
        self.error = None
        self.created_at = datetime.now()
        self.completed_at = None


class Worker:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.running = False
    
    def submit(self, task_id: str, func: Callable, *args, **kwargs) -> Task:
        task = Task(task_id, func, args, kwargs)
        self.tasks[task_id] = task
        logger.info(f"Task {task_id} submitted")
        return task
    
    async def execute_task(self, task_id: str):
        task = self.tasks.get(task_id)
        if not task:
            return
        
        task.status = "running"
        logger.info(f"Executing task {task_id}")
        
        try:
            if asyncio.iscoroutinefunction(task.func):
                task.result = await task.func(*task.args, **task.kwargs)
            else:
                task.result = task.func(*task.args, **task.kwargs)
            task.status = "completed"
            task.completed_at = datetime.now()
            logger.info(f"Task {task_id} completed")
        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            task.completed_at = datetime.now()
            logger.error(f"Task {task_id} failed: {e}")
    
    async def run(self):
        self.running = True
        logger.info("Worker started")
        
        while self.running:
            pending = [t for t in self.tasks.values() if t.status == "pending"]
            
            for task in pending:
                asyncio.create_task(self.execute_task(task.task_id))
            
            await asyncio.sleep(0.5)
    
    def stop(self):
        self.running = False
        logger.info("Worker stopped")
    
    def get_task(self, task_id: str) -> Task:
        return self.tasks.get(task_id)


# Predefined task types
async def process_ai_request(task_data: Dict[str, Any]):
    await asyncio.sleep(1)
    return {"response": f"Processed: {task_data.get('message', '')}"}


async def process_memory_task(task_data: Dict[str, Any]):
    await asyncio.sleep(0.5)
    return {"stored": True}


async def process_tool_execution(task_data: Dict[str, Any]):
    await asyncio.sleep(0.5)
    return {"executed": True}


# Run worker
if __name__ == "__main__":
    worker = Worker()
    
    # Submit some test tasks
    worker.submit("ai_1", process_ai_request, {"message": "Hello"})
    worker.submit("mem_1", process_memory_task, {"content": "Test"})
    worker.submit("tool_1", process_tool_execution, {"tool": "echo"})
    
    asyncio.run(worker.run())