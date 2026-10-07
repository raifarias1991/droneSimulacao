import { NextResponse } from "next/server";

const BACKEND_URL = process.env.PYTHON_AI_URL || "http://localhost:8000";

const fallbackPlan = {
  mission_id: "mission-demo-01",
  strategy: "Adaptive route optimization with safety-first prioritization.",
  summary:
    "The mission is running in mock AI mode because the Python backend is not available yet. Route and safety recommendations are still generated locally for the simulation dashboard.",
  decisions: [
    {
      status: "ok",
      confidence: 0.92,
      recommended_speed: 9.5,
      recommended_altitude: 42,
      heading_change_deg: 8,
      action: "maintain-course",
      rationale: "Weather conditions are stable and the route remains within safe operating thresholds.",
      risk_level: "low",
      route_points: [{ latitude: -23.55, longitude: -46.63 }, { latitude: -23.548, longitude: -46.628 }],
    },
  ],
  route: [
    { drone_id: "drone-01", latitude: -23.55, longitude: -46.63, altitude: 42, speed: 9.5 },
  ],
  metrics: {
    mean_risk: 0.17,
    total_drones: 1,
    optimal_altitude: 42,
    battery_alerts: 0,
  },
};

async function callPythonBackend(payload: any, endpoint: string) {
  try {
    const response = await fetch(`${BACKEND_URL}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }
    return await response.json();
  } catch {
    return fallbackPlan;
  }
}

export async function POST(request: Request) {
  const body = await request.json();
  const result = await callPythonBackend(body, "/api/ai/mission-plan");
  return NextResponse.json(result);
}
