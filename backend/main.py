from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import sys

sys.path.append("/app/shared")

from base import Scheduler
from mock import MockAlgorithm
from models import Task

app = FastAPI(title="Process Scheduler API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProcessInput(BaseModel):
    pid: int
    arrival: int
    proc_time: int


class ScheduleRequest(BaseModel):
    algorithm: str
    quantum: int
    processes: List[ProcessInput]


class ScheduleResponse(BaseModel):
    ganttChart: List[Dict]
    metrics: Dict
    timeline: List[Dict]


@app.get("/")
async def root():
    return {"message": "Process Scheduler API"}


@app.get("/api/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/schedule", response_model=ScheduleResponse)
async def schedule_processes(request: ScheduleRequest):
    try:
        # Converter input para Task objects
        tasks = [
            Task(pid=p.pid, arrival=p.arrival, proc_time=p.proc_time)
            for p in request.processes
        ]

        if not tasks:
            raise HTTPException(status_code=400, detail="No processes provided")

        # Por enquanto, usar apenas MockAlgorithm (FCFS)
        algorithm = MockAlgorithm()
        scheduler = Scheduler(tasks=tasks, scheduler_algorithm=algorithm)

        metrics, timeline = scheduler.schedule()

        # Converter timeline para Gantt chart no formato Maziero
        if not timeline:
            raise HTTPException(status_code=500, detail="Schedule failed")

        max_time = max(t.end_time for t in timeline)
        gantt_chart = []

        for t in range(max_time):
            row = {"time": t}
            for task in tasks:
                # Verificar se o processo está executando neste instante
                is_running = any(
                    slot.pid == task.pid and t >= slot.start_time and t < slot.end_time
                    for slot in timeline
                )
                row[f"P{task.pid}"] = "##" if is_running else "--"
            gantt_chart.append(row)

        return {
            "ganttChart": gantt_chart,
            "metrics": {
                "avg_life": metrics.avg_life,
                "avg_wait": metrics.avg_wait,
                "num_context_switch": metrics.num_context_switch,
            },
            "timeline": [
                {"pid": t.pid, "start": t.start_time, "end": t.end_time}
                for t in timeline
            ],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
