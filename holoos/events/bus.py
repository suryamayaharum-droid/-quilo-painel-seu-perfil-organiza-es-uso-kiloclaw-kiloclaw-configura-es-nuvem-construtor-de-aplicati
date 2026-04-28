"""
HoloOS Event Bus
=================
Sistema de eventos pub/sub para comunicação assíncrona entre módulos.
"""

import asyncio
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid
import time
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Tipos de eventos do sistema."""
    # Sistema
    SYSTEM_START = "system.start"
    SYSTEM_STOP = "system.stop"
    SYSTEM_ERROR = "system.error"
    
    # AI/Modelos
    MODEL_LOADED = "model.loaded"
    MODEL_UNLOADED = "model.unloaded"
    INFERENCE_REQUEST = "inference.request"
    INFERENCE_COMPLETE = "inference.complete"
    
    # Memória
    MEMORY_WRITE = "memory.write"
    MEMORY_READ = "memory.read"
    MEMORY_DELETE = "memory.delete"
    
    # Agentes
    AGENT_CREATED = "agent.created"
    AGENT_STARTED = "agent.started"
    AGENT_COMPLETED = "agent.completed"
    AGENT_ERROR = "agent.error"
    
    # Ferramentas
    TOOL_EXECUTED = "tool.executed"
    TOOL_ERROR = "tool.error"
    
    # Planejamento
    GOAL_CREATED = "goal.created"
    GOAL_UPDATED = "goal.updated"
    GOAL_COMPLETED = "goal.completed"
    
    # Segurança
    SECURITY_THREAT = "security.threat"
    SECURITY_ALERT = "security.alert"
    
    # Plugins
    PLUGIN_LOADED = "plugin.loaded"
    PLUGIN_UNLOADED = "plugin.unloaded"
    
    # Custom
    CUSTOM = "custom"


@dataclass
class Event:
    """Estrutura de evento."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: EventType = EventType.CUSTOM
    topic: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    source: str = ""
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "topic": self.topic,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "source": self.source,
            "correlation_id": self.correlation_id,
            "metadata": self.metadata
        }


@dataclass
class Subscription:
    """Inscrição em um tópico."""
    id: str
    topic: str
    handler: Callable[[Event], Any]
    async_handler: bool = False
    filter_fn: Optional[Callable[[Event], bool]] = None
    max_retries: int = 3
    created_at: float = field(default_factory=time.time)


