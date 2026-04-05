"""
HoloOS Agent Orchestration
==========================
Multi-agent collaboration system.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid
import asyncio


class AgentRole(Enum):
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    EXECUTOR = "executor"
    ANALYZER = "analyzer"
    PLANNER = "planner"


class AgentStatus(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    WAITING = "waiting"
    DONE = "done"


@dataclass
class Agent:
    id: str
    name: str
    role: AgentRole
    description: str
    capabilities: List[str]
    model: str = "gpt-4"
    status: AgentStatus = AgentStatus.IDLE
    memory: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_to_memory(self, entry: Dict[str, Any]):
        self.memory.append(entry)
        if len(self.memory) > 100:
            self.memory.pop(0)


@dataclass
class Task:
    id: str
    description: str
    assignee: Optional[str] = None
    status: str = "pending"
    result: Optional[Any] = None
    dependencies: List[str] = field(default_factory=list)


@dataclass
class AgentMessage:
    id: str
    from_agent: str
    to_agent: str
    content: str
    timestamp: float = field(default_factory=lambda: __import__("time").time())


class AgentTeam:
    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.messages: List[AgentMessage] = []
        self._create_default_agents()
    
    def _create_default_agents(self):
        default_agents = [
            Agent(
                id="coordinator",
                name="Coordinator",
                role=AgentRole.COORDINATOR,
                description="Coordinates team efforts and delegates tasks",
                capabilities=["task_planning", "delegation", "summary"]
            ),
            Agent(
                id="researcher",
                name="Researcher",
                role=AgentRole.RESEARCHER,
                description="Gathers information and analyzes data",
                capabilities=["web_search", "data_analysis", "knowledge_retrieval"]
            ),
            Agent(
                id="executor",
                name="Executor",
                role=AgentRole.EXECUTOR,
                description="Executes tasks and actions",
                capabilities=["code_execution", "file_operations", "tool_usage"]
            ),
            Agent(
                id="analyzer",
                name="Analyzer",
                role=AgentRole.ANALYZER,
                description="Analyzes results and provides insights",
                capabilities=["pattern_recognition", "metrics", "reporting"]
            ),
            Agent(
                id="planner",
                name="Planner",
                role=AgentRole.PLANNER,
                description="Creates plans and strategies",
                capabilities=["strategic_planning", "goal_setting", "risk_assessment"]
            ),
        ]
        
        for agent in default_agents:
            self.agents[agent.id] = agent
    
    def add_agent(self, agent: Agent):
        self.agents[agent.id] = agent
    
    def remove_agent(self, agent_id: str):
        if agent_id in self.agents:
            del self.agents[agent_id]
    
    def assign_task(self, task: Task, agent_id: str):
        task.assignee = agent_id
        self.tasks[task.id] = task
        
        if agent_id in self.agents:
            self.agents[agent_id].status = AgentStatus.THINKING
    
    def create_task(self, description: str, dependencies: List[str] = None) -> Task:
        task = Task(
            id=f"task_{uuid.uuid4().hex[:8]}",
            description=description,
            dependencies=dependencies or []
        )
        self.tasks[task.id] = task
        return task
    
    def send_message(self, from_id: str, to_id: str, content: str):
        message = AgentMessage(
            id=str(uuid.uuid4()),
            from_agent=from_id,
            to_agent=to_id,
            content=content
        )
        self.messages.append(message)
        
        if to_id in self.agents:
            self.agents[to_id].add_to_memory({"type": "message", "from": from_id, "content": content})
    
    async def execute_task(self, task_id: str) -> Dict[str, Any]:
        task = self.tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}
        
        agent_id = task.assignee
        if not agent_id or agent_id not in self.agents:
            return {"error": "No assignee for task"}
        
        agent = self.agents[agent_id]
        agent.status = AgentStatus.ACTING
        
        await asyncio.sleep(0.5)
        
        result = {
            "task_id": task_id,
            "agent": agent.name,
            "result": f"Completed: {task.description}",
            "status": "completed"
        }
        
        agent.status = AgentStatus.DONE
        task.status = "completed"
        task.result = result
        
        return result
    
    async def run_workflow(self, workflow: List[str]) -> List[Dict[str, Any]]:
        results = []
        
        for task_id in workflow:
            result = await self.execute_task(task_id)
            results.append(result)
            
            coordinator = self.agents.get("coordinator")
            if coordinator:
                coordinator.add_to_memory({"type": "task_completed", "task": task_id, "result": result})
        
        return results
    
    def get_team_status(self) -> Dict[str, Any]:
        return {
            "team_id": self.id,
            "team_name": self.name,
            "agents": [
                {
                    "id": a.id,
                    "name": a.name,
                    "role": a.role.value,
                    "status": a.status.value,
                    "capabilities": a.capabilities
                }
                for a in self.agents.values()
            ],
            "tasks": {
                "total": len(self.tasks),
                "completed": len([t for t in self.tasks.values() if t.status == "completed"]),
                "pending": len([t for t in self.tasks.values() if t.status == "pending"])
            }
        }


class Orchestrator:
    def __init__(self):
        self.teams: Dict[str, AgentTeam] = {}
    
    def create_team(self, name: str) -> AgentTeam:
        team = AgentTeam(name)
        self.teams[team.id] = team
        return team
    
    def get_team(self, team_id: str) -> Optional[AgentTeam]:
        return self.teams.get(team_id)
    
    def list_teams(self) -> List[Dict[str, Any]]:
        return [
            {"id": t.id, "name": t.name, "agents": len(t.agents)}
            for t in self.teams.values()
        ]


_orchestrator = Orchestrator()


def get_orchestrator() -> Orchestrator:
    return _orchestrator


__all__ = [
    "Agent",
    "AgentRole",
    "AgentStatus",
    "Task",
    "AgentMessage",
    "AgentTeam",
    "Orchestrator",
    "get_orchestrator"
]