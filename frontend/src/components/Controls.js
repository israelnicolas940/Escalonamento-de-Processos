import React from "react";

export default function Controls({
  algorithm,
  setAlgorithm,
  mode,
  setMode,
  onAddProcess,
  onClearProcesses,
  onStart,
  loading,
  processesCount,
}) {
  return (
    <div className="controls">
      <div className="control-row">
        <label>
          Algorithm
          <select
            value={algorithm}
            onChange={(e) => setAlgorithm(e.target.value)}
          >
            <option value="fcfs">First Come First Served</option>
            <option value="sjf">Shortest Job First</option>
            <option value="srtf">Shortest Remaining Time First</option>
            <option value="rr">Round Robin</option>
          </select>
        </label>

        <label>
          Mode
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="all">All at once</option>
            <option value="step">Step by step</option>
          </select>
        </label>
      </div>

      <div className="control-row actions">
        <div className="left-actions">
          <button
            type="button"
            onClick={onAddProcess}
            className="btn-add"
            title="Add process"
          >
            +
          </button>
          <button
            type="button"
            onClick={onClearProcesses}
            className="btn-clear"
            title="Clear all"
          >
            ×
          </button>
        </div>

        <button
          className="start-btn"
          onClick={onStart}
          disabled={loading || !processesCount}
          title="Start simulation"
        >
          {loading ? "RUNNING..." : "START SIMULATION"}
        </button>
      </div>
    </div>
  );
}
