import React, { useState } from 'react';
import { PlusCircle, XCircle } from 'lucide-react';

export default function ProcessSchedulerUI() {
  const [algorithm, setAlgorithm] = useState('round-robin');
  const [mode, setMode] = useState('all-at-once');
  const [quantum, setQuantum] = useState(4);
  const [processes, setProcesses] = useState(() => {
    // default 6 processes like your screenshot
    return Array.from({ length: 6 }).map((_, i) => ({ id: i, arrival: i < 2 ? 1 : 0, burst: 1 }));
  });

  function addProcess() {
    setProcesses(prev => [...prev, { id: prev.length, arrival: 0, burst: 1 }]);
  }

  function removeProcess() {
    setProcesses(prev => prev.slice(0, Math.max(0, prev.length - 1)));
  }

  function updateProcess(idx, key, value) {
    setProcesses(prev => {
      const copy = [...prev];
      copy[idx] = { ...copy[idx], [key]: value };
      return copy;
    });
  }

  function startSimulation() {
    // placeholder: wire this to your backend or simulation runner
    const payload = { algorithm, mode, quantum, processes };
    console.log('Starting simulation with', payload);
    alert('Simulation started — check console for payload');
  }

  return (
    <div className="min-h-screen bg-[#1f2430] text-[#f3f4f6] flex items-start justify-center p-8">
      <div className="w-full max-w-3xl">
        <header className="text-center mb-8">
          <h1 className="text-3xl font-semibold">Process Scheduler</h1>
        </header>

        <section className="space-y-6 bg-[#2b2f37] p-8 rounded-2xl shadow-lg">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3 items-center">
            <label className="text-sm text-[#cbd5e1]">Algorithm</label>
            <select
              value={algorithm}
              onChange={e => setAlgorithm(e.target.value)}
              className="sm:col-span-2 bg-[#22252b] border border-[#3a3f47] rounded-lg py-3 px-4 focus:outline-none"
            >
              <option value="round-robin">Round Robin</option>
              <option value="fcfs">FCFS</option>
              <option value="sjf">SJF</option>
              <option value="priority">Priority</option>
            </select>

            <label className="text-sm text-[#cbd5e1]">Mode</label>
            <select
              value={mode}
              onChange={e => setMode(e.target.value)}
              className="sm:col-span-2 bg-[#22252b] border border-[#3a3f47] rounded-lg py-3 px-4 focus:outline-none"
            >
              <option value="all-at-once">All at once</option>
              <option value="streaming">Streaming</option>
            </select>

            <label className="text-sm text-[#cbd5e1]">Quantum</label>
            <input
              type="number"
              min={1}
              value={quantum}
              onChange={e => setQuantum(Math.max(1, Number(e.target.value || 1)))}
              className="sm:col-span-2 bg-[#22252b] border border-[#3a3f47] rounded-lg py-3 px-4 w-full"
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-medium">Processes</h2>
              <div className="flex gap-3">
                <button
                  onClick={addProcess}
                  className="flex items-center gap-2 bg-pink-400 hover:bg-pink-300 text-black rounded-full p-2"
                  aria-label="add"
                >
                  <PlusCircle size={18} />
                </button>
                <button
                  onClick={removeProcess}
                  className="flex items-center gap-2 bg-red-400 hover:bg-red-300 text-black rounded-full p-2"
                  aria-label="remove"
                >
                  <XCircle size={18} />
                </button>
              </div>
            </div>

            <div className="grid gap-3">
              {processes.map((p, idx) => (
                <div
                  key={p.id}
                  className="grid grid-cols-12 gap-3 items-center bg-[#23262b] border border-[#33373d] rounded-xl p-3"
                >
                  <div className="col-span-1 flex items-center justify-center bg-[#151719] rounded-lg h-10">
                    <span className="text-sm text-[#9aa4b2]">{p.id}</span>
                  </div>

                  <div className="col-span-5">
                    <label className="block text-xs text-[#9aa4b2] mb-1">Arrival Time</label>
                    <input
                      type="number"
                      min={0}
                      value={p.arrival}
                      onChange={e => updateProcess(idx, 'arrival', Number(e.target.value || 0))}
                      className="w-full bg-transparent border border-[#3a3f47] rounded-md px-3 py-2 focus:outline-none"
                    />
                  </div>

                  <div className="col-span-6">
                    <label className="block text-xs text-[#9aa4b2] mb-1">Burst Time</label>
                    <input
                      type="number"
                      min={1}
                      value={p.burst}
                      onChange={e => updateProcess(idx, 'burst', Math.max(1, Number(e.target.value || 1)))}
                      className="w-full bg-transparent border border-[#3a3f47] rounded-md px-3 py-2 focus:outline-none"
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-4">
            <button
              onClick={startSimulation}
              className="w-full bg-pink-400 hover:bg-pink-300 text-black font-semibold py-3 rounded-xl shadow-md"
            >
              START SIMULATION
            </button>
          </div>
        </section>
      </div>
    </div>
  );
}

