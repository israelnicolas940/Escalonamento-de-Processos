from typing import List, Dict
from collections import deque
from math import ceil

from .base import SchedulerAlgorithm
from .models import TimeSlice, Task


class FirstComeFirstServed(SchedulerAlgorithm):
    def schedule(self, tasks: List[Task]) -> Dict[int, List[TimeSlice]]:
        tasks_sorted = sorted(tasks, key=lambda t: t.arrival)
        timeline = 0
        schedule_map: Dict[int, List[TimeSlice]] = {}

        for task in tasks_sorted:
            start_time = max(timeline, task.arrival)
            end_time = start_time + task.proc_time
            schedule_map.setdefault(task.pid, []).append(
                TimeSlice(start_time, end_time)
            )
            timeline = end_time

        return schedule_map


class ShortestJobFirst(SchedulerAlgorithm):
    def schedule(self, tasks: List[Task]) -> Dict[int, List[TimeSlice]]:
        tasks = sorted(tasks, key=lambda t: t.arrival)
        schedule_map: Dict[int, List[TimeSlice]] = {}
        timeline = 0
        remaining = tasks.copy()

        while remaining:
            available = [t for t in remaining if t.arrival <= timeline]

            if not available:
                timeline = remaining[0].arrival
                continue

            current = min(available, key=lambda t: t.proc_time)
            start_time = timeline
            end_time = start_time + current.proc_time
            schedule_map[current.pid] = [TimeSlice(start_time, end_time)]

            timeline = end_time
            remaining.remove(current)

        return schedule_map


class ShortestRemainingTimeFirst(SchedulerAlgorithm):
    def schedule(self, tasks: List[Task]) -> Dict[int, List[TimeSlice]]:
        tasks = sorted(tasks, key=lambda t: t.arrival)
        remaining_time = {t.pid: t.proc_time for t in tasks}
        schedule_map: Dict[int, List[TimeSlice]] = {t.pid: [] for t in tasks}

        time = 0
        completed = 0
        current_pid = None
        start_time = None

        while completed < len(tasks):
            available = [
                t for t in tasks if t.arrival <= time and remaining_time[t.pid] > 0
            ]

            if not available:
                time += 1
                continue

            current_task = min(available, key=lambda t: remaining_time[t.pid])
            pid = current_task.pid

            if current_pid != pid:
                if current_pid is not None and start_time is not None:
                    schedule_map[current_pid].append(TimeSlice(start_time, time))
                start_time = time
                current_pid = pid

            remaining_time[pid] -= 1
            time += 1

            if remaining_time[pid] == 0:
                schedule_map[pid].append(TimeSlice(start_time, time))
                completed += 1
                current_pid = None
                start_time = None

        return schedule_map


class PriorityNonPreemptive(SchedulerAlgorithm):
    def schedule(self, tasks: List[Task]) -> Dict[int, List[TimeSlice]]:
        tasks = sorted(tasks, key=lambda t: t.arrival)
        schedule_map: Dict[int, List[TimeSlice]] = {}
        timeline = 0
        remaining = tasks.copy()

        while remaining:
            available = [t for t in remaining if t.arrival <= timeline]

            if not available:
                timeline = remaining[0].arrival
                continue

            current = max(available, key=lambda t: getattr(t, "priority", 0))
            start_time = timeline
            end_time = start_time + current.proc_time
            schedule_map[current.pid] = [TimeSlice(start_time, end_time)]

            timeline = end_time
            remaining.remove(current)

        return schedule_map


class PriorityPreemptive(SchedulerAlgorithm):
    def schedule(self, tasks: List[Task]) -> Dict[int, List[TimeSlice]]:
        tasks = sorted(tasks, key=lambda t: t.arrival)
        remaining_time = {t.pid: t.proc_time for t in tasks}
        schedule_map: Dict[int, List[TimeSlice]] = {t.pid: [] for t in tasks}

        time = 0
        completed = 0
        current_pid = None
        start_time = None

        while completed < len(tasks):
            available = [
                t for t in tasks if t.arrival <= time and remaining_time[t.pid] > 0
            ]

            if not available:
                time += 1
                continue

            current_task = max(available, key=lambda t: getattr(t, "priority", 0))
            pid = current_task.pid

            if current_pid != pid:
                if current_pid is not None and start_time is not None:
                    schedule_map[current_pid].append(TimeSlice(start_time, time))
                start_time = time
                current_pid = pid

            remaining_time[pid] -= 1
            time += 1

            if remaining_time[pid] == 0:
                schedule_map[pid].append(TimeSlice(start_time, time))
                completed += 1
                current_pid = None
                start_time = None

        return schedule_map


class RoundRobin(SchedulerAlgorithm):
    def __init__(self, quantum: int):
        self.quantum = quantum

    def schedule(self, tasks: List[Task]) -> Dict[int, List[TimeSlice]]:
        tasks = sorted(tasks, key=lambda t: t.arrival)
        schedule_map: Dict[int, List[TimeSlice]] = {t.pid: [] for t in tasks}

        ready_queue = deque()
        time = 0
        remaining = {t.pid: t.proc_time for t in tasks}
        tasks_copy = tasks.copy()

        while ready_queue or tasks_copy:
            while tasks_copy and tasks_copy[0].arrival <= time:
                ready_queue.append(tasks_copy.pop(0))

            if not ready_queue:
                time = tasks_copy[0].arrival
                ready_queue.append(tasks_copy.pop(0))
                continue

            current = ready_queue.popleft()
            start_time = time
            exec_time = min(self.quantum, remaining[current.pid])
            end_time = time + exec_time

            schedule_map[current.pid].append(TimeSlice(start_time, end_time))
            remaining[current.pid] -= exec_time
            time = end_time

            while tasks_copy and tasks_copy[0].arrival <= time:
                ready_queue.append(tasks_copy.pop(0))

            if remaining[current.pid] > 0:
                ready_queue.append(current)

        return schedule_map


class RoundRobinPriorityAging(SchedulerAlgorithm):
    def __init__(self, quantum: int, aging: int = 1):
        self.quantum = quantum
        self.aging = aging

    def schedule(self, tasks: List[Task]) -> Dict[int, List[TimeSlice]]:
        tasks = sorted(tasks, key=lambda t: t.arrival)
        schedule_map: Dict[int, List[TimeSlice]] = {t.pid: [] for t in tasks}

        ready_queue = deque()
        time = 0
        remaining = {t.pid: t.proc_time for t in tasks}
        tasks_copy = tasks.copy()

        while ready_queue or tasks_copy:
            while tasks_copy and tasks_copy[0].arrival <= time:
                ready_queue.append(tasks_copy.pop(0))

            if not ready_queue:
                time = tasks_copy[0].arrival
                ready_queue.append(tasks_copy.pop(0))
                continue

            ready_queue = deque(
                sorted(
                    ready_queue, key=lambda t: getattr(t, "priority", 0), reverse=True
                )
            )

            current = ready_queue.popleft()
            start_time = time
            exec_time = min(self.quantum, remaining[current.pid])
            end_time = time + exec_time

            num_quantums = ceil(exec_time / self.quantum)
            for task in ready_queue:
                task.priority = getattr(task, "priority", 0) + self.aging * num_quantums

            schedule_map[current.pid].append(TimeSlice(start_time, end_time))
            remaining[current.pid] -= exec_time
            time = end_time

            while tasks_copy and tasks_copy[0].arrival <= time:
                ready_queue.append(tasks_copy.pop(0))

            if remaining[current.pid] > 0:
                ready_queue.append(current)

        return schedule_map
