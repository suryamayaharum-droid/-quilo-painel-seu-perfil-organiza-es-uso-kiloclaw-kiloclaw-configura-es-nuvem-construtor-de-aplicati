"""
HoloOS Observability Integration
================================
Langfuse-like tracing and monitoring for AI operations.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import time
import uuid
import json


@dataclass
class Trace:
    id: str
    name: str
    start_time: float
    end_time: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    spans: List["Span"] = field(default_factory=list)


@dataclass
class Span:
    id: str
    trace_id: str
    parent_id: Optional[str]
    name: str
    start_time: float
    end_time: Optional[float] = None
    status: str = "success"
    input: Optional[str] = None
    output: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    model: Optional[str] = None
    tokens_used: Optional[int] = None
    cost: Optional[float] = None


@dataclass
class Generation:
    id: str
    trace_id: str
    model: str
    prompt: str
    completion: str
    tokens: int
    cost: float
    latency: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class Feedback:
    id: str
    trace_id: str
    score: float
    comment: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


class ObservabilityClient:
    def __init__(self, project_name: str = "holoos"):
        self.project_name = project_name
        self.traces: Dict[str, Trace] = {}
        self.generations: List[Generation] = []
        self.feedbacks: List[Feedback] = []
        self.current_trace: Optional[Trace] = None
    
    def create_trace(self, name: str, metadata: Dict[str, Any] = None) -> Trace:
        trace = Trace(
            id=str(uuid.uuid4()),
            name=name,
            start_time=time.time(),
            metadata=metadata or {}
        )
        self.traces[trace.id] = trace
        self.current_trace = trace
        return trace
    
    def start_span(
        self,
        name: str,
        trace_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        metadata: Dict[str, Any] = None
    ) -> Span:
        span = Span(
            id=str(uuid.uuid4()),
            trace_id=trace_id or (self.current_trace.id if self.current_trace else ""),
            parent_id=parent_id,
            name=name,
            start_time=time.time(),
            metadata=metadata or {}
        )
        
        if span.trace_id and span.trace_id in self.traces:
            self.traces[span.trace_id].spans.append(span)
        
        return span
    
    def end_span(self, span: Span, status: str = "success", output: str = None):
        span.end_time = time.time()
        span.status = status
        span.output = output
    
    def log_generation(
        self,
        trace_id: str,
        model: str,
        prompt: str,
        completion: str,
        tokens: int,
        cost: float,
        latency: float
    ):
        generation = Generation(
            id=str(uuid.uuid4()),
            trace_id=trace_id,
            model=model,
            prompt=prompt,
            completion=completion,
            tokens=tokens,
            cost=cost,
            latency=latency
        )
        self.generations.append(generation)
    
    def add_feedback(self, trace_id: str, score: float, comment: str = None):
        feedback = Feedback(
            id=str(uuid.uuid4()),
            trace_id=trace_id,
            score=score,
            comment=comment
        )
        self.feedbacks.append(feedback)
    
    def get_trace(self, trace_id: str) -> Optional[Trace]:
        return self.traces.get(trace_id)
    
    def get_traces(self, limit: int = 50) -> List[Trace]:
        return list(self.traces.values())[-limit:]
    
    def get_generations(self, limit: int = 50) -> List[Generation]:
        return self.generations[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        total_cost = sum(g.cost for g in self.generations)
        total_tokens = sum(g.tokens for g in self.generations)
        avg_latency = sum(g.latency for g in self.generations) / max(len(self.generations), 1)
        
        model_usage = {}
        for g in self.generations:
            model_usage[g.model] = model_usage.get(g.model, 0) + 1
        
        return {
            "project": self.project_name,
            "total_traces": len(self.traces),
            "total_generations": len(self.generations),
            "total_cost": round(total_cost, 4),
            "total_tokens": total_tokens,
            "average_latency": round(avg_latency, 3),
            "model_usage": model_usage,
            "feedback_count": len(self.feedbacks)
        }
    
    def export_json(self) -> str:
        return json.dumps({
            "traces": [
                {
                    "id": t.id,
                    "name": t.name,
                    "start_time": t.start_time,
                    "end_time": t.end_time,
                    "metadata": t.metadata,
                    "span_count": len(t.spans)
                }
                for t in self.traces.values()
            ],
            "generations": [
                {
                    "id": g.id,
                    "trace_id": g.trace_id,
                    "model": g.model,
                    "tokens": g.tokens,
                    "cost": g.cost,
                    "latency": g.latency
                }
                for g in self.generations
            ]
        }, indent=2)


class LangfuseClient(ObservabilityClient):
    """Alias for compatibility with Langfuse"""
    pass


class PhoenixClient(ObservabilityClient):
    """Alias for compatibility with Phoenix"""
    pass


_observability = ObservabilityClient()


def get_observability() -> ObservabilityClient:
    return _observability


def trace(name: str, metadata: Dict[str, Any] = None):
    """Decorator for automatic tracing"""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            client = get_observability()
            trace_obj = client.create_trace(name, metadata)
            span = client.start_span(func.__name__, trace_id=trace_obj.id)
            
            try:
                result = func(*args, **kwargs)
                client.end_span(span, "success")
                return result
            except Exception as e:
                client.end_span(span, "error", str(e))
                raise
        
        return wrapper
    return decorator


__all__ = [
    "ObservabilityClient",
    "LangfuseClient",
    "PhoenixClient",
    "Trace",
    "Span",
    "Generation",
    "Feedback",
    "get_observability",
    "trace"
]