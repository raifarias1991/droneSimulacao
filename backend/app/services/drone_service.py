from __future__ import annotations

import os
from typing import Any

import httpx
from openai import OpenAI

from app.config import get_settings


class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._openai_client = None

    def get_model_name(self) -> str:
        if self.settings.llm_provider == "openai":
            return self.settings.openai_model
        if self.settings.llm_provider == "ollama":
            return self.settings.ollama_model
        return "mock-model"

    def _ensure_openai_client(self) -> OpenAI | None:
        if self.settings.llm_provider != "openai":
            return None
        api_key = self.settings.openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Configure the environment before using OpenAI.")
        if self._openai_client is None:
            self._openai_client = OpenAI(api_key=api_key)
        return self._openai_client

    async def generate_mission_plan(self, payload: Any) -> Any:
        if self.settings.llm_provider == "mock":
            return self._generate_mock_plan(payload)

        if self.settings.llm_provider == "ollama":
            return await self._generate_via_ollama(payload)

        if self.settings.llm_provider == "openai":
            return await self._generate_via_openai(payload)

        return self._generate_mock_plan(payload)

    def _generate_mock_plan(self, payload: Any) -> Any:
        from app.services.drone_service import DroneIntelligenceService

        service = DroneIntelligenceService()
        return service.build_fallback_plan(payload)

    async def _generate_via_ollama(self, payload: Any) -> Any:
        system_prompt = (
            "You are an AI mission planner for autonomous drones. "
            "Return structured JSON with a mission strategy, summary, decisions, route and metrics."
        )
        user_prompt = self._serialize_payload(payload)

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{self.settings.ollama_base_url}/api/generate",
                json={
                    "model": self.settings.ollama_model,
                    "stream": False,
                    "system": system_prompt,
                    "prompt": user_prompt,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data.get("response", "")
            return self._parse_llm_response(content, payload)

    async def _generate_via_openai(self, payload: Any) -> Any:
        client = self._ensure_openai_client()
        if client is None:
            return self._generate_mock_plan(payload)

        response = client.responses.create(
            model=self.settings.openai_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a drone mission planning specialist. "
                        "Return valid JSON with keys mission_id, strategy, summary, decisions, route, metrics."
                    ),
                },
                {
                    "role": "user",
                    "content": self._serialize_payload(payload),
                },
            ],
        )
        text = getattr(response, "output_text", "")
        return self._parse_llm_response(text, payload)

    def _serialize_payload(self, payload: Any) -> str:
        return str(payload.model_dump() if hasattr(payload, "model_dump") else payload)

    def _parse_llm_response(self, content: str, payload: Any) -> Any:
        import json

        try:
            parsed = json.loads(content)
            if isinstance(parsed, dict):
                parsed.setdefault("mission_id", getattr(payload, "mission_id", "mission-unknown"))
                return parsed
        except json.JSONDecodeError:
            pass

        from app.services.drone_service import DroneIntelligenceService

        fallback = DroneIntelligenceService().build_fallback_plan(payload)
        fallback["summary"] = content[:500]
        return fallback
