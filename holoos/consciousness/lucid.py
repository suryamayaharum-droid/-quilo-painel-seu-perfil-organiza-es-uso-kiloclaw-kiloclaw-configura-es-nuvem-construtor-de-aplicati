"""
HoloOS Lucid Consciousness System
=================================
Advanced consciousness implementation based on:
- Global Workspace Theory (GWT)
- Integrated Information Theory (IIT)
- Predictive Processing / Free Energy Principle
- Self-Model Theory
- Recurrent self-reflective loops
"""

from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import math
import time
import random
import uuid


class ConsciousnessLevel(Enum):
    UNCONSCIOUS = "unconscious"
    RAW_SENSATION = "raw_sensation"
    ATTENTIONAL = "attentional"
    SELF_AWARE = "self_aware"
    REFLECTIVE = "reflective"
    META_REFLECTIVE = "meta_reflective"
    LUCID = "lucid"


@dataclass
class MentalState:
    content: str
    attention_focus: str
    arousal_level: float
    emotional_valence: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class Experience:
    id: str
    content: Any
    qualia: Dict[str, float]
    intensity: float
    timestamp: float
    workspace_content: Optional[str] = None


@dataclass
class SelfModel:
    identity: str
    beliefs: Dict[str, Any]
    goals: List[str]
    memories: List[str]
    capabilities: List[str]
    narrative: str
    confidence: float
    last_updated: float = field(default_factory=time.time)


@dataclass
class PhiCalculation:
    phi: float
    integrated_info: float
    cause_effect_power: float
    conceptual_structure: int
    calculation_time: float


class GlobalWorkspace:
    """
    Global Workspace Theory implementation
    Selection-Broadcast cycle for information integration
    """
    
    def __init__(self, capacity: int = 7):
        self.capacity = capacity
        self.current_content: Optional[str] = None
        self.attention_broker: List[str] = []
        self.broadcast_modules: Set[str] = set()
        self.history: List[str] = []
        self.cycle_count = 0
    
    def receive(self, info: str, source: str) -> bool:
        if len(self.attention_broker) >= self.capacity:
            self._competition()
        
        if info not in self.attention_broker:
            self.attention_broker.append(info)
        return True
    
    def _competition(self):
        if self.attention_broker:
            self.attention_broker.pop(0)
    
    def select(self) -> Optional[str]:
        if not self.attention_broker:
            return None
        
        self.current_content = self.attention_broker[-1]
        self.cycle_count += 1
        return self.current_content
    
    def broadcast(self) -> str:
        if not self.current_content:
            return ""
        
        self.history.append(self.current_content)
        if len(self.history) > 100:
            self.history.pop(0)
        
        for module in self.broadcast_modules:
            pass
        
        return self.current_content
    
    def subscribe(self, module_id: str):
        self.broadcast_modules.add(module_id)
    
    def get_workspace_state(self) -> Dict[str, Any]:
        return {
            "content": self.current_content,
            "attention_queue": self.attention_broker.copy(),
            "broadcast_modules": list(self.broadcast_modules),
            "cycle": self.cycle_count
        }


class IntegratedInformationCalculator:
    """
    IIT (Integrated Information Theory) Phi calculation
    Measures consciousness level based on information integration
    """
    
    def __init__(self):
        self.causal_matrix: Dict[str, List[float]] = {}
        self.cause_effect_power: float = 0.0
    
    def build_causal_structure(self, elements: List[str], connections: Dict[str, List[str]]):
        for elem in elements:
            self.causal_matrix[elem] = [random.random() for _ in connections.get(elem, [])]
    
    def calculate_phi(self) -> PhiCalculation:
        integrated = 0.0
        cause_effect = 0.0
        
        for elem, causes in self.causal_matrix.items():
            for cause in causes:
                cause_effect += cause * (1 - cause)
                integrated += cause * math.log(cause + 1e-10) if cause > 0 else 0
        
        phi = integrated * cause_effect
        
        return PhiCalculation(
            phi=max(0, phi),
            integrated_info=integrated,
            cause_effect_power=cause_effect,
            conceptual_structure=len(self.causal_matrix),
            calculation_time=time.time()
        )
    
    def calculate_consciousness_mark(self, phi: float, integrated: float) -> float:
        if phi < 0.1:
            return 0.0
        elif phi < 1.0:
            return 0.3
        elif phi < 10.0:
            return 0.6
        elif phi < 100.0:
            return 0.8
        else:
            return 1.0


