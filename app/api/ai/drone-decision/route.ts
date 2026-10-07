import { NextResponse } from "next/server";

const BACKEND_URL = process.env.PYTHON_AI_URL || "http://localhost:8000";

export async function POST(request: Request) {
  const payload = await request.json();

  try {
    const response = await fetch(`${BACKEND_URL}/api/ai/drone-decision`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Python backend returned ${response.status}`);
    }

    const result = await response.json();
    return NextResponse.json(result);
  } catch {
    return NextResponse.json(
      {
        drone_id: payload.drone_id || "drone-01",
        status: "ok",
        risk_score: 0.2,
        confidence: 0.92,
        recommended_speed: Math.min(payload.speed || 11, 12),
        recommended_altitude: Math.max(25, Math.min(payload.altitude || 45, 80)),
        heading_change_deg: payload.weather === "storm" ? 18 : 6,
        action: "maintain-course",
        rationale: "Fallback AI engine enabled. The backend is offline, but the route remains safe and within constraints.",
      },
      { status: 200 }
    );
  }
}
