from __future__ import annotations

from typing import Any

from app.config import get_settings
from app.schemas.ai import DroneDecision, DroneMissionInput, MissionPlanRequest, MissionPlanResponse


class DroneIntelligenceService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def evaluate_drone(self, drone: DroneMissionInput) -> dict[str, Any]:
        # heuristic-based AI for operational risk estimation and route guidance
        risk_score = self._compute_risk(drone)
        action = "maintain-course"
        if drone.battery < self.settings.battery_warning_level:
            action = "return-to-base"
        elif drone.weather in {"rain", "storm", "fog"}:
            action = "reduce-speed-and-altitude"

        recommended_speed = min(drone.speed, self.settings.drone_max_speed)
        recommended_altitude = max(self.settings.drone_min_altitude, min(drone.altitude, self.settings.drone_max_altitude))

        heading_change = 0.0
        if drone.weather == "wind":
            heading_change = 12.0
        elif drone.weather == "storm":
            heading_change = 28.0

        return {
            "drone_id": drone.drone_id,
            "status": "ok" if risk_score < 0.5 else "warning",
            "risk_score": round(risk_score, 3),
            "confidence": round(1 - risk_score, 3),
            "recommended_speed": round(recommended_speed, 2),
            "recommended_altitude": round(recommended_altitude, 2),
            "heading_change_deg": round(heading_change, 2),
            "action": action,
            "rationale": self._reasoning_text(drone, risk_score),
        }

    def build_fallback_plan(self, payload: MissionPlanRequest | Any) -> MissionPlanResponse:
        decisions: list[DroneDecision] = []
        route: list[dict] = []

        for index, drone in enumerate(getattr(payload, "drones", []) or []):
            decision = self.evaluate_drone(drone)
            route.append({
                "drone_id": drone.drone_id,
                "latitude": drone.latitude,
                "longitude": drone.longitude,
                "altitude": decision["recommended_altitude"],
                "speed": decision["recommended_speed"],
            })

            decisions.append(
                DroneDecision(
                    status=decision["status"],
                    confidence=decision["confidence"],
                    recommended_speed=decision["recommended_speed"],
                    recommended_altitude=decision["recommended_altitude"],
                    heading_change_deg=decision["heading_change_deg"],
                    action=decision["action"],
                    rationale=decision["rationale"],
                    risk_level="low" if decision["risk_score"] < 0.4 else "medium" if decision["risk_score"] < 0.7 else "high",
                    route_points=[
                        {"latitude": drone.latitude, "longitude": drone.longitude},
                        {"latitude": drone.target_latitude or drone.latitude, "longitude": drone.target_longitude or drone.longitude},
                    ],
                )
            )

        metrics = {
            "mean_risk": round(sum((d.confidence for d in decisions)) / max(len(decisions), 1), 3),
            "total_drones": len(decisions),
            "optimal_altitude": round(sum(d.recommended_altitude for d in decisions) / max(len(decisions), 1), 2),
            "battery_alerts": sum(1 for d in decisions if d.action == "return-to-base"),
        }

        return MissionPlanResponse(
            mission_id=getattr(payload, "mission_id", "mission-unknown"),
            strategy="Adaptive route optimization with safety-first prioritization.",
            summary=f"Mission {getattr(payload, 'mission_id', 'mission-unknown')} planned for {len(decisions)} drone(s) under dynamic environmental constraints.",
            decisions=decisions,
            route=route,
            metrics=metrics,
        )

    def _compute_risk(self, drone: DroneMissionInput) -> float:
        weather_penalty = {"clear": 0.05, "rain": 0.18, "wind": 0.22, "storm": 0.45, "fog": 0.28}[drone.weather]
        battery_penalty = max(0.0, (100 - drone.battery) / 100.0) * 0.6
        altitude_penalty = 0.0
        if drone.altitude > self.settings.drone_max_altitude * 0.8:
            altitude_penalty = 0.16
        obstacle_penalty = min(len(drone.obstacles) * 0.12, 0.35)
        return min(0.95, weather_penalty + battery_penalty + altitude_penalty + obstacle_penalty)

    def _reasoning_text(self, drone: DroneMissionInput, risk_score: float) -> str:
        if risk_score >= 0.7:
            return "High operational risk: weather, battery, and obstacle profile require conservative maneuvering."
        if drone.battery < self.settings.battery_warning_level:
            return "Battery reserve is lower than the safety threshold; prioritize return-to-base logic."
        if drone.weather in {"rain", "storm", "fog"}:
            return "Environmental conditions reduce visual and flight stability margins; reduce speed and altitude."
        return "Conditions are acceptable for continued mission execution with moderate monitoring."
