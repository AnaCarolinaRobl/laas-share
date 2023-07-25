import matplotlib.pyplot as plt
import numpy as np

# Nome do arquivo de texto
nome_arquivo = "26.txt"

# Listas para armazenar os valores
comandos_26 = []
correntes_26 = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        comando, corrente = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        comandos_26.append(float(comando))
        correntes_26.append(float(corrente))

nome_arquivo = "33.txt"

# Listas para armazenar os valores
comandos_old = []
correntes_old = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        comando, corrente = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        comandos_old.append(float(comando))
        correntes_old.append(float(corrente))

nome_arquivo = "39.txt"

# Listas para armazenar os valores
comandos_new = []
correntes_new = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        comando, corrente = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        comandos_new.append(float(comando))
        correntes_new.append(float(corrente))

nome_arquivo = "44.txt"

# Listas para armazenar os valores
comandos_new1 = []
correntes_new1 = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        comando, corrente = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        comandos_new1.append(float(comando))
        correntes_new1.append(float(corrente))


nome_arquivo = "50.txt"

# Listas para armazenar os valores
comandos_new2 = []
correntes_new2 = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        comando, corrente = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        comandos_new2.append(float(comando))
        correntes_new2.append(float(corrente))

nome_arquivo = "57.txt"

# Listas para armazenar os valores
comandos_new3 = []
correntes_new3 = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        comando, corrente = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        comandos_new3.append(float(comando))
        correntes_new3.append(float(corrente))

nome_arquivo = "63.txt"

# Listas para armazenar os valores
comandos_new4 = []
correntes_new4 = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        comando, corrente = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        comandos_new4.append(float(comando))
        correntes_new4.append(float(corrente))

nome_arquivo = "69.txt"

# Listas para armazenar os valores
comandos_new5 = []
correntes_new5 = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        comando, corrente = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        comandos_new5.append(float(comando))
        correntes_new5.append(float(corrente))

nome_arquivo = "75.txt"

# Listas para armazenar os valores
comandos_new6 = []
correntes_new6 = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        comando, corrente = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        comandos_new6.append(float(comando))
        correntes_new6.append(float(corrente))


# Plotagem do gráfico
# plt.plot(comandos, correntes, 'g.', label= '26 degrés')
VBUS = 16
u=[]
i=[]
commande=[]
arquivos = ['26.txt', '39.txt','57.txt','75.txt']
markers = ['b.', 'r.', 'g.', 'y.', 'p.']

for index_arquivo, nome_arquivo in enumerate(arquivos):
    comandos=[]
    correntes=[]
    T=float(nome_arquivo.split('.')[0])
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


    for j in range(len(comandos)):
        if comandos[j] > 0.06:
            commande.append(comandos[j])
            u.append(comandos[j]*VBUS)
            i.append(correntes[j])

    k1=490
    k2=-125
    k3=-97.5
   
    print(T)
    corrente = [round((k1*u[i]+k2)/(T-k3),3) for i in range(len(u))]
    # correntes_filtrada = [correntes[i] for i in range(len(comandos)) if comandos[i] > 0.06]
    # comandos = [comandos_new6[i] for i in range(len(comandos_new6)) if comandos_new6[i] > 0.06]



    # plt.plot(commande, i, markers[index_arquivo], label= f'{T} degrés real current')
    plt.plot(commande, corrente, label=f"Estimated Current in {T}")


    # print(temp)
    # print(sum(temp)/len(temp))

def filtro (comandos, correntes):

    _comandos = [comandos[i] for i in range(len(comandos)) if comandos[i] >= 0.06]  
    _correntes = [correntes[i] for i in range(len(correntes)) if comandos[i] >= 0.06] 
    return _comandos, _correntes

comandos_26, correntes_26 = filtro (comandos_26, correntes_26)    
comandos_new, correntes_new = filtro (comandos_new, correntes_new)   
comandos_new3, correntes_new3 = filtro (comandos_new3, correntes_new3)   
comandos_new6, correntes_new6 = filtro (comandos_new6, correntes_new6)   



plt.plot(comandos_26, correntes_26, 'b,', label= '26 degrés real current')

# plt.plot(comandos_old, correntes_old, 'b.', label= '33 degrés')

plt.plot(comandos_new, correntes_new, 'r,', label= '39 degrés real current')

# plt.plot(comandos_new1, correntes_new1, 'y.', label= '44 degrés')
# plt.plot(comandos_new2, correntes_new2, 'c.', label= '50 degrés')


plt.plot(comandos_new3, correntes_new3, 'g,', label= '57 degrés real current')

# plt.plot(comandos_new4, correntes_new4, 'k.', label= '63 degrés')
# plt.plot(comandos_new5, correntes_new5, 'g.', label= '69 degrés')
plt.plot(comandos_new6, correntes_new6, 'r,', label= '75 degrés real current', linewidth=100)


plt.legend()
plt.xlabel('Command [V/V]')
plt.ylabel('Current [A]')
plt.title('Command x Current ')
plt.grid(True)
plt.show()

#26, 33, 39