import matplotlib.pyplot as plt
import numpy as np

# Nome do arquivo de texto
nome_arquivo = "rolling_data_squared_stop.txt"

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

# TIME1 = int(len(times) / times[-1])
TIME1 = -1

for i in range(len(iqs)):
    if abs(iqs[i]) < 1.9:
        iqs[i] = 0


# Cria uma figura com 2 linhas e 2 colunas de subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Plot dos gráficos em cada subplot
axs[0, 0].plot(times[:TIME1], ids[:TIME1], 'g.', label="Id")
axs[0, 0].plot(times[:TIME1], iqs[:TIME1], 'r.',label="Iq")
axs[0, 0].set_title('Measured Currents')
axs[0, 0].set_xlabel('Time [s]')
axs[0, 0].set_ylabel('Current [A]')
axs[0, 0].legend()
axs[0, 0].grid()

axs[0, 1].plot(times[:TIME1], vds[:TIME1],'g.', label="Vd")
axs[0, 1].plot(times[:TIME1], vqs[:TIME1],  'r.',label="Vq")
axs[0, 1].set_title('Defined Voltages')
axs[0, 1].set_xlabel('Time [s]')
axs[0, 1].set_ylabel('Voltage [V]')
axs[0, 1].legend()
axs[0, 1].grid()

axs[1, 0].plot(times[:TIME1], velocitys[:TIME1],'g.', label="Velocity")
axs[1, 0].plot(times[:TIME1], positions[:TIME1],'r.', label="Position")
axs[1, 0].set_title('Measured Velocitys and Positions')
axs[1, 0].set_xlabel('Time [s]')
axs[1, 0].set_ylabel('Velocity [rad/s]/Position [rad]')
axs[1, 0].legend()
axs[1, 0].grid()

axs[1, 1].plot(times[:TIME1], temps_measured[:TIME1],'y.')
axs[1, 1].set_title('Measured Temperature')
axs[1, 1].set_xlabel('Time [s]')
axs[1, 1].set_ylabel('Temperature [°Celsius]')
axs[1, 1].grid()

# Ajusta os espaços entre os subplots para evitar sobreposição de títulos e rótulos
plt.tight_layout()

plt.show()