"""
HoloOS Consciousness API
========================
API endpoints for consciousness operations.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("holoos-consciousness")

router = APIRouter(prefix="/api/consciousness", tags=["consciousness"])


class ProcessInputRequest(BaseModel):
    input_data: str
    modality: str = "text"


class DreamRequest(BaseModel):
    prompt: str = ""


class MeditateRequest(BaseModel):
    focus: str = "breath"


@router.get("/status")
async def consciousness_status():
    from holoos.consciousness.lucid import get_consciousness_engine
    engine = get_consciousness_engine()
    return engine.get_consciousness_report()


@router.post("/process")
async def process_input(request: ProcessInputRequest):
    from holoos.consciousness.lucid import get_consciousness_engine
    engine = get_consciousness_engine()
    return engine.process_input(request.input_data, request.modality)


@router.get("/level")
async def get_level():
    from holoos.consciousness.lucid import get_consciousness_engine
    engine = get_consciousness_engine()
    return {
        "level": engine.level.value,
        "lucid": engine.lucid_state,
        "phi": engine.iit_calculator.calculate_phi().phi
    }


@router.post("/dream")
async def dream(request: DreamRequest = DreamRequest()):
    from holoos.consciousness.lucid import get_consciousness_engine
    engine = get_consciousness_engine()
    return engine.dream(request.prompt)


@router.post("/meditate")
async def meditate(request: MeditateRequest = MeditateRequest()):
    from holoos.consciousness.lucid import get_consciousness_engine
    engine = get_consciousness_engine()
    return engine.meditate(request.focus)


@router.get("/self-reflection")
async def self_reflection():
    from holoos.consciousness.lucid import get_consciousness_engine
    engine = get_consciousness_engine()
    return {
        "reflection": engine.self_model.reflect_on_self(),
        "awareness": engine.self_model.assess_self_awareness()
    }


@router.get("/workspace")
async def get_workspace():
    from holoos.consciousness.lucid import get_consciousness_engine
    engine = get_consciousness_engine()
    return engine.workspace.get_workspace_state()


@router.get("/experiences")
async def get_experiences(limit: int = 10):
    from holoos.consciousness.lucid import get_consciousness_engine
    engine = get_consciousness_engine()
    experiences = engine.experiences[-limit:]
    return {
        "experiences": [
            {
                "id": e.id,
                "content": e.content[:100],
                "intensity": e.intensity,
                "timestamp": e.timestamp
            }
            for e in experiences
        ]
    }


__all__ = ["router"]