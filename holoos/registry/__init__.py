"""
HoloOS Model Registry
=====================
Model management and versioning system.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json


class ModelStatus(Enum):
    DRAFT = "draft"
    REGISTERED = "registered"
    DEPLOYED = "deployed"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


@dataclass
class ModelVersion:
    version: str
    created_at: datetime
    description: str
    framework: str
    metrics: Dict[str, float] = field(default_factory=dict)
    artifacts: Dict[str, str] = field(default_factory=dict)


@dataclass
class RegisteredModel:
    name: str
    description: str
    task_type: str
    provider: str
    status: ModelStatus
    current_version: str
    versions: List[ModelVersion] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class ModelRegistry:
    def __init__(self):
        self.models: Dict[str, RegisteredModel] = {}
        self._deployments: Dict[str, Dict[str, Any]] = {}
        self._aliases: Dict[str, str] = {}
    
    def register_model(
        self,
        name: str,
        description: str,
        task_type: str,
        provider: str,
        version: str,
        framework: str,
        metadata: Dict[str, Any] = None,
        tags: List[str] = None
    ) -> RegisteredModel:
        if name in self.models:
            model = self.models[name]
            model.status = ModelStatus.REGISTERED
            model.updated_at = datetime.now()
        else:
            model = RegisteredModel(
                name=name,
                description=description,
                task_type=task_type,
                provider=provider,
                status=ModelStatus.REGISTERED,
                current_version=version,
                metadata=metadata or {},
                tags=tags or []
            )
            self.models[name] = model
        
        model_version = ModelVersion(
            version=version,
            created_at=datetime.now(),
            description=f"Version {version}",
            framework=framework
        )
        model.versions.append(model_version)
        model.current_version = version
        
        return model
    
    def get_model(self, name: str) -> Optional[RegisteredModel]:
        if name in self._aliases:
            name = self._aliases[name]
        return self.models.get(name)
    
    def list_models(
        self,
        task_type: str = None,
        provider: str = None,
        status: ModelStatus = None,
        tags: List[str] = None
    ) -> List[RegisteredModel]:
        results = list(self.models.values())
        
        if task_type:
            results = [m for m in results if m.task_type == task_type]
        if provider:
            results = [m for m in results if m.provider == provider]
        if status:
            results = [m for m in results if m.status == status]
        if tags:
            results = [m for m in results if any(t in m.tags for t in tags)]
        
        return results
    
    def deploy_model(self, name: str, version: str = None, environment: str = "production") -> Dict[str, Any]:
        model = self.get_model(name)
        if not model:
            raise ValueError(f"Model {name} not found")
        
        version = version or model.current_version
        
        deployment = {
            "model": name,
            "version": version,
            "environment": environment,
            "deployed_at": datetime.now().isoformat(),
            "status": "deployed"
        }
        
        key = f"{name}:{environment}"
        self._deployments[key] = deployment
        
        model.status = ModelStatus.DEPLOYED
        model.updated_at = datetime.now()
        
        return deployment
    
    def get_deployment(self, name: str, environment: str = "production") -> Optional[Dict[str, Any]]:
        key = f"{name}:{environment}"
        return self._deployments.get(key)
    
    def list_deployments(self, environment: str = None) -> List[Dict[str, Any]]:
        if environment:
            return [d for d in self._deployments.values() if d["environment"] == environment]
        return list(self._deployments.values())
    
    def create_alias(self, alias: str, model_name: str, version: str = None):
        model = self.get_model(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        
        self._aliases[alias] = model_name
        
        if version:
            self._deployments[f"{alias}:production"] = {
                "model": model_name,
                "version": version,
                "environment": "production",
                "alias": alias,
                "deployed_at": datetime.now().isoformat()
            }
    
    def deprecate_model(self, name: str, replacement: str = None):
        model = self.get_model(name)
        if model:
            model.status = ModelStatus.DEPRECATED
            model.metadata["replacement"] = replacement
            model.updated_at = datetime.now()
    
    def archive_model(self, name: str):
        model = self.get_model(name)
        if model:
            model.status = ModelStatus.ARCHIVED
            model.updated_at = datetime.now()
    
    def get_stats(self) -> Dict[str, Any]:
        by_status = {}
        by_provider = {}
        by_task = {}
        
        for model in self.models.values():
            by_status[model.status.value] = by_status.get(model.status.value, 0) + 1
            by_provider[model.provider] = by_provider.get(model.provider, 0) + 1
            by_task[model.task_type] = by_task.get(model.task_type, 0) + 1
        
        return {
            "total_models": len(self.models),
            "total_deployments": len(self._deployments),
            "total_aliases": len(self._aliases),
            "by_status": by_status,
            "by_provider": by_provider,
            "by_task_type": by_task
        }
    
    def export_registry(self) -> str:
        return json.dumps({
            "models": [
                {
                    "name": m.name,
                    "description": m.description,
                    "task_type": m.task_type,
                    "provider": m.provider,
                    "status": m.status.value,
                    "current_version": m.current_version,
                    "versions": [{"version": v.version, "framework": v.framework} for v in m.versions],
                    "tags": m.tags
                }
                for m in self.models.values()
            ],
            "deployments": self._deployments,
            "aliases": self._aliases
        }, indent=2)


_model_registry = ModelRegistry()


def get_model_registry() -> ModelRegistry:
    return _model_registry


__all__ = [
    "ModelRegistry",
    "RegisteredModel",
    "ModelVersion",
    "ModelStatus",
    "get_model_registry"
]