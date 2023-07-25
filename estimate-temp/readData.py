import matplotlib.pyplot as plt

# Nome do arquivo de texto
nome_arquivo = "data.txt"

# Listas para armazenar os valores
times = []
ids, iqs = []
vds, vqs = []
temps_measured = []
temps_model = []
temps_lstq = []


# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        time, id, iq, vd, vq, temp_measured, temp_lstq, temp_model = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        times.append(float(time))
        ids.append(float(id))
        iqs.append(float(iq))
        vds.append(float(vd))
        vqs.append(float(vq))
        temps_measured.append(float(temp_measure))
        temps_model.append(float(temp_model))
        temps_lstq.append(float(temp_lstq))


# Criando a figura e os subplots
fig, axs = plt.subplots(2, 1, figsize=(8, 6))

# Plotando o primeiro gráfico na posição (0, 0) da grade (em cima)
axs[0].plot(times, temperatures_measured, 'g.', label="Measured Temperature")
axs[0].plot(times, temperatures_estimated, 'r.', label="Estimated Temperature")
# axs[0].plot(times, temperatures_estimated_offset,'b.', label="Estimated Temperature with Offset of -10")
axs[0].set_xlabel('Time [s]')
axs[0].set_ylabel('Temperature [° Celsius]')
axs[0].legend()
axs[0].grid()

# Plotando o segundo gráfico na posição (1, 0) da grade (embaixo)
axs[1].plot(times, correntes, color='blue')
axs[1].set_xlabel('Time [s]')
axs[1].set_ylabel('Current [A]')
# axs[1].legend()

# Plotagem do gráfico
# plt.plot(times, temperatures_measured, 'g.', label="Measured Temperature")
# plt.plot(times, temperatures_estimated, 'r.', label="Estimated Temperature Original")
# plt.plot(times, temperatures_estimated_offset, 'b.', label="Estimated Temperature with Offset of -10")
# plt.legend()
# plt.xlabel('Time [s]')
# plt.ylabel('Temperature [° Celsius]')
# plt.title('Time x Temperature')
# plt.grid(True)
plt.show()

#26, 33, 39