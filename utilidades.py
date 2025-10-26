import random

# Função que computa a espera de todos os processos disponíveis, mas que não foram escolhidos
def Waiting(Disponiveis, Terminados, pid):
    for p in Disponiveis:
        if(p.pid != pid and p not in Terminados):
            p.wait_time += 1

# Função que computa o envelhecimento de todos os processos disponíveis, mas que não foram escolhidos
def Aging(Disponiveis, Terminados, pid, aging):
    for p in Disponiveis:
        if(p.pid != pid and p not in Terminados):
            p.prior_aux += aging

# Função para decidir, se tivermos dois ou mais processos empatados, qual será escolhido
def Desempatador(Candidatos, Timeline):
    Menores_tempos = []
    minimo = min(p.time_rmng for p in Candidatos)
    for p in Candidatos:
        if(len(Timeline) > 0 and Timeline[-1] == p.pid):
            return p # Primeiro, ele tenta manter o processo que já está executando
        if(p.time_rmng == minimo):
            Menores_tempos.append(p)
    if(len(Menores_tempos) == 1): # Em seguida, ele busca o processo que falta menos tempo para terminar sua execução
        return Menores_tempos[0]
    else:
        return random.choice(Menores_tempos) # E, em último caso, ele retorna um processo aleatório entre os candidatos

# Função para calcular o tempo médio de espera
def Calc_AvgWaitTime(Processos):
    total = 0
    for p in Processos:
        total += p.wait_time
    return total/len(Processos) if Processos else 0

# Função para calcular o tempo médio de vida dos processos
def Calc_AvgWaitTurn(Processos):
    total = 0
    for p in Processos:
        total += (p.wait_time + p.time_exec)
    return total/len(Processos) if Processos else 0

# Função para plotar o diagrama das distribuições dos processos ao longo do tempo
def Plotar_diagrama(Timeline, Processos):
    cabecalho = "tempo   "
    for p in Processos:
        cabecalho += p.pid + "  "
    print(cabecalho)

    i = 0
    for t in Timeline:
        if(i < 9):
            linha = " " + str(i) + "- " + str(i+1) + "   "
        else: 
            if(i == 9):
                linha = " " + str(i) + "-" + str(i+1) + "   "
            else:
                linha = str(i) + "-" + str(i+1) + "   "
        for p in Processos:
            if(t == p.pid):
                linha += "##  "
            else:
                linha += "--  "
        i += 1
        print(linha)
