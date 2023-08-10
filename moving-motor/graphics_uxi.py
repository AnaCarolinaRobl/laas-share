import matplotlib.pyplot as plt
import numpy as np

# Nome do arquivo de texto
nome_arquivo = "uxi_data.txt"

# Listas para armazenar os valores
times = []
ids, iqs = [], []
vds, vqs = [], []
temps_measured = []
positions = []
velocitys = []



# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        time, id, iq, vd, vq, velocity, temp_measured, position = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        times.append(float(time))
        ids.append(float(id))
        iqs.append(float(iq))
        vds.append(float(vd))
        vqs.append(float(vq))
        velocitys.append(float(velocity))
        temps_measured.append(float(temp_measured))
        positions.append(float(position))

TIME1 = int(len(times) / times[-1])
# TIME1 = -1

plt.plot(iqs, vqs, '.')
plt.title("iqs x uqs")
plt.legend()
plt.grid()
plt.show()

resis = [vqs[i] / iqs[i] for i in range(len(vqs))]
plt.plot(iqs, resis, '.')
plt.title("resis")
plt.show()
