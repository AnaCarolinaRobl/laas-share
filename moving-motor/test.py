import numpy as np
import matplotlib.pyplot as plt

# Função para calcular a derivada
def calcular_derivada(x, y):
    dy = np.gradient(y, x)
    return dy

# Ler os valores do arquivo TXT
arquivo = "dados_sinusoidal.txt"
dados_sinusoidal = np.loadtxt(arquivo)

# Definir os valores de x
x = np.linspace(0, len(dados_sinusoidal) - 1, len(dados_sinusoidal))

# Calcular a derivada dos dados
derivada = calcular_derivada(x, dados_sinusoidal)

# Plotar o gráfico original
plt.subplot(2, 1, 1)
plt.plot(x, dados_sinusoidal)
plt.title('Gráfico Original (Sinusoidal)')
plt.xlabel('Índice')
plt.ylabel('Amplitude')

# Plotar o gráfico da derivada
plt.subplot(2, 1, 2)
plt.plot(x, derivada)
plt.title('Derivada da Sinusoidal')
plt.xlabel('Índice')
plt.ylabel('Derivada')

# Ajustar o layout dos subplots para evitar sobreposição de títulos e rótulos
plt.tight_layout()

# Mostrar os gráficos na tela
plt.show()

# **********************************************
# Cria uma figura com 2 linhas e 2 colunas de subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Plot dos gráficos em cada subplot
axs[0, 0].plot(times_estimate[:TIME1*10], iqs_estimate[:TIME1*10], 'g.', label="Id")
axs[0, 0].plot(times_estimate[:TIME1*10], vqs_estimate[:TIME1*10], 'r.',label="Vq")
axs[0, 0].plot(times_estimate[:TIME1*10], velocitys_estimate[:TIME1*10],'y.',label="Velocity")
axs[0, 0].set_title('1A')
axs[0, 0].set_xlabel('Time [s]')
axs[0, 0].legend()
axs[0, 0].grid()

axs[0, 1].plot(times_estimate[TIME1*10:TIME1*20], iqs_estimate[TIME1*10:TIME1*20],'g.', label="Id")
axs[0, 1].plot(times_estimate[TIME1*10:TIME1*20], vqs_estimate[TIME1*10:TIME1*20],  'r.',label="Vq")
axs[0, 1].plot(times_estimate[TIME1*10:TIME1*20], velocitys_estimate[TIME1*10:TIME1*20],'y.',label="Velocity")
axs[0, 1].set_title('2A')
axs[0, 1].set_xlabel('Time [s]')
axs[0, 1].legend()
axs[0, 1].grid()

axs[1, 0].plot(times_estimate[TIME1*20:TIME1*30], iqs_estimate[TIME1*20:TIME1*30],'g.', label="Id")
axs[1, 0].plot(times_estimate[TIME1*20:TIME1*30], vqs_estimate[TIME1*20:TIME1*30],'r.', label="Vq")
axs[1, 0].plot(times_estimate[TIME1*20:TIME1*30], velocitys_estimate[TIME1*20:TIME1*30],'y.', label="Velocity")
axs[1, 0].set_title('3A')
axs[1, 0].set_xlabel('Time [s]')
axs[1, 0].legend()
axs[1, 0].grid()

axs[1, 1].plot(times_estimate[TIME1*30:TIME1*40], iqs_estimate[TIME1*30:TIME1*40],'g.', label="Id")
axs[1, 1].plot(times_estimate[TIME1*30:TIME1*40], vqs_estimate[TIME1*30:TIME1*40],'r.',label="Vq")
axs[1, 1].plot(times_estimate[TIME1*30:TIME1*40], velocitys_estimate[TIME1*30:TIME1*40],'y.',label="Velocity")
axs[1, 1].set_title('4A')
axs[1, 1].set_xlabel('Time [s]')
axs[1, 1].grid()
