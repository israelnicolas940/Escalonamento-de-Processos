class Processo:
    def __init__(self, time_crt, time_exec, prior, pos):
        self.time_crt = time_crt
        self.time_exec = time_exec
        self.prior = prior
        self.wait_time = 0
        self.state = "Ready"
        self.endtime = -1
        self.name = "P" + str(pos)

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

Processos = []
i = 1
while True:
    entrada = input("").split()
    if not entrada:
        break
    Processos.append(Processo(entrada[0], entrada[1], entrada[2], i))
    print(Processos[i - 1].name)
    i += 1
