from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from shared.algorithm import (
    FirstComeFirstServed,
    PriorityNonPreemptive,
    PriorityPreemptive,
    RoundRobin,
    RoundRobinPriorityAging,
    ShortestJobFirst,
    ShortestRemainingTimeFirst,
)
from shared.base import Scheduler
from shared.models import Task

app = FastAPI(title="Process Scheduler API")

# Configuração CORS - deve vir ANTES das rotas
# Permitir requisições vindas do Traefik/frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique o domínio exato
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProcessInput(BaseModel):
    pid: int
    arrival: int
    proc_time: int
    priority: Optional[int] = 0


class ScheduleRequest(BaseModel):
    algorithm: str
    quantum: Optional[int] = 2
    aging: Optional[int] = 1
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
        print("CHECKPOINT 1: Recebendo requisição")
        print(f"Algorithm: {request.algorithm}")
        print(f"Processes: {request.processes}")

        tasks = [
            Task(
                pid=p.pid,
                arrival=p.arrival,
                proc_time=p.proc_time,
                priority=p.priority if p.priority is not None else 0,
            )
            for p in request.processes
        ]

        if not tasks:
            raise HTTPException(status_code=400, detail="No processes provided")

        print(f"CHECKPOINT 2: {len(tasks)} tasks criadas")

        # Selecionar algoritmo baseado no request
        algorithm_map = {
            "fcfs": FirstComeFirstServed(),
            "sjf": ShortestJobFirst(),
            "srtf": ShortestRemainingTimeFirst(),
            "pc": PriorityNonPreemptive(),  # Prioridade Cooperativo
            "pp": PriorityPreemptive(),  # Prioridade Preemptivo
            "rr": RoundRobin(quantum=request.quantum),
            "rra": RoundRobinPriorityAging(
                quantum=request.quantum, aging=request.aging
            ),
        }

        print("CHECKPOINT 3: Selecionando algoritmo")

        algorithm = algorithm_map.get(request.algorithm)
        if not algorithm:
            raise HTTPException(
                status_code=400, detail=f"Unknown algorithm: {request.algorithm}"
            )

        print(f"CHECKPOINT 4: Criando scheduler com algoritmo {request.algorithm}")
        scheduler = Scheduler(tasks=tasks, scheduler_algorithm=algorithm)

        print("CHECKPOINT 5: Executando schedule")
        metrics, timeline = scheduler.schedule()

        print(f"CHECKPOINT 6: Schedule completo. Timeline length: {len(timeline)}")

        # Converter timeline para Gantt chart no formato Maziero
        if not timeline:
            raise HTTPException(status_code=500, detail="Schedule failed")

        max_time = max(t.end_time for t in timeline)
        gantt_chart = []

        for t in range(max_time):
            row = {"time": t}
            for task in tasks:
                is_running = any(
                    slot.pid == task.pid and t >= slot.start_time and t < slot.end_time
                    for slot in timeline
                )
                row[f"P{task.pid}"] = "##" if is_running else "--"
            gantt_chart.append(row)

        print("CHECKPOINT 7: Gantt chart criado, retornando resposta")

        response_data = {
            "ganttChart": gantt_chart,
            "metrics": {
                "avg_life": float(metrics.avg_life),
                "avg_wait": float(metrics.avg_wait),
                "num_context_switch": int(metrics.num_context_switch),
            },
            "timeline": [
                {"pid": int(t.pid), "start": int(t.start_time), "end": int(t.end_time)}
                for t in timeline
            ],
        }

        print("CHECKPOINT 8: Resposta preparada, enviando...")
        return response_data

    except HTTPException:
        raise
    except Exception as e:
        import traceback

        print("ERRO COMPLETO:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
