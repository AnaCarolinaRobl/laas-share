import matplotlib.pyplot as plt
import numpy as np

# Nome do arquivo de texto
nome_arquivo = "data/rolling_data_sin_6A.txt"

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

# Calcular a derivada dos dados
derivada = np.gradient(iqs, times)

# FILTER FUNTCTION
def LPF_FILTER(tau, xs):
    ys = [0] * len(xs)
    ys[0] = xs[0]
    for i in range(1, len(xs)):
        ys[i] = tau * xs[i] + (1 - tau) * ys[i-1]
    return ys

def LPF_FILTER_init(flt_coef, ys, initial_value):
    flt_ys = [initial_value]
    for i in range(1, len(ys)):
        flt_ys.append(((flt_ys[i-1]) + (flt_coef * ((ys[i]) - (flt_ys[i-1])))))
    return flt_ys

def HPF_FILTER(tau, xs):
    ys = [0] * len(xs)
    ys[0] = 0
    for i in range(1, len(xs)):
        ys[i] = tau * (ys[i-1] + xs[i] - xs[i-1])
    return ys

TIME1 = int(len(times)/220)

resis = []
velocity_div_current = []
devCurrent_div_current = []
inv_current = []
temps_fit = []
times_fit = []
vqs_temp = []
iqs_temp = []

iqs_raw = iqs.copy()

for i in range(len(vqs)):
    if iqs[i] != 0 and abs(vqs[i]) > 0.96 and i > TIME1*8:
        resis.append(vqs[i]/iqs[i]) # 0.5 
        velocity_div_current.append(velocitys[i]/iqs[i]) # 25
        inv_current.append(1/iqs[i])
        devCurrent_div_current.append(derivada[i]/iqs[i])
        temps_fit.append(temps_measured[i])
        times_fit.append(times[i])
        vqs_temp.append(vqs[i])
        iqs_temp.append(iqs[i])

vqs = vqs_temp.copy()
iqs = iqs_temp.copy()

# vqs delay treated
vqs = [abs(vqs[i]) for i in range(len(vqs))]
iqs = [abs(iqs[i]) for i in range(len(iqs))]
velocity_div_current = [abs(velocity_div_current[i]) for i in range(len(velocity_div_current))]

velocity_div_current = LPF_FILTER_init(0.001, velocity_div_current, 15)
vqs = LPF_FILTER_init(0.0001, vqs, 2.5)
iqs = LPF_FILTER_init(0.0001, iqs, 4)

# plt.plot(times_fit, iqs, label ="Iqs")
# plt.plot(times_fit, vqs, label ="Vqs")
# plt.legend()
# plt.grid()
# plt.show()

resis_flt = [abs(resis[i]) for i in range(len(resis))]
resis_flt = LPF_FILTER_init(0.001, resis_flt, resis_flt[0])

# plt.plot(times_fit, resis_flt, label = "resis_flt")
# plt.legend()
# plt.show()

# # NEW TEMPS_LSTQ SQUARE
# res_k1 = 109.41
# res_k2 = -2.218
# res_k3 = 0.2502
# res_k4 = 0#-0.000115
# res_k5 = 13.38

# TEMPS_LSTQ SIN
res_k1 = 2410
res_k2 = -0.00818
res_k3 = -0.08191
res_k4 = 0.000359
res_k5 = -1380


# # TEMPS_LSTQ CONSTANTS WITH STOPPED MOTOR
# res_k1 = 879
# res_k2 = -215
# res_k3 = -219


new_lstq = True

temps_lstq = []

if new_lstq:
    for i in range(len(resis_flt)):
        temp_lstq = res_k1*resis_flt[i] + res_k2*velocity_div_current[i] + res_k3*inv_current[i] + res_k4*(devCurrent_div_current[i]) + res_k5
        temp_lstq = round(temp_lstq, 1)
        temps_lstq.append(temp_lstq)
else:
    for i in range(len(vqs)):
        if iqs[i] != 0:
            temp_lstq = res_k1 * (resis_flt[i]) + res_k2 * (1 / iqs[i]) + res_k3
            temp_lstq = round(temp_lstq, 1)
        else:
            temp_lstq = 0
        temps_lstq.append(temp_lstq)

# Fusion temperatures (thermal and LSTQ)
def complementaryFilter(arr_hp, arr_lp, tau_hp, tau_lp):
    arr_hp = HPF_FILTER(tau_hp, arr_hp)
    arr_lp = LPF_FILTER(tau_lp, arr_lp)
    
    arr_filtered = []
    for i in range(len(arr_hp)):
        arr_filtered.append(arr_hp[i] + arr_lp[i])

    # arr_filtered = MEDIAN_FILTER(arr_filtered, 10)

    return arr_filtered

T_AMBIENT = temps_measured[0]
# calculate termique model
def thermal_model(times, iqs):
    K1 = 0.0102
    K2 = 1/529
    K3 = 1 # 45/25
    temps_model = [T_AMBIENT]
    for i in range(0, len(iqs)-1):
        delta_t = temps_model[-1] - T_AMBIENT
        current = iqs[i]*iqs[i]+iqs[i]*iqs[i]
        temp_derivate = ((current * K1) - (delta_t * K2)) * K3
        DT = times[i+1] - times[i]
        temps_model.append(temps_model[-1] + ((temp_derivate) * DT))
    return temps_model

tau = 0.001
temps_model = thermal_model(times, iqs_raw)
# temps_fusion = complementaryFilter(temps_model, temps_lstq, 1-tau, tau)


# Criando a figura e os subplots
fig, axs = plt.subplots(2, 1, figsize=(8, 6))

# Plotando o primeiro gráfico na posição (0, 0) da grade (em cima)
axs[0].plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
# axs[0].plot(times_fit, temps_lstq, 'r.',label="Estimated Temperature with resistance model")
# axs[0].plot(times_fit, temps_fusion, 'y.', label=f"Estimated Fusion Temperature")
axs[0].plot(times, temps_model, 'b.', label=f"Estimated Model Temperature")

axs[0].set_xlabel('Time [s]')
axs[0].set_ylabel('Temperature [° Celsius]')
axs[0].legend()
axs[0].grid()

# Plotando o segundo gráfico na posição (1, 0) da grade (embaixo)
# errors = [temps_fit[i] - temps_lstq[i] for i in range(len(temps_fit))]
# axs[1].plot(times_fit, errors, 'b.')
axs[1].plot(times, iqs_raw, 'b.')
axs[1].set_xlabel('Time [s]')
axs[1].set_ylabel('Current [Ampere]')

plt.show()
