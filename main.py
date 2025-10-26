from processo import Processo
from utilidades import Calc_AvgWaitTime, Calc_AvgWaitTurn, Plotar_diagrama
from escalonadores import Scheduler_FCFS, Scheduler_SJF, Scheduler_SRTF, Scheduler_PrioSp, Scheduler_PrioCp, Scheduler_RRSp, Scheduler_RRCp

# Lendo o arquivo de configuração e obtendo...
arquivo_config = "config.txt"
try:
    with open(arquivo_config, "r", encoding="utf-8") as configuracao:
        tam_quantum = configuracao.readline().strip().split(':')[1] #... o tamanho do quantum e...
        aging = configuracao.readline().strip().strip().split(':')[1] #... o grau de envelhecimento
except FileNotFoundError:
    print(f"Erro: o arquivo", arquivo_config, "nao foi encontrado")   
except Exception as e:
    print(f"Ocorreu o seguinte erro: {e}")    

print("Insira a descrição dos processos no formato: [Tempo de chegada] [Tempo de execução] [Prioridade].") 
print("OBS:Para parar de inserir processos, bastar apertar 'Enter' sem enviar nada)")

Processos = [] # Esse vetor armazenará todos os processos inseridos pelo usuário
i = 1
while True:
    entrada = input("").split() # Obtendo as entradas do usuário
    if not entrada:
        break # Se o usuário mandar uma linha vazia, ele para de ler as entradas
    Processos.append(Processo(int(entrada[0]), int(entrada[1]), int (entrada[2]), i))
    i += 1

algoritmo = input("Digite qual dos algoritmos gostaria de utilizar: \n1-Firsr Come, First Served(FCFS)\n2-Shortest" \
" Job First(SJF)\n3-Shortest Remaining Time First(SRTF)\n4-Por prioridade, sem preempção\n5-Por prioridade, com" \
"preempção por prioridade\n6-Round Robin com quantum, sem prioridade\n7-Round Robin com prioridade e envlhecimento\n")

Processos.sort(key=lambda p: p.time_crt) # Ordena os processos por ordem de criação
Disponiveis = [] # }
Terminados = []  # } iniciação de listas e variável que serão usadas pelos algoritmos
cntxt_chngs = 0  # }

# Identificar qual algoritmo o usuário escolheu
if(int(algoritmo) == 1):
    Timeline, trocas = Scheduler_FCFS(Processos, Disponiveis, Terminados, cntxt_chngs, tam_quantum, aging)
elif int(algoritmo) == 2:
    Timeline, trocas = Scheduler_SJF(Processos, Disponiveis, Terminados, cntxt_chngs, tam_quantum, aging)
elif int(algoritmo) == 3:
    Timeline, trocas = Scheduler_SRTF(Processos, Disponiveis, Terminados, cntxt_chngs, tam_quantum, aging)
elif int(algoritmo) == 4:
    Timeline, trocas = Scheduler_PrioSp(Processos, Disponiveis, Terminados, cntxt_chngs, tam_quantum, aging)
elif int(algoritmo) == 5:
    Timeline, trocas = Scheduler_PrioCp(Processos, Disponiveis, Terminados, cntxt_chngs, tam_quantum, aging)
elif int(algoritmo) == 6:
    Timeline, trocas = Scheduler_RRSp(Processos, Disponiveis, Terminados, cntxt_chngs, tam_quantum, aging)
elif int(algoritmo) == 7:
    Timeline, trocas = Scheduler_RRCp(Processos, Disponiveis, Terminados, cntxt_chngs, tam_quantum, aging)

print("Tempo médio de vida: ", Calc_AvgWaitTurn(Processos))
print("Tempo médio de espera: ", Calc_AvgWaitTime(Processos))
print("Número de trocas de contexto: ", trocas)
Plotar_diagrama(Timeline, Processos)
