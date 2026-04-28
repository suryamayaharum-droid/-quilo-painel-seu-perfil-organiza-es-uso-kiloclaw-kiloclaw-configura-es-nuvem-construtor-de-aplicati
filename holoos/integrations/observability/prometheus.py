"""
HoloOS Prometheus Integration
==============================
Exporter de métricas para Prometheus.
"""

from typing import Dict, Any, Optional
import logging
import time

logger = logging.getLogger(__name__)

try:
    from prometheus_client import Counter, Gauge, Histogram, start_http_server, CollectorRegistry
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    logger.warning("Prometheus client not installed. Install with: pip install prometheus-client")


class PrometheusMetrics:
    """
    Coletor de métricas do HoloOS para Prometheus.
    """
    
    def __init__(self, port: int = 8001):
        """
        Inicializa métricas Prometheus.
        
        Args:
            port: Porta para expor métricas
        """
        if not PROMETHEUS_AVAILABLE:
            raise ImportError("Prometheus client not available")
        
        self.port = port
        self.registry = CollectorRegistry()
        
        # Métricas de sistema
        self.system_uptime = Gauge(
            'holoos_system_uptime_seconds',
            'Tempo de atividade do sistema em segundos',
            registry=self.registry
        )
        
        self.system_start_time = Gauge(
            'holoos_system_start_time',
            'Timestamp de início do sistema',
            registry=self.registry
        )
        
        # Métricas de AI/Modelos
        self.inference_requests_total = Counter(
            'holoos_inference_requests_total',
            'Total de requisições de inferência',
            ['model_id', 'status'],
            registry=self.registry
        )
        
        self.inference_duration = Histogram(
            'holoos_inference_duration_seconds',
            'Duração das inferências',
            ['model_id'],
            buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
            registry=self.registry
        )
        
        self.tokens_generated_total = Counter(
            'holoos_tokens_generated_total',
            'Total de tokens gerados',
            ['model_id'],
            registry=self.registry
        )
        
        # Métricas de Memória
        self.memory_usage_bytes = Gauge(
            'holoos_memory_usage_bytes',
            'Uso de memória em bytes',
            ['memory_type'],
            registry=self.registry
        )
        
        self.memory_entries_count = Gauge(
            'holoos_memory_entries_count',
            'Número de entradas na memória',
            ['memory_type'],
            registry=self.registry
        )
        
        # Métricas de Agentes
        self.agents_active = Gauge(
            'holoos_agents_active',
            'Número de agentes ativos',
            registry=self.registry
        )
        
        self.tasks_completed_total = Counter(
            'holoos_tasks_completed_total',
            'Total de tarefas completadas',
            ['status'],
            registry=self.registry
        )
        
        # Métricas de Ferramentas
        self.tool_executions_total = Counter(
            'holoos_tool_executions_total',
            'Total de execuções de ferramentas',
            ['tool_name', 'status'],
            registry=self.registry
        )
        
        self.tool_execution_duration = Histogram(
            'holoos_tool_execution_duration_seconds',
            'Duração das execuções de ferramentas',
            ['tool_name'],
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
            registry=self.registry
        )
        
        # Métricas de Segurança
        self.security_threats_total = Counter(
            'holoos_security_threats_total',
            'Total de ameaças de segurança detectadas',
            ['threat_level', 'category'],
            registry=self.registry
        )
        
        # Métricas de Gateway
        self.gateway_requests_total = Counter(
            'holoos_gateway_requests_total',
            'Total de requisições ao gateway',
            ['endpoint', 'method', 'status_code'],
            registry=self.registry
        )
        
        self.gateway_request_duration = Histogram(
            'holoos_gateway_request_duration_seconds',
            'Duração das requisições ao gateway',
            ['endpoint'],
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0],
            registry=self.registry
        )
        
        # Inicia servidor HTTP
        self.start_time = time.time()
        self.system_start_time.set(self.start_time)
        
        logger.info(f"Prometheus metrics initialized on port {port}")
    
    def start_server(self):
        """Inicia o servidor HTTP de métricas."""
        if not PROMETHEUS_AVAILABLE:
            return
        
        start_http_server(self.port, registry=self.registry)
        logger.info(f"Prometheus metrics server started on port {self.port}")
    
    def record_inference(
        self,
        model_id: str,
        duration: float,
        tokens: int,
        success: bool = True
    ):
        """Registra uma inferência."""
        status = "success" if success else "error"
        self.inference_requests_total.labels(model_id=model_id, status=status).inc()
        self.inference_duration.labels(model_id=model_id).observe(duration)
        self.tokens_generated_total.labels(model_id=model_id).inc(tokens)
    
    def record_memory_usage(
        self,
        memory_type: str,
        usage_bytes: int,
        entries_count: int
    ):
        """Registra uso de memória."""
        self.memory_usage_bytes.labels(memory_type=memory_type).set(usage_bytes)
        self.memory_entries_count.labels(memory_type=memory_type).set(entries_count)
    
    def record_tool_execution(
        self,
        tool_name: str,
        duration: float,
        success: bool = True
    ):
        """Registra execução de ferramenta."""
        status = "success" if success else "error"
        self.tool_executions_total.labels(tool_name=tool_name, status=status).inc()
        self.tool_execution_duration.labels(tool_name=tool_name).observe(duration)
    
    def record_security_threat(
        self,
        threat_level: str,
        category: str
    ):
        """Registra ameaça de segurança."""
        self.security_threats_total.labels(
            threat_level=threat_level,
            category=category
        ).inc()
    
    def record_gateway_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        duration: float
    ):
        """Registra requisição ao gateway."""
        self.gateway_requests_total.labels(
            endpoint=endpoint,
            method=method,
            status_code=status_code
        ).inc()
        self.gateway_request_duration.labels(endpoint=endpoint).observe(duration)
    
    def update_system_uptime(self):
        """Atualiza métrica de uptime."""
        self.system_uptime.set(time.time() - self.start_time)
    
    def set_agents_active(self, count: int):
        """Define número de agentes ativos."""
        self.agents_active.set(count)
    
    def record_task_completed(self, status: str = "success"):
        """Registra tarefa completada."""
        self.tasks_completed_total.labels(status=status).inc()


def get_prometheus_metrics(port: int = 8001) -> Optional[PrometheusMetrics]:
    """Factory function para criar coletor de métricas."""
    if not PROMETHEUS_AVAILABLE:
        return None
    return PrometheusMetrics(port=port)


__all__ = [
    "PrometheusMetrics",
    "get_prometheus_metrics"
]
