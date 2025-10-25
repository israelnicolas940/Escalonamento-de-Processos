import React from "react";

/**
 * Exibe um Gantt Chart alinhado pelo tempo real.
 * Exemplo:
 * Tempo: 0---1---2---3---4---5---6
 *         [P1][   ][P2][P2][P3][  ]
 */
export default function Gantt({ timeline }) {
  if (!timeline || timeline.length === 0) return null;

  // Calcula tempo máximo (último fim)
  const maxTime = Math.max(...timeline.map((t) => t.end));
  const minTime = Math.min(...timeline.map((t) => t.start));
  const totalWidth = (maxTime - minTime + 1) * 40; // 40px = 1 unidade de tempo

  // Gera blocos posicionados proporcionalmente no eixo temporal
  const slots = timeline.map((t, i) => ({
    ...t,
    left: (t.start - minTime) * 40,
    width: (t.end - t.start) * 40,
  }));

  return (
    <div className="gantt">
      <div className="gantt-title">Execution Timeline</div>

      <div
        className="gantt-grid"
        style={{
          position: "relative",
          height: "60px",
          borderBottom: "1px solid rgba(255,255,255,0.1)",
          width: `${totalWidth}px`,
          overflowX: "auto",
        }}
      >
        {/* Barras */}
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

        {/* Eixo do tempo */}
        <div
          style={{
            position: "absolute",
            top: "50px",
            display: "flex",
            fontSize: "11px",
            color: "var(--muted)",
          }}
        >
          {Array.from({ length: maxTime - minTime + 1 }, (_, i) => (
            <div
              key={i}
              style={{
                width: "40px",
                textAlign: "center",
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
