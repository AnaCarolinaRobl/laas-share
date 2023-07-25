import matplotlib.pyplot as plt
import numpy as np
# Nome do arquivo de texto
nome_arquivo = "TempoXTemp.txt"

times0 = []
temperatures0 = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    next(arquivo)# Ignora a primeira linha (cabeçalho)
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        time, temperature = linha.strip().split(",")
        times0.append(float(time))
        temperatures0.append(float(temperature))


# Nome do arquivo de texto
nome_arquivo = "TempoXTempDes.txt"

times1 = []
temperatures1 = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    next(arquivo)# Ignora a primeira linha (cabeçalho)
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        time, temperature = linha.strip().split(",")
        times1.append(float(time))
        temperatures1.append(float(temperature))

times = times0.copy()
temperatures = temperatures0.copy()

test = []

for i, t in enumerate(times1):
    print(t, times0[-1])
    times.append(t + times0[-1])
    test.append(t + times0[-1])
    temperatures.append(temperatures1[i])


# Nome do arquivo de texto
nome_arquivo = "TempoXTempDes1.txt"

times2 = []
temperatures2 = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    next(arquivo)# Ignora a primeira linha (cabeçalho)
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        time, temperature = linha.strip().split(",")
        times2.append(float(time))
        temperatures2.append(float(temperature))

last_time = times[-1]

for i, t in enumerate(times2):
    times.append(last_time + t)
    temperatures.append(temperatures2[i])

plt.plot(np.array(times)/60, temperatures, ".")
plt.title("Temperature behavior with current of 3A(rise) and 0A(descent)")
plt.xlabel("Time (minutes)")
plt.ylabel("Temperature (Celsius)")
plt.grid()

plt.show()
