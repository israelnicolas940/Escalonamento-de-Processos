from typing import List, Dict, Tuple
from models import Task, TimeSlice, Timeline, Metrics


# Helper: transforma per-task slices em timeline global ordenada
def to_global_timeline(
    per_task: Dict[int, List[TimeSlice]],
) -> List[Timeline]:
    timeline: List[Tuple[int, int, int]] = []
    for pid, slices in per_task.items():
        for s in slices:
            timeline.append((s.start, s.end, pid))
    # ordenar por start, e em caso de empate por end asc
    timeline.sort(key=lambda t: t[0])
    # validar sobreposições ou mesclar slices consecutivas do mesmo pid
    merged: List[Timeline] = []
    for start, end, pid in timeline:
        if start >= end:
            raise ValueError(
                f"Invalid timeslice for pid {pid}: start >= end ({start} >= {end})"
            )
        if merged[-1].pid == pid and merged[-1].start_time == start:
            # mesclar fatias contíguas do mesmo pid
            merged[-1] = Timeline(merged[-1].pid, end, pid)
        else:
            merged.append(Timeline(pid, start, end))
    return merged


def compute_metrics(per_task: Dict[int, List[TimeSlice]], tasks: List[Task]) -> Metrics:
    if not tasks:
        return Metrics(0.0, 0.0, 0)

    # valida presença de todas as tasks no schedule
    for t in tasks:
        if t.pid not in per_task or not per_task[t.pid]:
            raise ValueError(f"Task pid={t.pid} has no timeslices in schedule")

    timeline = to_global_timeline(per_task)

    # context switches: contar transições de pid no timeline
    ctx_switches = 0
    prev_pid = None
    for _, _, pid in timeline:
        if prev_pid is not None and pid != prev_pid:
            ctx_switches += 1
        prev_pid = pid

    # avg turnaround (life) e avg wait
    total_life = 0
    total_wait = 0
    for t in tasks:
        slices = per_task[t.pid]
        # assumir slices ordenados por start; se não, ordene:
        slices = sorted(slices, key=lambda s: s.start)
        completion = slices[-1].end
        turnaround = completion - t.arrival
        total_life += turnaround

        # espera = (tempo até primeira execução) + lacunas entre fatias
        wait = max(0, slices[0].start - t.arrival)
        for i in range(len(slices) - 1):
            gap = slices[i + 1].start - slices[i].end
            if gap > 0:
                wait += gap
        total_wait += wait

    n = len(tasks)
    return Metrics(
        avg_life=total_life / n,
        avg_wait=total_wait / n,
        num_context_switch=ctx_switches,
    )
