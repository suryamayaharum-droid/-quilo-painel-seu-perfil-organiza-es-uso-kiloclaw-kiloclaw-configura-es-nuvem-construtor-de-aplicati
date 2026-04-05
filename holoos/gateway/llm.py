"""
HoloOS LLM Gateway
==================
Unified LLM access gateway with multiple providers.
"""

from typing import Dict, Any, List, Optional, AsyncGenerator
from dataclasses import dataclass
from enum import Enum
import asyncio
import time


class Provider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    META = "meta"
    MISTRAL = "mistral"
    COHERE = "cohere"
    LOCAL = "local"


@dataclass
class LLMConfig:
    provider: Provider
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


@dataclass
class LLMRequest:
    model: str
    messages: List[Dict[str, str]]
    temperature: float = 0.7
    max_tokens: int = 4096
    stream: bool = False
    tools: Optional[List[Dict[str, Any]]] = None


@dataclass
class LLMResponse:
    model: str
    content: str
    usage: Dict[str, int]
    finish_reason: str
    tool_calls: Optional[List[Dict[str, Any]]] = None


class LLMGateway:
    def __init__(self):
        self.models: Dict[str, LLMConfig] = {}
        self.default_model: str = "gpt-4"
        self._register_default_models()
        self._request_counts: Dict[str, int] = {}
        self._rate_limits: Dict[str, int] = {}
    
    def _register_default_models(self):
        models = [
            LLMConfig(Provider.OPENAI, "gpt-4", temperature=0.7, max_tokens=8192),
            LLMConfig(Provider.OPENAI, "gpt-3.5-turbo", temperature=0.7, max_tokens=4096),
            LLMConfig(Provider.ANTHROPIC, "claude-3-opus-20240229", temperature=0.7, max_tokens=4096),
            LLMConfig(Provider.ANTHROPIC, "claude-3-sonnet-20240229", temperature=0.7, max_tokens=4096),
            LLMConfig(Provider.GOOGLE, "gemini-1.5-pro", temperature=0.7, max_tokens=8192),
            LLMConfig(Provider.GOOGLE, "gemini-1.5-flash", temperature=0.7, max_tokens=4096),
            LLMConfig(Provider.META, "llama-3-70b", temperature=0.7, max_tokens=4096),
            LLMConfig(Provider.META, "llama-3-8b", temperature=0.7, max_tokens=4096),
            LLMConfig(Provider.MISTRAL, "mistral-large-latest", temperature=0.7, max_tokens=4096),
            LLMConfig(Provider.MISTRAL, "mistral-small-latest", temperature=0.7, max_tokens=4096),
            LLMConfig(Provider.COHERE, "command-r-plus", temperature=0.7, max_tokens=4096),
        ]
        
        for config in models:
            self.models[config.model] = config
    
    def register_model(self, config: LLMConfig):
        self.models[config.model] = config
    
    def set_default_model(self, model: str):
        if model in self.models:
            self.default_model = model
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        return [
            {
                "model": m.model,
                "provider": m.provider.value,
                "max_tokens": m.max_tokens
            }
            for m in self.models.values()
        ]
    
    def check_rate_limit(self, model: str) -> bool:
        current_time = int(time.time() / 60)
        key = f"{model}:{current_time}"
        
        if key not in self._request_counts:
            self._request_counts[key] = 0
        
        limit = self._rate_limits.get(model, 100)
        
        if self._request_counts[key] >= limit:
            return False
        
        self._request_counts[key] += 1
        return True
    
    def set_rate_limit(self, model: str, requests_per_minute: int):
        self._rate_limits[model] = requests_per_minute
    
    async def chat(self, request: LLMRequest) -> LLMResponse:
        if not self.check_rate_limit(request.model):
            raise Exception(f"Rate limit exceeded for {request.model}")
        
        config = self.models.get(request.model, self.models.get(self.default_model))
        
        await asyncio.sleep(0.1)
        
        content = self._simulate_response(request.messages, config)
        
        usage = {
            "prompt_tokens": sum(len(m["content"].split()) for m in request.messages),
            "completion_tokens": len(content.split()),
            "total_tokens": sum(len(m["content"].split()) for m in request.messages) + len(content.split())
        }
        
        return LLMResponse(
            model=request.model,
            content=content,
            usage=usage,
            finish_reason="stop"
        )
    
    async def chat_stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        if not self.check_rate_limit(request.model):
            raise Exception(f"Rate limit exceeded for {request.model}")
        
        config = self.models.get(request.model, self.models.get(self.default_model))
        
        words = self._simulate_response(request.messages, config).split()
        
        for i, word in enumerate(words):
            chunk = f"data: {{'content': '{word} ', 'index': {i}, 'done': false}}\n\n"
            yield chunk
            await asyncio.sleep(0.05)
        
        yield "data: {'content': '', 'index': len(words), 'done': true}\n\n"
    
    def _simulate_response(self, messages: List[Dict[str, str]], config: LLMConfig) -> str:
        last_message = messages[-1]["content"] if messages else ""
        
        responses = {
            Provider.OPENAI: f"GPT-4 responding to: {last_message[:50]}...",
            Provider.ANTHROPIC: f"Claude responding to: {last_message[:50]}...",
            Provider.GOOGLE: f"Gemini responding to: {last_message[:50]}...",
            Provider.META: f"Llama responding to: {last_message[:50]}...",
            Provider.MISTRAL: f"Mistral responding to: {last_message[:50]}...",
            Provider.COHERE: f"Command R responding to: {last_message[:50]}...",
        }
        
        return responses.get(config.provider, f"Model responding to: {last_message[:50]}...")
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_models": len(self.models),
            "default_model": self.default_model,
            "providers": list(set(m.provider.value for m in self.models.values())),
            "rate_limits": self._rate_limits
        }


_llm_gateway = LLMGateway()


def get_llm_gateway() -> LLMGateway:
    return _llm_gateway


__all__ = ["LLMGateway", "LLMConfig", "LLMRequest", "LLMResponse", "Provider", "get_llm_gateway"]