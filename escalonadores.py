from utilidades import Waiting, Aging, Desempatador

def Scheduler_FCFS(Processos, Disponiveis, Terminados, cntxt_chngs, qntm, aging):
    time = 0 # Tempo inicial
    Timeline = [] # Linha do tempo especificando qual processo executou em dado momento
    while(len(Processos) > len(Terminados)): # Enquanto existirem processos inacabados...
        for p in Processos:
            if(p.time_crt <= time and p not in Disponiveis and p not in Terminados):
                Disponiveis.append(p) # Se a data de criação for menor que o tempo atual, o 
                                      # O processo torna-se disponível

        if not Disponiveis:
            Timeline.append("-") # Para o caso de ainda não terem sido criados processos
            time += 1
            continue
        
        proc_atual = Disponiveis.pop(0) # Escolhe-se o processo por ordem de chegada
        if(len(Timeline) > 0 and Timeline[-1] != proc_atual.pid): # Verifica se houve troca de contexto
                cntxt_chngs += 1
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
    return Timeline, cntxt_chngs

def Scheduler_SJF(Processos, Disponiveis, Terminados, cntxt_chngs, qntm, aging):
    time = 0 # Tempo inicial
    Timeline = [] # Linha do tempo especificando qual processo executou em dado momento
    while(len(Processos) > len(Terminados)): # Enquanto existirem processos inacabados...
        for p in Processos:
            if(p.time_crt <= time and p not in Disponiveis and p not in Terminados):
                Disponiveis.append(p) # Se a data de criação for menor que o tempo atual, o 
                                      # O processo torna-se disponível

        if not Disponiveis:
            Timeline.append("-") # Para o caso de ainda não terem sido criados processos
            time += 1
            continue
        
        # Escolhe o processo de menor duração e o retira da lista de processos disponíveis
        menor_rmng = min(p.time_rmng for p in Disponiveis)
        Candidatos = [p for p in Disponiveis if p.time_rmng == menor_rmng]
        proc_atual = Desempatador(Candidatos, Timeline)
        Disponiveis.remove(proc_atual)
        if(len(Timeline) > 0 and Timeline[-1] != proc_atual.pid): # Verifica se houve troca de contexto
                cntxt_chngs += 1

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
    return Timeline, cntxt_chngs + 1 # Troca da CPU vazia para o primeiro processo

def Scheduler_SRTF(Processos, Disponiveis, Terminados, cntxt_chngs, qntm, aging):
    time = 0 # Tempo inicial
    Timeline = [] # Linha do tempo especificando qual processo executou em dado momento
    proc_atual = None
    while(len(Processos) > len(Terminados)): # Enquanto existirem processos inacabados...
        for p in Processos:
            if(p.time_crt <= time and p not in Disponiveis and p not in Terminados):
                Disponiveis.append(p) # Se o a data de criação for menor que o tempo atual, o 
                                      # O processo torna-se disponível

        # Removendo processos já terminados da lista de processos disponíveis
        Disponiveis = [p for p in Disponiveis if p not in Terminados]

        if not Disponiveis:
            Timeline.append("-") # Para o caso de ainda não terem sido criados processos
            time += 1
            continue
        
        # Escolhe o processo de menor duração restante e o retira da lista de processos disponíveis
        menor_rmng = min(p.time_rmng for p in Disponiveis)
        Candidatos = [p for p in Disponiveis if p.time_rmng == menor_rmng]
        menor = Desempatador(Candidatos, Timeline)
        if(proc_atual != menor):
            proc_atual = menor
            cntxt_chngs += 1
        
        proc_atual.time_rmng -= 1 # desconta-se 1 do tempo restante para encerrar o processo escolhido
        Waiting(Disponiveis, Terminados, proc_atual.pid) # Todos os processos disponíveis que não estão executando, esperam
        Timeline.append(proc_atual.pid) # Adiciona-se à linha do tempo o processo que executou
        time += 1
        if(proc_atual.time_rmng == 0):
            proc_atual.end_time = time
            Terminados.append(proc_atual)
            proc_atual = None
    return Timeline, cntxt_chngs

