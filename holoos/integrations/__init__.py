"""
HoloOS Integrations Package
============================
Integrações com frameworks e serviços externos.
"""

from holoos.integrations.langchain import (
    LangChainAdapter,
    HoloOSTool,
    get_langchain_adapter
)

from holoos.integrations.vector_dbs import (
    ChromaDBVectorStore,
    ChromaDBRAGEngine,
    get_chromadb_rag
)

from holoos.integrations.observability import (
    PrometheusMetrics,
    get_prometheus_metrics
)

__all__ = [
    # LangChain
    "LangChainAdapter",
    "HoloOSTool",
    "get_langchain_adapter",
    
    # Vector DBs
    "ChromaDBVectorStore",
    "ChromaDBRAGEngine",
    "get_chromadb_rag",
    
    # Observability
    "PrometheusMetrics",
    "get_prometheus_metrics"
]
