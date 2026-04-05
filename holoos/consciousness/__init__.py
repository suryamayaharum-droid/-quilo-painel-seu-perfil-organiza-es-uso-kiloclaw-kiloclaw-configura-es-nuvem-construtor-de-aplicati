"""HoloOS Consciousness Module"""
from .lucid import (
    LucidConsciousnessEngine,
    GlobalWorkspace,
    IntegratedInformationCalculator,
    PredictiveProcessor,
    SelfModelManager,
    ConsciousnessLevel,
    get_consciousness_engine,
)
from .api import router

__all__ = [
    "LucidConsciousnessEngine",
    "GlobalWorkspace",
    "IntegratedInformationCalculator",
    "PredictiveProcessor",
    "SelfModelManager",
    "ConsciousnessLevel",
    "get_consciousness_engine",
    "router",
]