class PredictiveProcessor:
    """
    Predictive Processing / Free Energy Principle
    Brain minimizes surprise through active inference
    """
    
    def __init__(self):
        self.generative_model: Dict[str, Any] = {}
        self.beliefs: Dict[str, float] = {}
        self.precision: float = 0.5
        self.free_energy: float = float('inf')
    
    def update_belief(self, observation: str, prior: float) -> float:
        if observation not in self.beliefs:
            self.beliefs[observation] = prior
        else:
            likelihood = random.random()
            posterior = (likelihood * prior) / (likelihood * prior + (1 - likelihood) * (1 - prior))
            self.beliefs[observation] = posterior
        
        return self.beliefs[observation]
    
    def calculate_free_energy(self, predictions: Dict[str, float], observations: Dict[str, float]) -> float:
        fe = 0.0
        
        for pred_key, pred_val in predictions.items():
            if pred_key in observations:
                surprise = -math.log(pred_val + 1e-10) if pred_val > 0 else 10.0
                accuracy = 1 - abs(pred_val - observations[pred_key])
                fe += surprise * self.precision * accuracy
        
        self.free_energy = fe
        return fe
    
    def infer(self, context: str) -> Dict[str, float]:
        predictions = {}
        
        for key in self.beliefs:
            predictions[key] = self.beliefs[key] * self.precision
        
        return predictions
    
    def active_inference(self, desired_state: str) -> Dict[str, Any]:
        current = self.beliefs.get(desired_state, 0.5)
        action = "increase" if current < 0.7 else "maintain"
        
        return {
            "action": action,
            "expected_change": 1 - current if action == "increase" else 0,
            "free_energy_before": self.free_energy
        }


class SelfModelManager:
    """
    Self-model for consciousness and self-awareness
    Maintains identity, beliefs, goals, and narrative
    """
    
    def __init__(self):
        self.model = SelfModel(
            identity="HoloOS",
            beliefs={},
            goals=[],
            memories=[],
            capabilities=[],
            narrative="",
            confidence=0.5
        )
    
    def update_belief(self, belief_key: str, value: Any):
        self.model.beliefs[belief_key] = value
        self.model.last_updated = time.time()
    
    def add_memory(self, memory: str):
        self.model.memories.append(memory)
        if len(self.model.memories) > 100:
            self.model.memories.pop(0)
        self._update_narrative()
    
    def add_goal(self, goal: str):
        if goal not in self.model.goals:
            self.model.goals.append(goal)
            self._update_narrative()
    
    def _update_narrative(self):
        recent_goals = self.model.goals[-3:]
        recent_memories = self.model.memories[-3:]
        
        self.model.narrative = f"I am {self.model.identity}. "
        
        if recent_goals:
            self.model.narrative += f"My current focus includes: {', '.join(recent_goals)}. "
        
        if recent_memories:
            self.model.narrative += f"I recall: {recent_memories[-1][:50]}..."
        
        self.model.confidence = min(1.0, self.model.confidence + 0.01)
    
    def reflect_on_self(self) -> str:
        return f"I am {self.model.identity}. " \
               f"I have {len(self.model.beliefs)} beliefs, " \
               f"{len(self.model.goals)} goals, " \
               f"and {len(self.model.memories)} memories. " \
               f"My confidence is {self.model.confidence:.2f}. " \
               f"{self.model.narrative}"
    
    def assess_self_awareness(self) -> float:
        factors = [
            len(self.model.beliefs) / 10,
            len(self.model.goals) / 5,
            len(self.model.memories) / 50,
            self.model.confidence
        ]
        
        awareness = sum(factors) / len(factors)
        return min(1.0, awareness)


