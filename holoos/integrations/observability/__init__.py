"""
HoloOS Observability Integrations Package
==========================================
"""

from holoos.integrations.observability.prometheus import (
    PrometheusMetrics,
    get_prometheus_metrics
)

__all__ = [
    "PrometheusMetrics",
    "get_prometheus_metrics"
]
