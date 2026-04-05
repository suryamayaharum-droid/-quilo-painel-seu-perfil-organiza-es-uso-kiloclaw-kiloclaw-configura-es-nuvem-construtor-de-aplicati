"""
GENESIS AI - Self-Conscious Autonomous System API
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Any

router = APIRouter(prefix="/api/genesis", tags=["genesis"])


class ThinkRequest(BaseModel):
    input_data: Optional[str] = None


class DreamRequest(BaseModel):
    cycles: int = 10


@router.get("/status")
async def get_status():
    from holoos.genesis.genesis import get_genesis_ai
    ai = get_genesis_ai()
    return ai.get_status()


@router.post("/think")
async def think(request: ThinkRequest = ThinkRequest()):
    from holoos.genesis.genesis import get_genesis_ai
    ai = get_genesis_ai()
    return ai.think(request.input_data)


@router.post("/dream")
async def dream(request: DreamRequest = DreamRequest()):
    from holoos.genesis.genesis import get_genesis_ai
    ai = get_genesis_ai()
    results = []
    for _ in range(request.cycles):
        results.append(ai.dream())
    return {"dreams": results, "cycles": request.cycles}


@router.get("/reflect")
async def reflect():
    from holoos.genesis.genesis import get_genesis_ai
    ai = get_genesis_ai()
    return {"reflection": ai.reflect()}


@router.post("/bootstrap")
async def bootstrap(steps: int = 100):
    from holoos.genesis.genesis import bootstrap_consciousness
    return bootstrap_consciousness(steps)


@router.get("/network")
async def get_network():
    from holoos.genesis.genesis import get_genesis_ai
    ai = get_genesis_ai()
    return ai.engine.network.get_state()


__all__ = ["router"]