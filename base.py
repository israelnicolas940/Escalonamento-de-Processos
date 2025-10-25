from _typeshed import SupportsRichComparison
from typing import List, Dict
from dataclasses import dataclass
from abc import ABC, abstractmethod
import metrics


@dataclass
class Task:
    pid: int
    arrival: int
    proc_time: int
    priority: int
    aging: int


@dataclass
class TimeSlice:
    first: int
    second: int


class SchedulerAlgorithm(ABC):
    @abstractmethod
    def schedule(self, tasks: List[Task]) -> Dict[int, List[TimeSlice]]:
        """
        Retorna um mapa pid -> lista ordenada de TimeSlice
        TimeSlice: [first,second) onde first < second.
        Implementação deve:
            - Retornar slices sem sobreposição por pid.
            - Usar todos os pids presentes em tasks.
        """
        raise NotImplementedError


class Scheduler:
    def __init__(self, tasks: List[Task], scheduler_algorithm: SchedulerAlgorithm):
        self.tasks = tasks
        self.algorithm = scheduler_algorithm

    def setAlgorithm(self, new_algorithm: SchedulerAlgorithm):
        self.algorithm = new_algorithm

    def schedule(self):
        schedule_res = self.algorithm.schedule(self.tasks)

        metrics_res: metrics.Metrics = metrics.compute_metrics(schedule_res, self.tasks)
        return (metrics_res, metrics.to_global_timeline(schedule_res))
