from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class DroneMissionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mission_id: str = Field(..., description="Unique mission identifier")
    drone_id: str = Field(..., description="Drone identifier")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    altitude: float = Field(..., ge=0)
    battery: float = Field(..., ge=0, le=100)
    speed: float = Field(..., ge=0)
    heading: float = Field(..., ge=0, le=360)
    weather: Literal["clear", "rain", "wind", "storm", "fog"] = "clear"
    obstacles: list[dict] = Field(default_factory=list)
    target_latitude: float | None = Field(default=None, ge=-90, le=90)
    target_longitude: float | None = Field(default=None, ge=-180, le=180)
    target_altitude: float | None = Field(default=None, ge=0)
    telemetry: dict = Field(default_factory=dict)


class MissionPlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mission_id: str = Field(..., min_length=1)
    drone_id: str = Field(..., min_length=1)
    scenario: str = Field(..., min_length=5)
    objective: str = Field(..., min_length=5)
    drones: list[DroneMissionInput] = Field(default_factory=list)
    constraints: dict = Field(default_factory=dict)


class DroneDecision(BaseModel):
    status: str
    confidence: float
    recommended_speed: float
    recommended_altitude: float
    heading_change_deg: float
    action: str
    rationale: str
    risk_level: str
    route_points: list[dict]


class MissionPlanResponse(BaseModel):
    mission_id: str
    strategy: str
    summary: str
    decisions: list[DroneDecision]
    route: list[dict]
    metrics: dict
