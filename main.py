# Classe Processo
class Processo:
    def __init__(self, time_crt, time_exec, prior, pos):
        self.time_crt = time_crt # Tempo de criação do processo
        self.time_exec = time_exec # Tempo de execução restante
        self.prior = prior # Prioridade do processo
        self.wait_time = 0 # Tempo de espera do processo
        self.state = "Ready" # Estado do processo
        self.endtime = -1 # Tempo em que o processo acabou
        self.name = "P" + str(pos) # Nome do processo

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
    Processos.append(Processo(entrada[0], entrada[1], entrada[2], i))
    print(Processos[i - 1].name)
    i += 1

Processos.sort(key=lambda p: p.time_crt)
for j in Processos:
    print(j.time_crt)
