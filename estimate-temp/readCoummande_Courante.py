import matplotlib.pyplot as plt

# Nome do arquivo de texto
nome_arquivo = "ResistanceXTemperature.txt"

# Listas para armazenar os valores
comandos = []
correntes = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        comando, corrente = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        comandos.append(float(comando))
        correntes.append(float(corrente))



# Plotagem do gráfico
plt.plot(comandos, correntes, 'g.', label)
plt.legend()
plt.xlabel('Commande')
plt.ylabel('Courante')
plt.title('Commande x Courante')
plt.grid(True)
plt.show()

#26, 33, 39