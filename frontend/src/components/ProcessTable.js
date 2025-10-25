import React from "react";

export default function ProcessTable({
  processes,
  updateProcess,
  removeProcess,
}) {
  return (
    <div className="process-section">
      <div className="table-header grid-cols-3">
        <div>Id</div>
        <div>Arrival Time</div>
        <div>Burst Time</div>
      </div>

      <div className="process-list">
        {processes.length === 0 && (
          <div className="empty-note">No processes. Click + to add.</div>
        )}
        {processes.map((proc) => (
          <div key={proc.id} className="table-row grid-cols-3">
            <div className="pid">{proc.id}</div>

            <input
              type="number"
              min="0"
              value={proc.arrival}
              onChange={(e) =>
                updateProcess(proc.id, "arrival", +e.target.value)
              }
            />

            <div className="burst-cell">
              <input
                type="number"
                min="1"
                value={proc.burst}
                onChange={(e) =>
                  updateProcess(proc.id, "burst", +e.target.value)
                }
              />
              <button
                className="btn-remove"
                onClick={() => removeProcess(proc.id)}
                title="Remove process"
              >
                ×
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
