import React, { useState } from "react";
import Controls from "./components/Controls";
import ProcessTable from "./components/ProcessTable";
import Gantt from "./components/Gantt";
import { runMockSimulation } from "./utils/simulation";
import "./index.css";

export default function App() {
  const [algorithm, setAlgorithm] = useState("fcfs");
  const [quantum, setQuantum] = useState(2);
  const [aging, setAging] = useState(1);
  const [processes, setProcesses] = useState([
    { id: 0, arrival: 0, burst: 5, priority: 2 },
    { id: 1, arrival: 0, burst: 2, priority: 3 },
    { id: 2, arrival: 1, burst: 4, priority: 1 },
    { id: 3, arrival: 3, burst: 3, priority: 4 },
  ]);
  const [loading, setLoading] = useState(false);
  const [simulation, setSimulation] = useState(null);
  const [error, setError] = useState(null);

  const addProcess = () => {
    const newId = processes.length
      ? Math.max(...processes.map((p) => p.id)) + 1
      : 0;
    setProcesses([
      ...processes,
      { id: newId, arrival: 0, burst: 1, priority: 0 },
    ]);
  };

  const clearProcesses = () => {
    setProcesses([]);
    setSimulation(null);
    setError(null);
  };

  const removeProcess = (id) => {
    setProcesses(processes.filter((p) => p.id !== id));
  };

  const updateProcess = (id, field, value) => {
    setProcesses(
      processes.map((p) =>
        p.id === id ? { ...p, [field]: parseInt(value) || 0 } : p,
      ),
    );
  };

  const serializeProcesses = (procs) =>
    procs.map((p) => ({
      pid: p.id,
      arrival: Number(p.arrival),
      proc_time: Number(p.burst),
      priority: Number(p.priority) || 0,
    }));

  const runSimulation = async () => {
    setLoading(true);
    setSimulation(null);
    setError(null);

    const payload = {
      algorithm,
      quantum,
      aging,
      processes: serializeProcesses(processes),
    };

    console.log("Enviando payload:", payload);

    try {
      const apiUrl = process.env.REACT_APP_API_URL || "http://localhost";
      const response = await fetch(`${apiUrl}/api/schedule`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      console.log("Response received:", response.status);

      if (!response.ok) {
        let errorText;
        try {
          const errorData = await response.json();
          errorText = errorData.detail || `HTTP ${response.status}`;
        } catch {
          errorText = await response.text();
        }
        throw new Error(`Backend error: ${errorText}`);
      }

      const data = await response.json();
      console.log("Resposta do backend:", data);
      setSimulation(data);
    } catch (err) {
      console.error("Erro na simulação:", err);
      setError(err.message);

      // Fallback para simulação mock
      console.log("Usando simulação mock como fallback");
      const mockResult = runMockSimulation(processes);
      setSimulation(mockResult);
    } finally {
      setLoading(false);
    }
  };

  // Verificar se algoritmo precisa de quantum
  const needsQuantum = ["rr", "rra"].includes(algorithm);
  const needsPriority = ["pd", "pc", "pp", "rra"].includes(algorithm);

  return (
    <div className="app-container">
      <h1>Process Scheduler</h1>

      <Controls
        algorithm={algorithm}
        setAlgorithm={setAlgorithm}
        quantum={quantum}
        setQuantum={setQuantum}
        aging={aging}
        setAging={setAging}
        needsQuantum={needsQuantum}
        onAddProcess={addProcess}
        onClearProcesses={clearProcesses}
        onStart={runSimulation}
        loading={loading}
        processesCount={processes.length}
      />

      {error && (
        <div
          style={{
            background: "rgba(255, 90, 106, 0.1)",
            border: "1px solid rgba(255, 90, 106, 0.3)",
            borderRadius: "8px",
            padding: "12px",
            marginTop: "16px",
            color: "#ff5a6a",
          }}
        >
          <strong>Erro:</strong> {error}
        </div>
      )}

      <h2>Processes</h2>

      <ProcessTable
        processes={processes}
        updateProcess={updateProcess}
        removeProcess={removeProcess}
        needsPriority={needsPriority}
      />

      {simulation && (
        <>
          <div className="metrics">
            <div className="metric">
              <div className="metric-label">Tempo médio de vida</div>
              <div className="metric-value">
                {simulation.metrics.avg_life.toFixed(2)}
              </div>
            </div>
            <div className="metric">
              <div className="metric-label">Tempo médio de espera</div>
              <div className="metric-value">
                {simulation.metrics.avg_wait.toFixed(2)}
              </div>
            </div>
            <div className="metric">
              <div className="metric-label">Trocas de Contexto</div>
              <div className="metric-value">
                {simulation.metrics.num_context_switch}
              </div>
            </div>
          </div>

          <div className="gantt">
            <h2>Diagrama</h2>
            <Gantt
              timeline={simulation.timeline}
              processes={processes}
              ganttChart={simulation.ganttChart}
            />
          </div>
        </>
      )}
    </div>
  );
}
