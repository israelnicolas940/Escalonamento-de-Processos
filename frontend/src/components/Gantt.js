import React from "react";

export default function Gantt({ timeline }) {
  if (!timeline || timeline.length === 0) return null;

  // Always start at time 0
  const minTime = 0;
  const maxTime = Math.max(...timeline.map((t) => t.end));
  const unitWidth = 60; // pixels per time unit

  // Map bars
  const slots = timeline.map((t) => ({
    ...t,
    left: t.start * unitWidth,
    width: (t.end - t.start) * unitWidth,
  }));

  return (
    <div className="gantt">
      <div className="gantt-title">Execution Timeline</div>

      <div
        className="gantt-grid"
        style={{
          position: "relative",
          height: "80px",
          borderBottom: "1px solid rgba(255,255,255,0.1)",
          overflowX: "auto",
          whiteSpace: "nowrap",
          paddingBottom: "10px",
        }}
      >
        {/* Bars */}
        {slots.map((slot, i) => (
          <div
            key={i}
            className="gantt-bar"
            style={{
              position: "absolute",
              left: `${slot.left}px`,
              width: `${slot.width}px`,
              height: "40px",
              background: "linear-gradient(90deg,#ff7ab6,#8b5cf6)",
              color: "#071024",
              borderRadius: "6px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 600,
              fontSize: "13px",
              top: "10px",
            }}
            title={`P${slot.pid} [${slot.start}-${slot.end}]`}
          >
            P{slot.pid}
          </div>
        ))}

        {/* Time axis — perfectly aligned at edges */}
        <div
          style={{
            position: "absolute",
            top: "55px",
            left: 0,
            display: "flex",
            fontSize: "11px",
            color: "rgba(255,255,255,0.7)",
          }}
        >
          {Array.from({ length: maxTime - minTime + 1 }, (_, i) => (
            <div
              key={i}
              style={{
                width: `${unitWidth}px`,
                textAlign: "left",
              }}
            >
              {minTime + i}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