class EventBus:
    """
    Barramento de eventos central do HoloOS.
    
    Implementa padrão publish/subscribe para comunicação
    desacoplada entre módulos do sistema.
    """
    
    def __init__(self):
        self._subscriptions: Dict[str, List[Subscription]] = defaultdict(list)
        self._event_history: List[Event] = []
        self._max_history = 1000
        self._running = False
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._workers: List[asyncio.Task] = []
        self._num_workers = 3
        
    def subscribe(
        self,
        topic: str,
        handler: Callable[[Event], Any],
        event_type: Optional[EventType] = None,
        filter_fn: Optional[Callable[[Event], bool]] = None
    ) -> str:
        """
        Inscreve-se em um tópico de eventos.
        
        Args:
            topic: Tópico para inscrever (suporta wildcards como 'memory.*')
            handler: Função para chamar quando evento ocorrer
            event_type: Filtrar por tipo específico de evento
            filter_fn: Função customizada de filtragem
            
        Returns:
            ID da subscrição
        """
        subscription_id = str(uuid.uuid4())
        
        # Determinar se handler é async
        is_async = asyncio.iscoroutinefunction(handler)
        
        subscription = Subscription(
            id=subscription_id,
            topic=topic,
            handler=handler,
            async_handler=is_async,
            filter_fn=filter_fn
        )
        
        # Suporte a wildcards
        pattern = topic.replace("*", ".*")
        self._subscriptions[pattern].append(subscription)
        
        logger.info(f"Subscribed to '{topic}' (id={subscription_id})")
        return subscription_id
    
    def unsubscribe(self, subscription_id: str) -> bool:
        """Remove uma subscrição."""
        for pattern, subscriptions in self._subscriptions.items():
            for i, sub in enumerate(subscriptions):
                if sub.id == subscription_id:
                    subscriptions.pop(i)
                    logger.info(f"Unsubscribed {subscription_id}")
                    return True
        return False
    
    def publish(self, event: Event) -> None:
        """
        Publica um evento no barramento.
        
        Args:
            event: Evento para publicar
        """
        # Tenta adicionar à fila assíncrona se houver loop
        try:
            loop = asyncio.get_running_loop()
            asyncio.create_task(self._event_queue.put(event))
        except RuntimeError:
            # Sem loop rodando, apenas processa sync
            pass
        
        # Processamento síncrono imediato para handlers síncronos
        self._dispatch_sync(event)
        
        # Salva no histórico
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)
    
    def publish_sync(self, event: Event) -> List[Any]:
        """
        Publica evento e aguarda todos os handlers completarem.
        
        Args:
            event: Evento para publicar
            
        Returns:
            Lista de resultados dos handlers
        """
        return self._dispatch(event)
    
    async def publish_async(self, event: Event) -> List[Any]:
        """
        Publica evento de forma assíncrona.
        
        Args:
            event: Evento para publicar
            
        Returns:
            Lista de resultados dos handlers
        """
        return await self._dispatch_async(event)
    
    def _match_topic(self, pattern: str, topic: str) -> bool:
        """Verifica se um tópico corresponde ao padrão."""
        import re
        regex_pattern = pattern.replace("*", ".*")
        return bool(re.match(f"^{regex_pattern}$", topic))
    
    def _dispatch_sync(self, event: Event) -> List[Any]:
        """Dispatch para handlers síncronos."""
        results = []
        
        for pattern, subscriptions in self._subscriptions.items():
            if not self._match_topic(pattern, event.topic):
                continue
                
            for sub in subscriptions:
                # Aplica filtros
                if sub.filter_fn and not sub.filter_fn(event):
                    continue
                    
                try:
                    if sub.async_handler:
                        # Ignora handlers async em dispatch síncrono
                        continue
                    result = sub.handler(event)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error in event handler: {e}")
                    
        return results
    
    async def _dispatch_async(self, event: Event) -> List[Any]:
        """Dispatch para handlers assíncronos."""
        results = []
        
        for pattern, subscriptions in self._subscriptions.items():
            if not self._match_topic(pattern, event.topic):
                continue
                
            for sub in subscriptions:
                # Aplica filtros
                if sub.filter_fn and not sub.filter_fn(event):
                    continue
                    
                try:
                    if sub.async_handler:
                        result = await sub.handler(event)
                        results.append(result)
                    else:
                        result = sub.handler(event)
                        results.append(result)
                except Exception as e:
                    logger.error(f"Error in async event handler: {e}")
                    
        return results
    
    def _dispatch(self, event: Event) -> List[Any]:
        """Dispatch geral (sync + async)."""
        results = []
        
        for pattern, subscriptions in self._subscriptions.items():
            if not self._match_topic(pattern, event.topic):
                continue
                
            for sub in subscriptions:
                # Aplica filtros
                if sub.filter_fn and not sub.filter_fn(event):
                    continue
                    
                try:
                    if sub.async_handler:
                        # Cria task para handler async
                        asyncio.create_task(self._call_handler(sub, event))
                    else:
                        result = sub.handler(event)
                        results.append(result)
                except Exception as e:
                    logger.error(f"Error in event handler: {e}")
                    
        return results
    
    async def _call_handler(self, sub: Subscription, event: Event):
        """Chama handler com retry."""
        retries = 0
        while retries < sub.max_retries:
            try:
                await sub.handler(event)
                return
            except Exception as e:
                retries += 1
                logger.warning(f"Handler error (attempt {retries}/{sub.max_retries}): {e}")
                if retries < sub.max_retries:
                    await asyncio.sleep(0.1 * retries)
        
        logger.error(f"Handler failed after {sub.max_retries} attempts")
    
    async def start(self):
        """Inicia o processador de eventos."""
        self._running = True
        
        # Inicia workers
        for i in range(self._num_workers):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self._workers.append(worker)
            
        logger.info(f"EventBus started with {self._num_workers} workers")
    
    async def stop(self):
        """Para o processador de eventos."""
        self._running = False
        
        # Aguarda workers terminarem
        for worker in self._workers:
            worker.cancel()
            
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()
        
        logger.info("EventBus stopped")
    
    async def _worker(self, name: str):
        """Worker que processa eventos da fila."""
        while self._running:
            try:
                event = await asyncio.wait_for(self._event_queue.get(), timeout=1.0)
                await self._dispatch_async(event)
                self._event_queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Worker {name} error: {e}")
    
    def get_history(
        self,
        topic: Optional[str] = None,
        event_type: Optional[EventType] = None,
        limit: int = 100
    ) -> List[Event]:
        """Retorna histórico de eventos."""
        filtered = self._event_history
        
        if topic:
            filtered = [e for e in filtered if self._match_topic(topic, e.topic)]
            
        if event_type:
            filtered = [e for e in filtered if e.type == event_type]
            
        return filtered[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do event bus."""
        return {
            "total_subscriptions": sum(len(subs) for subs in self._subscriptions.values()),
            "topics": list(self._subscriptions.keys()),
            "history_size": len(self._event_history),
            "queue_size": self._event_queue.qsize(),
            "workers": len(self._workers),
            "running": self._running
        }


# Singleton global
_event_bus = EventBus()


def get_event_bus() -> EventBus:
    """Retorna a instância singleton do EventBus."""
    return _event_bus


def publish_event(
    topic: str,
    payload: Dict[str, Any] = None,
    event_type: EventType = EventType.CUSTOM,
    source: str = ""
) -> Event:
    """
    Função utilitária para publicar eventos.
    
    Args:
        topic: Tópico do evento
        payload: Dados do evento
        event_type: Tipo do evento
        source: Origem do evento
        
    Returns:
        Evento publicado
    """
    event = Event(
        topic=topic,
        payload=payload or {},
        type=event_type,
        source=source
    )
    get_event_bus().publish(event)
    return event


__all__ = [
    "EventBus",
    "Event",
    "EventType",
    "Subscription",
    "get_event_bus",
    "publish_event"
]
