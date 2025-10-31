// src/components/ProcessTable.js
import React from "react";

export default function ProcessTable({
  processes,
  updateProcess,
  removeProcess,
}) {
  return (
    <div className="process-section">
      <div className="table-header">
        <div>PID</div>
        <div>Ingresso</div>
        <div>Duração</div>
        <div>Prioridade</div>
        <div></div>
      </div>

      <div className="process-list">
        {processes.map((p) => (
          <div className="table-row" key={p.id}>
            <div className="pid">P{p.id}</div>

            <input
              type="number"
              value={p.arrival}
              min="0"
              onChange={(e) => updateProcess(p.id, "arrival", e.target.value)}
            />

            <input
              type="number"
              value={p.burst}
              min="1"
              onChange={(e) => updateProcess(p.id, "burst", e.target.value)}
            />

            <input
              type="number"
              value={p.priority ?? 0}
              min="0"
              onChange={(e) => updateProcess(p.id, "priority", e.target.value)}
            />

            <button className="btn-remove" onClick={() => removeProcess(p.id)}>
              ✕
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
