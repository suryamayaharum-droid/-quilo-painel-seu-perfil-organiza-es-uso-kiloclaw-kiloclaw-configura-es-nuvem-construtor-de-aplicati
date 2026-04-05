"""
HoloOS Python SDK
=================
"""

import requests
from typing import Optional, Dict, Any, List


class HoloOSClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def chat(self, message: str, model: Optional[str] = None) -> Dict[str, Any]:
        """Send a chat message"""
        response = requests.post(
            f"{self.base_url}/api/ai/chat",
            json={"message": message, "model": model}
        )
        return response.json()
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List available models"""
        response = requests.get(f"{self.base_url}/api/ai/models")
        return response.json().get("models", [])
    
    def store_memory(self, content: str, tags: List[str] = None) -> Dict[str, Any]:
        """Store in memory"""
        response = requests.post(
            f"{self.base_url}/api/memory/store",
            json={"content": content, "tags": tags or []}
        )
        return response.json()
    
    def retrieve_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve from memory"""
        response = requests.get(
            f"{self.base_url}/api/memory/retrieve",
            params={"query": query, "limit": limit}
        )
        return response.json().get("results", [])
    
    def execute_tool(self, tool: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool"""
        response = requests.post(
            f"{self.base_url}/api/tools/execute",
            json={"tool": tool, "params": params}
        )
        return response.json()
    
    def create_goal(self, description: str, strategy: str = "chain_of_thought") -> Dict[str, Any]:
        """Create a goal"""
        response = requests.post(
            f"{self.base_url}/api/planning/goal",
            json={"description": description, "strategy": strategy}
        )
        return response.json()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics"""
        response = requests.get(f"{self.base_url}/api/monitoring/metrics")
        return response.json()
    
    def security_status(self) -> Dict[str, Any]:
        """Get security status"""
        response = requests.get(f"{self.base_url}/api/security/status")
        return response.json()
    
    def list_modules(self) -> List[Dict[str, Any]]:
        """List all modules"""
        response = requests.get(f"{self.base_url}/api/modules")
        return response.json().get("modules", [])


__all__ = ["HoloOSClient"]