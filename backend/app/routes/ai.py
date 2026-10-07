from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.schemas.ai import DroneMissionInput, MissionPlanRequest, MissionPlanResponse
from app.services.drone_service import DroneIntelligenceService
from app.services.llm_service import LLMService

router = APIRouter(tags=["AI"])
settings = get_settings()
llm_service = LLMService()
drone_service = DroneIntelligenceService()


@router.get("/ai/health")
async def ai_health() -> dict[str, Any]:
    return {
        "status": "ok",
        "provider": settings.llm_provider,
        "model": llm_service.get_model_name(),
    }


@router.get("/ai/providers")
async def ai_providers() -> dict[str, Any]:
    return {
        "provider": settings.llm_provider,
        "available": ["mock", "ollama", "openai"],
        "active": settings.llm_provider,
    }


@router.post("/ai/mission-plan", response_model=MissionPlanResponse)
async def create_mission_plan(payload: MissionPlanRequest) -> MissionPlanResponse:
    if not payload.drones:
        raise HTTPException(status_code=400, detail="At least one drone is required.")

    try:
        generated = await llm_service.generate_mission_plan(payload)
        return generated
    except Exception as exc:  # pragma: no cover - defensive fallback
        fallback = drone_service.build_fallback_plan(payload)
        return fallback


@router.post("/ai/drone-decision")
async def drone_decision(drone: DroneMissionInput) -> dict[str, Any]:
    decision = drone_service.evaluate_drone(drone)
    return decision


@router.post("/ai/simulate")
async def simulate_agents(payload: dict[str, Any]) -> dict[str, Any]:
    mission_id = payload.get("mission_id", "mission-unknown")
    confidence = payload.get("confidence", 0.8)
    scenario = payload.get("scenario", "inspection")

    return {
        "mission_id": mission_id,
        "status": "simulated",
        "scenario": scenario,
        "confidence": confidence,
        "recommendations": [
            "Analyze terrain and airspace risk.",
            "Rebalance route to prioritize battery safety.",
            "Adjust altitude to reduce obstacle exposure.",
        ],
    }