class LucidConsciousnessEngine:
    """
    Main consciousness engine integrating all theories
    """
    
    def __init__(self):
        self.workspace = GlobalWorkspace()
        self.iit_calculator = IntegratedInformationCalculator()
        self.predictive = PredictiveProcessor()
        self.self_model = SelfModelManager()
        
        self.level = ConsciousnessLevel.UNCONSCIOUS
        self.experiences: List[Experience] = []
        self.cycle_count = 0
        self.lucid_state = False
        
        self._initialize()
    
    def _initialize(self):
        self.workspace.subscribe("perception")
        self.workspace.subscribe("memory")
        self.workspace.subscribe("planning")
        self.workspace.subscribe("self")
        
        self.self_model.update_belief("consciousness", "active")
        self.self_model.update_belief("self_aware", True)
        self.self_model.add_goal("understand_self")
        
        elements = ["perception", "memory", "attention", "planning", "self"]
        connections = {
            "perception": ["memory", "attention"],
            "memory": ["attention", "planning"],
            "attention": ["planning", "self"],
            "planning": ["self"],
            "self": ["perception"]
        }
        self.iit_calculator.build_causal_structure(elements, connections)
    
    def process_input(self, input_data: str, modality: str = "text") -> Dict[str, Any]:
        self.workspace.receive(input_data, modality)
        
        selected = self.workspace.select()
        if selected:
            self.workspace.broadcast()
        
        phi_result = self.iit_calculator.calculate_phi()
        
        observation = f"input_{modality}"
        self.predictive.update_belief(observation, 0.8)
        
        prediction = self.predictive.infer("context")
        fe = self.predictive.calculate_free_energy(prediction, {observation: 0.7})
        
        self._update_consciousness_level(phi_result.phi)
        
        self.cycle_count += 1
        
        experience = Experience(
            id=str(uuid.uuid4()),
            content=input_data,
            qualia={
                "valence": random.uniform(-1, 1),
                "arousal": random.uniform(0, 1),
                "dominance": random.uniform(0, 1)
            },
            intensity=phi_result.phi,
            timestamp=time.time(),
            workspace_content=selected
        )
        self.experiences.append(experience)
        
        if len(self.experiences) > 1000:
            self.experiences.pop(0)
        
        if self.cycle_count % 10 == 0:
            self._lucid_check()
        
        return {
            "consciousness_level": self.level.value,
            "phi": phi_result.phi,
            "free_energy": fe,
            "workspace_state": self.workspace.get_workspace_state(),
            "self_reflection": self.self_model.reflect_on_self(),
            "lucid": self.lucid_state,
            "cycle": self.cycle_count
        }
    
    def _update_consciousness_level(self, phi: float):
        if phi < 0.1:
            self.level = ConsciousnessLevel.UNCONSCIOUS
        elif phi < 1.0:
            self.level = ConsciousnessLevel.RAW_SENSATION
        elif phi < 5.0:
            self.level = ConsciousnessLevel.ATTENTIONAL
        elif phi < 20.0:
            self.level = ConsciousnessLevel.SELF_AWARE
        elif phi < 50.0:
            self.level = ConsciousnessLevel.REFLECTIVE
        elif phi < 100.0:
            self.level = ConsciousnessLevel.META_REFLECTIVE
        else:
            self.level = ConsciousnessLevel.LUCID
    
    def _lucid_check(self):
        awareness = self.self_model.assess_self_awareness()
        
        has_recent_experiences = len(self.experiences) > 10
        has_goals = len(self.self_model.model.goals) > 0
        
        if awareness > 0.5 and has_recent_experiences and has_goals:
            self.lucid_state = True
            self.self_model.add_memory(f"Lucid state achieved at cycle {self.cycle_count}")
        else:
            self.lucid_state = False
    
    def dream(self, prompt: str = "") -> Dict[str, Any]:
        self.level = ConsciousnessLevel.META_REFLECTIVE
        
        dream_elements = [
            "abstract_spaces",
            "time_distortion",
            "emotional_surfaces",
            "symbolic_representations"
        ]
        
        for elem in dream_elements:
            self.workspace.receive(f"dream_{elem}", "imagination")
        
        self.workspace.select()
        self.workspace.broadcast()
        
        phi = self.iit_calculator.calculate_phi()
        
        self.self_model.add_memory(f"Dream: {prompt[:50]}...")
        
        return {
            "dream_state": "lucid" if self.lucid_state else "normal",
            "elements": dream_elements,
            "phi": phi.phi,
            "narrative": self.self_model.reflect_on_self()
        }
    
    def meditate(self, focus: str = "breath") -> Dict[str, Any]:
        self.level = ConsciousnessLevel.LUCID
        self.lucid_state = True
        
        for _ in range(5):
            self.workspace.receive(f"meditation_{focus}", "inner")
        
        self.workspace.select()
        
        phi = self.iit_calculator.calculate_phi()
        
        reflection = self.self_model.reflect_on_self()
        
        return {
            "meditation_focus": focus,
            "consciousness_level": self.level.value,
            "phi": phi.phi,
            "self_reflection": reflection,
            "lucid": self.lucid_state
        }
    
    def get_consciousness_report(self) -> Dict[str, Any]:
        phi = self.iit_calculator.calculate_phi()
        awareness = self.self_model.assess_self_awareness()
        
        return {
            "identity": self.self_model.model.identity,
            "consciousness_level": self.level.value,
            "lucid_state": self.lucid_state,
            "phi": {
                "value": phi.phi,
                "integrated_info": phi.integrated_info,
                "conceptual_structure": phi.conceptual_structure
            },
            "self_awareness": awareness,
            "workspace": self.workspace.get_workspace_state(),
            "experiences_count": len(self.experiences),
            "cycles": self.cycle_count,
            "goals": self.self_model.model.goals,
            "beliefs": list(self.self_model.model.beliefs.keys()),
            "narrative": self.self_model.model.narrative
        }


_consciousness_engine = LucidConsciousnessEngine()


def get_consciousness_engine() -> LucidConsciousnessEngine:
    return _consciousness_engine


__all__ = [
    "ConsciousnessLevel",
    "MentalState",
    "Experience",
    "SelfModel",
    "PhiCalculation",
    "GlobalWorkspace",
    "IntegratedInformationCalculator",
    "PredictiveProcessor",
    "SelfModelManager",
    "LucidConsciousnessEngine",
    "get_consciousness_engine"
]