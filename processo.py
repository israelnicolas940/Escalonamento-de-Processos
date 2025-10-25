# Classe Processo
class Processo:
    def __init__(self, time_crt, time_exec, prior, pos):
        self.time_crt = time_crt # Tempo de criação do processo
        self.time_exec = time_exec # Tempo de execução restante
        self.prior = prior # Prioridade do processo
        self.prior_aux = prior # Prioridade mutável (aging)
        self.wait_time = 0 # Tempo de espera do processo
        self.time_rmng= time_exec # Tempo restante para terminar a execução
        self.end_time = -1 # Tempo em que o processo acabou
        self.pid = "P" + str(pos) # Nome do processo
