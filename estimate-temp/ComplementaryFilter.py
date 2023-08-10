import matplotlib.pyplot as plt
import numpy as np

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

T_AMBIENT = temps_measured[0]

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

# FILTER FUNTCTION
def LPF_FILTER(tau, xs):
    ys = [0] * len(xs)
    ys[0] = xs[0]
    for i in range(1, len(xs)):
        ys[i] = tau * xs[i] + (1 - tau) * ys[i-1]
    return ys

def MEDIAN_FILTER(arr, LENGTH):

    arr_flt = []

    for i in range(0, len(arr)):
        temps_vec = [round(arr[i], 1)]
        j = i-LENGTH
        k = i+LENGTH
        while len(temps_vec) <= (LENGTH*2+1) and j<i:
            if j>=0:
                temps_vec.append(round(arr[j], 1))
            if k < len(arr):
                temps_vec.append(round(arr[k], 1))
            j+=1
            k+=1

        x = round(sum(temps_vec)/len(temps_vec), 1)
        arr_flt.append(x)

    return arr_flt

def HPF_FILTER(tau, xs):
    ys = [0] * len(xs)
    ys[0] = 0
    for i in range(1, len(xs)):
        ys[i] = tau * (ys[i-1] + xs[i] - xs[i-1])
    return ys

temps_lstq_flt = MEDIAN_FILTER(temps_lstq, 10)



# Fusion temperatures (thermal and LSTQ)
def complementaryFilter(arr_hp, arr_lp, tau_hp, tau_lp):
    arr_hp = HPF_FILTER(tau_hp, arr_hp)
    arr_lp = LPF_FILTER(tau_lp, arr_lp)
    
    arr_filtered = []
    for i in range(len(arr_hp)):
        arr_filtered.append(arr_hp[i] + arr_lp[i])

    # arr_filtered = MEDIAN_FILTER(arr_filtered, 10)

    return arr_filtered

def complementaryFilterSimplified(tau):
    K1 = 0.0102
    K2 = 1/529
    K3 = 1 # 45/25
    temps_fusion=[T_AMBIENT]
    for i in range(0, len(ids)-1):
        delta_t = temps_fusion[-1] - T_AMBIENT
        current = ids[i]*ids[i]#+iqs[i]*iqs[i]
        temp_derivate = ((current * K1) - (delta_t * K2)) * K3
        DT = times[i+1] - times[i]
        temps_fusion.append(temps_fusion[-1] + ((temp_derivate) * DT * tau))

        e = temps_fusion[-1] - temps_lstq[i+1]
        trust = 1.0 - .004*1* (.01*(min(current, 100.0)))
        temps_fusion[-1] = (temps_fusion[-1]-trust*.01*e)

    return temps_fusion


# calculate termique model
def thermal_model():
    K1 = 0.0102
    K2 = 1/529
    K3 = 1 # 45/25
    temps_model = [T_AMBIENT]
    for i in range(0, len(ids)-1):
        delta_t = temps_model[-1] - T_AMBIENT
        current = ids[i]*ids[i]#+iqs[i]*iqs[i]
        temp_derivate = ((current * K1) - (delta_t * K2)) * K3
        DT = times[i+1] - times[i]
        temps_model.append(temps_model[-1] + ((temp_derivate) * DT))
    return temps_model


temps_model = thermal_model()
# temps_fusion = fusion_model()


taus = np.linspace(0.1, 0.5, 2)
temps_fusion = []
#     plt.plot(times, temps_fusion, label=f"Tau = {tau}")

# for tau in taus:

# temps_fusion = complementaryFilterSimplified(tau)
# temps_fusion_flt = MEDIAN_FILTER(temps_fusion, 5)




tau = 0.01
plt.plot(times, temps_measured, "b.", label="Measured Temperature")
plt.plot(times, temps_lstq_flt, label=f"Resistance model with Median Filter")
plt.plot(times, LPF_FILTER(tau, temps_lstq), label="Resistance model with Low Pass Filter")
plt.plot(times, complementaryFilter(temps_model, temps_lstq, 1-tau, tau), label=f"Complementary Filter tau_hp = {1-tau}, tau_lp = {tau}")
plt.plot(times, complementaryFilterSimplified(1-tau), label=f"Complementary Filter Simplified tau_hp = {1-tau}, tau_lp = {tau}")


plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')

# cf = complementaryFilter(temps_model, temps_lstq, 1-tau, tau)
# errors = [temps_measured[i] - cf[i] for i in range(len(cf))]
# plt.plot(times, errors, label=f"Error Complementary Filter tau_hp = {1-tau}, tau_lp = {tau}")


# plt.plot(times, temps_fusion_flt, label=f"Tau = {tau} filtered")

# plt.plot(times, temps_model, label=f"Thermal model")



# FILTERS TESTS
# plt.plot(times, HPF_FILTER(tau, temps_model), label= f"Thermal model with HPF and tau = {tau}")
# plt.plot(times, LPF_FILTER(0.1, temps_lstq), label= f"Resistance model with LPF and tau = {tau}")

plt.legend()
plt.show()

# axs[0].plot(times, temps_measured, 'g.', label="Measured Temperature")



# error lists
# errors_measured_fusion = [temps_measured[i] - temps_fusion[i]  for i in range(len(temps_measured))]


# # Criando a figura e os subplots
# fig, axs = plt.subplots(2, 1, figsize=(8, 6))

# # Plotando o primeiro gráfico na posição (0, 0) da grade (em cima)
# axs[0].plot(times, temps_measured, 'g.', label="Measured Temperature")
# # axs[0].plot(times, temps_lstq, 'r.',label="Estimated Temperature with resistance model")
# # axs[0].plot(times, temps_lstq_flt, 'y.', label=f"Estimated Temperature with resistance model and mean of {(LENGTH*2+1)} points")
# # axs[0].plot(times, temps_fusion, 'r.', label="Temperature fusion")

# ## Errors graphs
# # axs[0].plot(times, errors_measured_fusion, 'b.', label="Error = Measured - Fusion Temperature")


# axs[0].set_xlabel('Time [s]')
# axs[0].set_ylabel('Temperature [° Celsius]')
# axs[0].legend()
# axs[0].grid()

# # Plotando o segundo gráfico na posição (1, 0) da grade (embaixo)
# axs[1].plot(times, iqs, 'b.')
# axs[1].set_xlabel('Time [s]')
# axs[1].set_ylabel('Current [A]')
# # axs[1].legend()

# plt.show()