def Scheduler_PrioSp(Processos, Disponiveis, Terminados, cntxt_chngs, qntm, aging):
    time = 0 # Tempo inicial
    Timeline = [] # Linha do tempo especificando qual processo executou em dado momento
    while(len(Processos) > len(Terminados)): # Enquanto existirem processos inacabados...
        for p in Processos:
            if(p.time_crt <= time and p not in Disponiveis and p not in Terminados):
                Disponiveis.append(p) # Se o a data de criação for menor que o tempo atual, o 
                                      # O processo torna-se disponível

        if not Disponiveis:
            Timeline.append("-") # Para o caso de ainda não terem sido criados processos
            time += 1
            continue
        
        # Escolhe o processo de maior prioridade e o retira da lista de processos disponíveis
        maior_prio = max(p.prior for p in Disponiveis)
        Candidatos = [p for p in Disponiveis if p.prior == maior_prio]
        proc_atual = Desempatador(Candidatos, Timeline)
        Disponiveis.remove(proc_atual)
        if(len(Timeline) > 0 and Timeline[-1] != proc_atual.pid): # Verifica se houve troca de contexto
                cntxt_chngs += 1

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
    return Timeline, cntxt_chngs

def Scheduler_PrioCp(Processos, Disponiveis, Terminados, cntxt_chngs, qntm, aging):
    time = 0 # Tempo inicial
    Timeline = [] # Linha do tempo especificando qual processo executou em dado momento
    proc_atual = None
    while(len(Processos) > len(Terminados)): # Enquanto existirem processos inacabados...
        for p in Processos:
            if(p.time_crt <= time and p not in Disponiveis and p not in Terminados):
                Disponiveis.append(p) # Se o a data de criação for menor que o tempo atual, o 
                                      # O processo torna-se disponível

        Disponiveis = [p for p in Disponiveis if p not in Terminados]

        if not Disponiveis:
            Timeline.append("-") # Para o caso de ainda não terem sido criados processos
            time += 1
            continue
        
        # Escolhe o processo de maior prioridade
        maior_prior = max(p.prior for p in Disponiveis)
        Candidatos = [p for p in Disponiveis if p.prior == maior_prior]
        maior = Desempatador(Candidatos, Timeline)
        if(len(Timeline) > 0 and Timeline[-1] != maior.pid):
            cntxt_chngs += 1
        proc_atual = maior
        
        proc_atual.time_rmng -= 1 # desconta-se 1 do tempo restante para encerrar o processo escolhido
        Timeline.append(proc_atual.pid) # Adiciona-se à linha do tempo o processo que executou
        time += 1
        Waiting(Disponiveis, Terminados, proc_atual.pid) # Todos os processos disponíveis que não estão executando, esperam
        if(proc_atual.time_rmng == 0):
            proc_atual.end_time = time
            Terminados.append(proc_atual)
            proc_atual = None
        
    return Timeline, cntxt_chngs

