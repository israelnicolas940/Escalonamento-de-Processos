# Lendo o arquivo de configuração e obtendo...
arquivo_config = "config.txt"
try:
    with open(arquivo_config, "r", encoding="utf-8") as configuracao:
        tam_quantum = configuracao.readline().strip() #... o tamanho do quantum e...
        aging = configuracao.readline().strip() #... o grau de envelhecimento
except FileNotFoundError:
    print(f"Erro: o arquivo", arquivo_config, "nao foi encontrado")   
except Exception as e:
    print(f"Ocorreu o seguinte erro: {e}")    

print(tam_quantum, aging) # Teste (Apagar depois)

