from base import SchedulerAlgorithm, Scheduler, Task, TimeSlice
from copy import deepcopy
from typing import List, Dict
from pprint import pprint


class FirstComeFirstServed(SchedulerAlgorithm):
    def schedule(self, tasks_: List[Task]) -> Dict[int, List[TimeSlice]]:
        # Ordena as tarefas pela ordem de chegada
        tasks = deepcopy(tasks_)
        tasks_sorted = sorted(tasks, key=lambda t: t.arrival)
        timeline = 0
        schedule_map: Dict[int, List[TimeSlice]] = {}

        while tasks_sorted:
            task = tasks_sorted.pop(0)
            # O tempo atual deve ser no mínimo o tempo de chegada
            start_time = max(timeline, task.arrival)
            end_time = start_time + task.proc_time

            # Adiciona a execução da tarefa
            if task.pid not in schedule_map:
                schedule_map[task.pid] = []
            schedule_map[task.pid].append(TimeSlice(start_time, end_time))

            # Atualiza o tempo total
            timeline = end_time

        return schedule_map


def main():
    listTask = [
        Task(0, 0, 5, 2, 0),
        Task(1, 0, 2, 3, 0),
        Task(2, 1, 4, 1, 0),
        Task(3, 3, 3, 4, 0)
    ]

    algorithms = [FirstComeFirstServed()]

    for alg in algorithms:
        scheduler = Scheduler(listTask, alg)
        metrics = scheduler.schedule()

        print('Metrics:')
        pprint(metrics)
        print('\n')


if __name__ == "__main__":
    main()
