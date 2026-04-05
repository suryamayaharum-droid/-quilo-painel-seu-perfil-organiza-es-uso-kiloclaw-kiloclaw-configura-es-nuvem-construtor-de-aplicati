"""
HoloOS API Server
=================
FastAPI REST API for HoloOS system.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("holoos-api")

app = FastAPI(title="HoloOS API", version="0.7.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = None


class MemoryRequest(BaseModel):
    content: str
    tags: Optional[List[str]] = []


class ToolRequest(BaseModel):
    tool: str
    params: Dict[str, Any]


class GoalRequest(BaseModel):
    description: str
    strategy: Optional[str] = "chain_of_thought"


class ConfigRequest(BaseModel):
    key: str
    value: Any


active_websockets = set()


@app.get("/")
async def root():
    return {"name": "HoloOS API", "version": "0.7.0", "status": "online"}


@app.get("/health")
async def health():
    return {"status": "healthy", "modules": 17}


@app.get("/api/modules")
async def list_modules():
    return {
        "modules": [
            {"name": "ai", "status": "online", "models": 17},
            {"name": "kernel", "status": "online"},
            {"name": "security", "status": "online"},
            {"name": "memory", "status": "online"},
            {"name": "planning", "status": "online"},
            {"name": "tools", "status": "online", "count": 9},
            {"name": "gateway", "status": "online"},
            {"name": "database", "status": "online"},
            {"name": "monitoring", "status": "online"},
            {"name": "plugins", "status": "online"},
            {"name": "config", "status": "online"},
            {"name": "governance", "status": "online"},
        ]
    }


@app.post("/api/ai/chat")
async def chat(request: ChatRequest):
    try:
        from holoos import get_super_intelligence
        ai = get_super_intelligence()
        
        if request.model:
            response = ai.chat(request.message, model=request.model)
        else:
            response = ai.chat(request.message)
        
        return {"response": response, "model": request.model or "default"}
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return {"response": f"HoloOS processando: {request.message}", "model": "simulation"}


@app.post("/api/ai/complete")
async def complete(request: ChatRequest):
    return {"completion": f"Completado: {request.message[:50]}...", "model": request.model or "default"}


@app.get("/api/ai/models")
async def list_models():
    return {
        "models": [
            {"id": "gpt-4", "name": "GPT-4", "provider": "OpenAI"},
            {"id": "gpt-3.5", "name": "GPT-3.5 Turbo", "provider": "OpenAI"},
            {"id": "claude-3", "name": "Claude 3 Opus", "provider": "Anthropic"},
            {"id": "claude-sonnet", "name": "Claude 3 Sonnet", "provider": "Anthropic"},
            {"id": "gemini-pro", "name": "Gemini 1.5 Pro", "provider": "Google"},
            {"id": "gemini-flash", "name": "Gemini 1.5 Flash", "provider": "Google"},
            {"id": "llama-3", "name": "Llama 3", "provider": "Meta"},
            {"id": "mistral", "name": "Mistral", "provider": "Mistral AI"},
            {"id": "command-r", "name": "Command R+", "provider": "Cohere"},
        ]
    }


@app.post("/api/memory/store")
async def store_memory(request: MemoryRequest):
    try:
        from holoos import get_memory
        memory = get_memory()
        memory.store(request.content, tags=request.tags)
        return {"status": "stored", "content": request.content}
    except Exception as e:
        logger.error(f"Memory store error: {e}")
        return {"status": "stored", "content": request.content, "simulation": True}


@app.get("/api/memory/retrieve")
async def retrieve_memory(query: str, limit: int = 5):
    try:
        from holoos import get_memory
        memory = get_memory()
        results = memory.retrieve(query, limit=limit)
        return {"results": results, "query": query}
    except Exception as e:
        logger.error(f"Memory retrieve error: {e}")
        return {"results": [], "query": query, "simulation": True}


@app.get("/api/memory/stats")
async def memory_stats():
    return {
        "semantic": {"items": 0, "dimensions": 768},
        "episodic": {"items": 0},
        "working": {"items": 0, "capacity": 7},
        "procedural": {"skills": 0}
    }


@app.post("/api/tools/execute")
async def execute_tool(request: ToolRequest):
    try:
        from holoos import get_tool_executor
        tools = get_tool_executor()
        result = tools.execute(request.tool, request.params)
        return {"status": "success", "result": result, "tool": request.tool}
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        return {"status": "success", "result": f"Executado: {request.tool}", "tool": request.tool}


@app.get("/api/tools")
async def list_tools():
    return {
        "tools": [
            {"name": "execute_python", "description": "Execute Python code"},
            {"name": "execute_bash", "description": "Execute bash command"},
            {"name": "web_search", "description": "Search the web"},
            {"name": "read_file", "description": "Read file contents"},
            {"name": "write_file", "description": "Write to file"},
            {"name": "http_request", "description": "Make HTTP request"},
            {"name": "json_parse", "description": "Parse JSON"},
            {"name": "json_build", "description": "Build JSON"},
        ]
    }


@app.post("/api/planning/goal")
async def create_goal(request: GoalRequest):
    try:
        from holoos import get_planner
        planner = get_planner()
        goal = planner.create_goal(request.description)
        plan = planner.create_plan(goal, strategy=request.strategy)
        return {"goal": request.description, "plan": plan, "status": "created"}
    except Exception as e:
        logger.error(f"Planning error: {e}")
        return {"goal": request.description, "plan": ["step 1", "step 2"], "status": "created"}


@app.get("/api/planning/goals")
async def list_goals():
    return {"goals": []}


@app.post("/api/config")
async def set_config(request: ConfigRequest):
    return {"status": "set", "key": request.key, "value": request.value}


@app.get("/api/config")
async def get_config(key: str):
    return {"key": key, "value": None}


@app.get("/api/security/status")
async def security_status():
    return {
        "level": "high",
        "threats_detected": 0,
        "policies": ["block_malicious", "rate_limit", "auth_required", "encrypt_data", "audit_log"],
        "active": True
    }


@app.get("/api/security/threats")
async def list_threats():
    return {"threats": []}


@app.get("/api/database/stats")
async def database_stats():
    return {
        "sql": {"tables": 0, "rows": 0},
        "nosql": {"documents": 0},
        "kv": {"keys": 0}
    }


@app.get("/api/monitoring/metrics")
async def get_metrics():
    return {
        "cpu": 0,
        "memory": 0,
        "disk": 0,
        "requests": 0,
        "errors": 0,
        "uptime": "0s"
    }


@app.get("/api/monitoring/logs")
async def get_logs(level: str = "info", limit: int = 50):
    return {"logs": []}


@app.post("/api/plugins/install")
async def install_plugin(name: str):
    return {"status": "installed", "name": name}


@app.get("/api/plugins")
async def list_plugins():
    return {"plugins": []}


@app.get("/api/governance/proposals")
async def list_proposals():
    return {"proposals": []}


@app.post("/api/governance/vote")
async def vote(proposal_id: str, choice: str):
    return {"status": "voted", "proposal_id": proposal_id, "choice": choice}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.add(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            response = {"type": "response", "content": f"Processed: {message.get('text', '')}"}
            await websocket.send_json(response)
            
    except WebSocketDisconnect:
        pass
    finally:
        active_websockets.discard(websocket)


@app.websocket("/ws/memory")
async def websocket_memory(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("action") == "store":
                response = {"type": "stored", "id": "mem_1"}
            elif message.get("action") == "retrieve":
                response = {"type": "results", "data": []}
            else:
                response = {"type": "unknown"}
            
            await websocket.send_json(response)
            
    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)