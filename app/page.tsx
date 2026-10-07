"use client";

import { useState } from "react";

const sampleMission = {
  mission_id: "mission-demo-01",
  drone_id: "drone-01",
  scenario: "Perimeter inspection in downtown district",
  objective: "Scan rooftops and identify no-fly zones",
  drones: [
    {
      mission_id: "mission-demo-01",
      drone_id: "drone-01",
      latitude: -23.55,
      longitude: -46.63,
      altitude: 48,
      battery: 76,
      speed: 11,
      heading: 90,
      weather: "wind",
      obstacles: [{ type: "tower", altitude: 70 }, { type: "antenna", altitude: 58 }],
      target_latitude: -23.548,
      target_longitude: -46.628,
      target_altitude: 35,
      telemetry: { temperature: 28, signal: 88 },
    },
  ],
  constraints: {
    max_altitude: 120,
    battery_threshold: 25,
    preferred_routes: ["west-corridor", "northern-ring"],
  },
};

const statStyle = { display: "grid", gap: 8, padding: 18, borderRadius: 16, border: "1px solid rgba(148,163,184,.2)", background: "rgba(15, 23, 42, .7)" } as const;

export default function HomePage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const runMission = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/ai/mission-plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(sampleMission),
      });
      const data = await response.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ maxWidth: 1200, margin: "0 auto", padding: "40px 20px 80px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 16, marginBottom: 28, flexWrap: "wrap" }}>
        <div>
          <div className="pill">Live AI Mission Control</div>
          <h1 style={{ margin: "14px 0 10px", fontSize: "clamp(2.2rem, 5vw, 4rem)", lineHeight: 1.1 }}>Drone intelligence dashboard</h1>
        </div>
        <button
          onClick={runMission}
          disabled={loading}
          style={{
            border: "none",
            borderRadius: 14,
            padding: "14px 22px",
            fontWeight: 700,
            background: loading ? "#334155" : "linear-gradient(135deg, #22c55e 0%, #10b981 100%)",
            color: "#03150d",
            cursor: loading ? "not-allowed" : "pointer",
            boxShadow: "0 12px 30px rgba(34, 197, 94, 0.4)",
          }}
        >
          {loading ? "Planning mission..." : "Generate mission plan"}
        </button>
      </div>

      <section style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 18, marginBottom: 28 }}>
        <div style={statStyle}>
          <span style={{ color: "#94a3b8" }}>Mission ID</span>
          <strong style={{ fontSize: 28 }}>{sampleMission.mission_id}</strong>
        </div>
        <div style={statStyle}>
          <span style={{ color: "#94a3b8" }}>Drone fleet</span>
          <strong style={{ fontSize: 28 }}>{sampleMission.drones.length}</strong>
        </div>
        <div style={statStyle}>
          <span style={{ color: "#94a3b8" }}>Battery threshold</span>
          <strong style={{ fontSize: 28 }}>{sampleMission.constraints.battery_threshold}%</strong>
        </div>
        <div style={statStyle}>
          <span style={{ color: "#94a3b8" }}>Provider</span>
          <strong style={{ fontSize: 28 }}>Python AI</strong>
        </div>
      </section>

      <section className="card" style={{ padding: 24, marginBottom: 28 }}>
        <h2 style={{ margin: "0 0 12px" }}>Mission context</h2>
        <p style={{ margin: 0, color: "#cbd5e1", lineHeight: 1.7 }}>
          {sampleMission.scenario} — {sampleMission.objective}
        </p>
      </section>

      {result ? (
        <section className="card" style={{ padding: 24 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12, marginBottom: 18 }}>
            <h2 style={{ margin: 0 }}>AI strategy</h2>
            <span className="pill">{result.strategy || "Adaptive route optimization"}</span>
          </div>

          <p style={{ color: "#dbeafe", lineHeight: 1.8, marginBottom: 24 }}>{result.summary}</p>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: 18 }}>
            {result.decisions?.map((decision: any, index: number) => (
              <div key={index} style={{ padding: 18, borderRadius: 16, background: "rgba(15, 23, 42, 0.9)", border: "1px solid rgba(148,163,184,.2)" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, marginBottom: 12 }}>
                  <strong>Drone {index + 1}</strong>
                  <span style={{ color: decision.risk_level === "high" ? "#fca5a5" : decision.risk_level === "medium" ? "#fcd34d" : "#86efac", fontWeight: 700 }}>
                    {decision.risk_level}
                  </span>
                </div>
                <p style={{ margin: "0 0 8px", color: "#dbeafe" }}>{decision.rationale}</p>
                <ul style={{ margin: 0, paddingLeft: 18, color: "#cbd5e1", lineHeight: 1.8 }}>
                  <li>Action: {decision.action}</li>
                  <li>Recommended speed: {decision.recommended_speed} m/s</li>
                  <li>Recommended altitude: {decision.recommended_altitude} m</li>
                  <li>Confidence: {(decision.confidence * 100).toFixed(0)}%</li>
                </ul>
              </div>
            ))}
          </div>

          <div style={{ marginTop: 22, paddingTop: 20, borderTop: "1px solid rgba(148,163,184,.2)" }}>
            <h3 style={{ margin: "0 0 12px" }}>Route overview</h3>
            <pre style={{ margin: 0, whiteSpace: "pre-wrap", background: "rgba(2, 6, 23, 0.7)", padding: 16, borderRadius: 12, color: "#cbd5e1" }}>
              {JSON.stringify(result.route || [], null, 2)}
            </pre>
          </div>
        </section>
      ) : null}
    </main>
  );
}
