from processo import Processo
from utilidades import Calc_AvgWaitTime, Calc_AvgWaitTurn
from escalonadores import Scheduler_FCFS, Scheduler_SJF, Scheduler_SRTF, Scheduler_PrioSp, Scheduler_PrioCp, Scheduler_RRSp, Scheduler_RRCp

# Lendo o arquivo de configuração e obtendo...
arquivo_config = "config.txt"
try:
    with open(arquivo_config, "r", encoding="utf-8") as configuracao:
        tam_quantum = configuracao.readline().strip().split(':')[1] #... o tamanho do quantum e...
        aging = configuracao.readline().strip().strip().split(':')[1] #... o grau de envelhecimento
        print(tam_quantum, aging) # Teste (Apagar depois)
except FileNotFoundError:
    print(f"Erro: o arquivo", arquivo_config, "nao foi encontrado")   
except Exception as e:
    print(f"Ocorreu o seguinte erro: {e}")    

Processos = [] # Esse vetor armazenará todos os processos inseridos pelo usuário
i = 1
while True:
    entrada = input("").split() # Obtendo as entradas do usuário
    if not entrada:
        break # Se o usuário mandar uma linha vazia, ele para de ler as entradas
    Processos.append(Processo(int(entrada[0]), int(entrada[1]), int (entrada[2]), i))
    print(Processos[i - 1].pid)
    i += 1

Processos.sort(key=lambda p: p.time_crt)
Disponiveis = []
Terminados = []
cntxt_chngs = 0

print(Scheduler_RRCp(Processos, Disponiveis, Terminados, cntxt_chngs, tam_quantum, aging))
for p in Processos:
    print(p.pid, p.wait_time, p.end_time)
print(Calc_AvgWaitTime(Processos), Calc_AvgWaitTurn(Processos))
