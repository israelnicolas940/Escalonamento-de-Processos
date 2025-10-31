import React from "react";

export default function Controls({
  algorithm,
  setAlgorithm,
  quantum,
  setQuantum,
  aging,
  setAging,
  needsQuantum,
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
          Algoritmo
          <select
            value={algorithm}
            onChange={(e) => setAlgorithm(e.target.value)}
          >
            <option value="fcfs">First Come First Served (FCFS)</option>
            <option value="sjf">Shortest Job First (SJF)</option>
            <option value="srtf">Shortest Remaining Time First (SRTF)</option>
            <option value="pc">Prioridade Cooperativo (Não-preemptivo)</option>
            <option value="pp">Prioridade Preemptivo</option>
            <option value="rr">Round Robin (RR)</option>
            <option value="rra">Round Robin com Envelhecimento</option>
          </select>
        </label>

        {needsQuantum && (
          <label>
            Quantum
            <input
              type="number"
              min="1"
              value={quantum}
              onChange={(e) => setQuantum(parseInt(e.target.value) || 1)}
            />
          </label>
        )}

        {algorithm === "rra" && (
          <label>
            Aging (Envelhecimento)
            <input
              type="number"
              min="0"
              value={aging}
              onChange={(e) => setAging(parseInt(e.target.value) || 0)}
            />
          </label>
        )}
      </div>

      <div className="actions">
        <div className="left-actions">
          <button
            type="button"
            onClick={onAddProcess}
            className="btn-add"
            title="Adicionar processo"
          >
            +
          </button>
          <button
            type="button"
            onClick={onClearProcesses}
            className="btn-clear"
            title="Limpar tudo"
          >
            ×
          </button>
        </div>

        <button
          className="start-btn"
          onClick={onStart}
          disabled={loading || !processesCount}
        >
          {loading ? "EXECUTANDO..." : "COMEÇAR SIMULAÇÃO"}
        </button>
      </div>
    </div>
  );
}
