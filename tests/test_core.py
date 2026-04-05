"""Tests for HoloOS Core"""
import pytest
from holoos.core.types import Language, QuantizationFormat
from holoos.core.registry import ComponentRegistry
from holoos.core.pipeline import PipelineCoordinator


class TestTypes:
    def test_language_count(self):
        assert len(Language) >= 35
    
    def test_quantization_formats(self):
        assert len(QuantizationFormat) >= 20


class TestRegistry:
    def test_register_component(self):
        registry = ComponentRegistry()
        registry.register("test", {"key": "value"})
        assert registry.get("test") == {"key": "value"}
    
    def test_list_components(self):
        registry = ComponentRegistry()
        registry.register("comp1", {"data": 1})
        registry.register("comp2", {"data": 2})
        components = registry.list_all()
        assert len(components) == 2


class TestPipeline:
    def test_coordinator_initialization(self):
        coordinator = PipelineCoordinator()
        assert coordinator is not None
    
    def test_pipeline_creation(self):
        coordinator = PipelineCoordinator()
        pipeline = coordinator.create_pipeline("test_pipeline")
        assert pipeline is not None