def Scheduler_RRSp(Processos, Disponiveis, Terminados, cntxt_chngs, qntm, aging):
    time = 0 # Tempo inicial
    Timeline = [] # Linha do tempo especificando qual processo executou em dado momento
    proc_atual = None
    while(len(Processos) > len(Terminados)): # Enquanto existirem processos inacabados...
        for p in Processos:
            if(p.time_crt <= time and p not in Disponiveis and p not in Terminados):
                Disponiveis.append(p) # Se o a data de criação for menor que o tempo atual, o 
                                      # O processo torna-se disponível

        Disponiveis = [p for p in Disponiveis if p not in Terminados]

        if not Disponiveis:
            Timeline.append("-") # Para o caso de ainda não terem sido criados processos
            time += 1
            continue
        
        # Escolhe o processo que está no começo da lista e o retira da lista de processos disponíveis
        proc_atual = Disponiveis.pop(0)
        if(len(Timeline) > 0 and Timeline[-1] != proc_atual.pid): # Verifica se houve troca de contexto
                cntxt_chngs += 1
        
        qntm_rmng = int(qntm)
        while(qntm_rmng > 0 and proc_atual.time_rmng > 0):
            Timeline.append(proc_atual.pid) # Adiciona-se à linha do tempo o processo que executou
            proc_atual.time_rmng -= 1 # desconta-se 1 do tempo restante para encerrar o processo escolhido
            time += 1
            qntm_rmng -= 1

            Waiting(Disponiveis, Terminados, proc_atual.pid) # Todos os processos disponíveis que não estão executando, esperam

            for p in Processos: # Sempre checa se novos processos estão disponíveis
                if(p.time_crt <= time and p not in Disponiveis and p not in Terminados and p != proc_atual):
                    Disponiveis.append(p)

        if(proc_atual.time_rmng == 0): # Se o processo acabou...
            proc_atual.end_time = time # Obtemos seu tempo de finalização e...
            Terminados.append(proc_atual) # Adicionamos ele à lista de terminados
        else:
            Disponiveis.append(proc_atual)
    return Timeline, cntxt_chngs
    
def Scheduler_RRCp(Processos, Disponiveis, Terminados, cntxt_chngs, qntm, aging):
    time = 0 # Tempo inicial
    Timeline = [] # Linha do tempo especificando qual processo executou em dado momento
    proc_atual = None
    while(len(Processos) > len(Terminados)): # Enquanto existirem processos inacabados...
        for p in Processos:
            if(p.time_crt <= time and p not in Disponiveis and p not in Terminados):
                Disponiveis.append(p) # Se o a data de criação for menor que o tempo atual, o 
                                      # O processo torna-se disponível

        Disponiveis = [p for p in Disponiveis if p not in Terminados]

        if not Disponiveis:
            Timeline.append("-") # Para o caso de ainda não terem sido criados processos
            time += 1
            continue
        
        # Escolhe o processo de menor duração e o retira da lista de processos disponíveis
        maior_prior_aux = max(p.prior_aux for p in Disponiveis)
        Candidatos = [p for p in Disponiveis if p.prior_aux == maior_prior_aux]
        proc_atual = Desempatador(Candidatos, Timeline)
        Disponiveis.remove(proc_atual)
        if(len(Timeline) > 0 and Timeline[-1] != proc_atual.pid): # Verifica se houve troca de contexto
                cntxt_chngs += 1
        
        qntm_rmng = int(qntm)
        while(qntm_rmng > 0 and proc_atual.time_rmng > 0):
            Timeline.append(proc_atual.pid) # Adiciona-se à linha do tempo o processo que executou
            proc_atual.time_rmng -= 1 # desconta-se 1 do tempo restante para encerrar o processo escolhido
            time += 1
            qntm_rmng -= 1

            Aging(Disponiveis, Terminados, proc_atual.pid, int(aging))
            Waiting(Disponiveis, Terminados, proc_atual.pid) # Todos os processos disponíveis que não estão executando, esperam

            for p in Processos: # Sempre checa se novos processos estão disponíveis
                if(p.time_crt <= time and p not in Disponiveis and p not in Terminados and p != proc_atual):
                    Disponiveis.append(p)

        if(proc_atual.time_rmng == 0): # Se o processo acabou...
            proc_atual.end_time = time # Obtemos seu tempo de finalização e...
            Terminados.append(proc_atual) # Adicionamos ele à lista de terminados
        else:
            proc_atual.prior_aux = proc_atual.prior # Anula o envelhecimento resetando a prioridade
            Disponiveis.append(proc_atual)
        
    return Timeline, cntxt_chngs

