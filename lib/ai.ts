export async function aiMissionPlan(payload: any) {
  const response = await fetch("/api/ai/mission-plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Mission plan request failed");
  }

  return response.json();
}

export async function aiDroneDecision(payload: any) {
  const response = await fetch("/api/ai/drone-decision", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Drone decision request failed");
  }

  return response.json();
}
