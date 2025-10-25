from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
import metrics
from models import Metrics, Task, TimeSlice, Timeline


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
        self._algorithm = scheduler_algorithm

    @property
    def algorithm(self) -> SchedulerAlgorithm:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm: SchedulerAlgorithm) -> None:
        self._algorithm = algorithm

    def schedule(self) -> Tuple[Metrics, List[Timeline]]:
        schedule_res = self.algorithm.schedule(self.tasks)

        metrics_res: Metrics = metrics.compute_metrics(schedule_res, self.tasks)
        return (metrics_res, metrics.to_global_timeline(schedule_res))
