import React, { useState } from "react";
import Controls from "./components/Controls";
import ProcessTable from "./components/ProcessTable";
import Gantt from "./components/Gantt";
import { runMockSimulation } from "./utils/simulation";
import "./index.css";

export default function App() {
  const [algorithm, setAlgorithm] = useState("fcfs");
  const [mode, setMode] = useState("all");
  const [processes, setProcesses] = useState([
    { id: 0, arrival: 0, burst: 1 },
    { id: 1, arrival: 1, burst: 1 },
  ]);
  const [loading, setLoading] = useState(false);
  const [simulation, setSimulation] = useState(null);

  const addProcess = () => {
    const newId = processes.length
      ? Math.max(...processes.map((p) => p.id)) + 1
      : 0;
    setProcesses([...processes, { id: newId, arrival: 0, burst: 1 }]);
  };

  const clearProcesses = () => setProcesses([]);

  const removeProcess = (id) =>
    setProcesses(processes.filter((p) => p.id !== id));

  const updateProcess = (id, field, value) =>
    setProcesses(
      processes.map((p) => (p.id === id ? { ...p, [field]: value } : p)),
    );

  const runSimulation = async () => {
    setLoading(true);
    setSimulation(null);

    try {
      // Aqui você pode chamar a API real. Por agora usamos mock.
      const result = runMockSimulation(processes);
      // simula pequena latência
      setTimeout(() => {
        setSimulation(result);
        setLoading(false);
      }, 250);
    } catch (err) {
      console.error(err);
      setSimulation(runMockSimulation(processes));
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>Process Scheduler</h1>

      <Controls
        algorithm={algorithm}
        setAlgorithm={setAlgorithm}
        mode={mode}
        setMode={setMode}
        onAddProcess={addProcess}
        onClearProcesses={clearProcesses}
        onStart={runSimulation}
        loading={loading}
        processesCount={processes.length}
      />

      <h2>Processes</h2>

      <ProcessTable
        processes={processes}
        updateProcess={updateProcess}
        removeProcess={removeProcess}
      />

      <div style={{ marginTop: "1rem" }}>
        <Gantt timeline={simulation ? simulation.timeline : []} />
      </div>

      {simulation && (
        <div className="metrics">
          <div className="metric">
            <div className="metric-label">Avg Turnaround</div>
            <div className="metric-value">
              {simulation.metrics.avg_life.toFixed(2)}
            </div>
          </div>
          <div className="metric">
            <div className="metric-label">Avg Waiting</div>
            <div className="metric-value">
              {simulation.metrics.avg_wait.toFixed(2)}
            </div>
          </div>
          <div className="metric">
            <div className="metric-label">Context Switches</div>
            <div className="metric-value">
              {simulation.metrics.num_context_switch}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
