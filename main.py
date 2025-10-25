# Classe Processo
class Processo:
    def __init__(self, time_crt, time_exec, prior, pos):
        self.time_crt = time_crt # Tempo de criação do processo
        self.time_exec = time_exec # Tempo de execução restante
        self.prior = prior # Prioridade do processo
        self.wait_time = 0 # Tempo de espera do processo
        self.time_rmng= time_exec # Tempo restante para terminar a execução
        self.end_time = -1 # Tempo em que o processo acabou
        self.pid = "P" + str(pos) # Nome do processo

# Função que computa a espera de todos os processos disponíveis, mas que não executaram
def Waiting(Disponiveis, Terminados, pid):
    for p in Disponiveis:
        if(p.pid != pid and p not in Terminados):
            p.wait_time += 1

def Scheduler_FCFS(Processos, Disponiveis, Terminados):
    time = 0 # Tempo inicial
    Timeline = [] # Linha do tempo especificando qual processo executou em dado momento
    while(len(Processos) > len(Terminados)): # Enquanto existirem processos inacabados...
        for p in Processos:
            if(p.time_crt <= time and p not in Disponiveis and p not in Terminados):
                Disponiveis.append(p) # Se o a data de criação for menor que o tempo atual, o 
                                      # O processo torna-se disponível

        if(len(Disponiveis) == 0):
            Timeline.append("-") # Para o caso de ainda não terem sido criados processos
            time += 1
            continue
        
        proc_atual = Disponiveis.pop(0) # Escolhe-se o primeiro processo que chegou
        while(proc_atual.time_rmng > 0):
            for p in Processos: # Sempre checa se novos processos estão disponíveis
                if(p.time_crt <= time and p not in Disponiveis and p not in Terminados):
                    Disponiveis.append(p)

            proc_atual.time_rmng -= 1 # desconta-se 1 do tempo restante para encerrar o processo escolhido
            Waiting(Disponiveis, Terminados, proc_atual.pid) # Todos os processos disponíveis que não estão executando, esperam
            Timeline.append(proc_atual.pid) # Adiciona-se à linha do tempo o processo que executou
            time += 1
            if(proc_atual.time_rmng == 0): # Se o processo acabou...
                proc_atual.end_time = time # Obtemos seu tempo de finalização e...
                Terminados.append(proc_atual) # Adicionamos ele à lista de terminados
    return Timeline

def Scheduler_SJF(Processos, Disponiveis, Terminados):
    time = 0 # Tempo inicial
    Timeline = [] # Linha do tempo especificando qual processo executou em dado momento
    while(len(Processos) > len(Terminados)): # Enquanto existirem processos inacabados...
        for p in Processos:
            if(p.time_crt <= time and p not in Disponiveis and p not in Terminados):
                Disponiveis.append(p) # Se o a data de criação for menor que o tempo atual, o 
                                      # O processo torna-se disponível

        if(len(Disponiveis) == 0):
            Timeline.append("-") # Para o caso de ainda não terem sido criados processos
            time += 1
            continue
        
        # Escolhe o processo de menor duração e o retira da lista de processos disponíveis
        proc_atual = Disponiveis.pop(Disponiveis.index(min(Disponiveis, key=lambda p: p.time_exec)))
        while(proc_atual.time_rmng > 0):
            for p in Processos: # Sempre checa se novos processos estão disponíveis
                if(p.time_crt <= time and p not in Disponiveis and p not in Terminados):
                    Disponiveis.append(p)

            proc_atual.time_rmng -= 1 # desconta-se 1 do tempo restante para encerrar o processo escolhido
            Waiting(Disponiveis, Terminados, proc_atual.pid) # Todos os processos disponíveis que não estão executando, esperam
            Timeline.append(proc_atual.pid) # Adiciona-se à linha do tempo o processo que executou
            time += 1
            if(proc_atual.time_rmng == 0): # Se o processo acabou...
                proc_atual.end_time = time # Obtemos seu tempo de finalização e...
                Terminados.append(proc_atual) # Adicionamos ele à lista de terminados
    return Timeline

# Lendo o arquivo de configuração e obtendo...
arquivo_config = "config.txt"
try:
    with open(arquivo_config, "r", encoding="utf-8") as configuracao:
        tam_quantum = configuracao.readline().strip() #... o tamanho do quantum e...
        aging = configuracao.readline().strip() #... o grau de envelhecimento
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

print(Scheduler_SJF(Processos, Disponiveis, Terminados))
for p in Terminados:
    print(p.pid, p.wait_time, p.end_time)
