import matplotlib.pyplot as plt

# Nome do arquivo de texto
nome_arquivo = "data.txt"

# Listas para armazenar os valores
times = []
ids, iqs = [], []
vds, vqs = [], []
temps_measured = []
temps_model_omodri = []
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
        temps_measured.append(float(temp_measured))
        temps_model_omodri.append(float(temp_model))
        temps_lstq.append(float(temp_lstq))


# NEW TEMPS_LSTQ
res_k1 = 879
res_k2 = -215
res_k3 = -219


temps_lstq1 = []
for i in range(len(ids)):
    current = ids[i]
    voltage = vds[i]
    if current != 0:
        temp_lstq = res_k1 * (voltage / current) + res_k2 * (1 / current) + res_k3
        temp_lstq = round(temp_lstq, 1)
    else:
        temp_lstq = 0
    

    temps_lstq1.append(temp_lstq)

temps_lstq = temps_lstq1

### data prepation
# Limits estimated temperature between 0 or 200
for i in range(len(temps_lstq)):
    if temps_lstq[i] > 200 or temps_lstq[i] < 0 or ids[i] < 1.5:
        temps_lstq[i] = temps_lstq[i-1]

# filtro passa baixa pro least_squares


def LPF_FILTER_1(flt_coef, y, x):
    erro = ((x) - (y))
    return ((y) + (flt_coef * erro))

temps_lstq_flt = []

LENGTH = 10
for i in range(0, len(temps_lstq)):
    temps_vec = [temps_lstq[i]]
    j = i-LENGTH
    k = i+LENGTH
    while len(temps_vec) <= (LENGTH*2+1) and j<i:
        if j>=0:
            temps_vec.append(temps_lstq[j])
        if k < len(temps_lstq):
            temps_vec.append(temps_lstq[k])
        j+=1
        k+=1

    temps_lstq_flt.append(sum(temps_vec)/len(temps_vec))

# calculate termique model
T_AMBIENT = temps_measured[0]

K1 = 0.0102
K2 = 1/529
K3 = 1 # 45/25


# Fusion temperatures (thermal and LSTQ)
def fusion_model():
    temps_fusion=[T_AMBIENT]
    for i in range(0, len(ids)-1):
        delta_t = temps_fusion[-1] - T_AMBIENT
        current = ids[i]*ids[i]#+iqs[i]*iqs[i]
        temp_derivate = ((current * K1) - (delta_t * K2)) * K3
        DT = times[i+1] - times[i]
        temps_fusion.append(temps_fusion[-1] + ((temp_derivate) * DT))

        e = temps_fusion[-1] - temps_lstq[i+1]
        trust = 1.0 - .004*1* (.01*(min(current, 100.0)))
        temps_fusion[-1] = (temps_fusion[-1]-trust*.01*e)

    return temps_fusion


def thermal_model():
    temps_model = [T_AMBIENT]
    for i in range(0, len(ids)-1):
        delta_t = temps_model[-1] - T_AMBIENT
        current = ids[i]*ids[i]#+iqs[i]*iqs[i]
        temp_derivate = ((current * K1) - (delta_t * K2)) * K3
        DT = times[i+1] - times[i]
        temps_model.append(temps_model[-1] + ((temp_derivate) * DT))
    return temps_model


temps_model = thermal_model()
temps_fusion = fusion_model()

# error lists
errors_measured_fusion = [temps_measured[i] - temps_fusion[i]  for i in range(len(temps_measured))]


# Criando a figura e os subplots
fig, axs = plt.subplots(2, 1, figsize=(8, 6))

# Plotando o primeiro gráfico na posição (0, 0) da grade (em cima)
axs[0].plot(times, temps_measured, 'g.', label="Measured Temperature")
axs[0].plot(times, temps_lstq, 'r.',label="Estimated Temperature with resistance model")
axs[0].plot(times, temps_lstq_flt, 'y.', label=f"Estimated Temperature with resistance model and mean of {(LENGTH*2+1)} points")
# axs[0].plot(times, temps_model, 'b.', label="Estimated Temperature with thermique model")
# axs[0].plot(times, temps_fusion, 'r.', label="Temperature fusion")

## Errors graphs
# axs[0].plot(times, errors_measured_fusion, 'b.', label="Error = Measured - Fusion Temperature")


axs[0].set_xlabel('Time [s]')
axs[0].set_ylabel('Temperature [° Celsius]')
axs[0].legend()
axs[0].grid()

# Plotando o segundo gráfico na posição (1, 0) da grade (embaixo)
axs[1].plot(times, iqs, 'b.')
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