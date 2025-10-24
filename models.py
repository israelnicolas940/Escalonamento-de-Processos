from typing import NamedTuple, Dict, List
from dataclasses import dataclass


# Tipos leves, imutáveis onde possível
class Timeline(NamedTuple):
    pid: int
    init_time: int
    end_time: int


class TimeSlice(NamedTuple):
    start: int
    end: int


@dataclass(frozen=True)
class Task:
    pid: int
    arrival: int
    proc_time: int


@dataclass(frozen=True)
class Metrics:
    avg_life: float
    avg_wait: float
    num_context_switch: int


@dataclass(frozen=True)
class Schedule:
    per_task: Dict[int, List[TimeSlice]]
    timeline: List[Timeline]
    metrics: Metrics
