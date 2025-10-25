// src/utils/simulation.js
export function runMockSimulation(processes) {
  const procs = [...processes].sort(
    (a, b) => a.arrival - b.arrival || a.id - b.id,
  );
  let now = 0;
  const timeline = [];

  procs.forEach((p) => {
    const start = Math.max(now, p.arrival);
    const burst = Math.max(1, Math.floor(p.burst));
    const end = start + burst;
    timeline.push({ pid: p.id, start, end });
    now = end;
  });

  const n = processes.length || 1;
  const avg_life =
    timeline.reduce(
      (s, t) => s + (t.end - processes.find((x) => x.id === t.pid).arrival),
      0,
    ) / n;
  const avg_wait =
    timeline.reduce(
      (s, t) => s + (t.start - processes.find((x) => x.id === t.pid).arrival),
      0,
    ) / n;
  const num_context_switch = Math.max(0, timeline.length - 1);

  return { timeline, metrics: { avg_life, avg_wait, num_context_switch } };
}
