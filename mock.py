from base import SchedulerAlgorithm
from models import TimeSlice, Task
from typing import List, Dict


class MockAlgorithm(SchedulerAlgorithm):
    def schedule(self, tasks: List[Task]) -> Dict[int, List[TimeSlice]]:
        """
        Retorna um mapa pid -> lista ordenada de TimeSlice
        TimeSlice: [first,second) onde first < second.
        Implementação deve:
            - Retornar slices sem sobreposição por pid.
            - Usar todos os pids presentes em tasks.
        """
        tasks_sorted = sorted(tasks, key=lambda t: t.arrival)
        current_time = 0
        schedule: Dict[int, List[TimeSlice]] = {}

        for task in tasks_sorted:
            start_time = max(current_time, task.arrival)
            end_time = start_time + task.proc_time
            schedule[task.pid] = [TimeSlice(start=start_time, end=end_time)]
            current_time = end_time

        return schedule
