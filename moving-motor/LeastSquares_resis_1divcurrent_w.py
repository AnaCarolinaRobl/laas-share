import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.optimize import curve_fit
from utils import get_data, LPF_FILTER, HPF_FILTER, complementaryFilter, fusion_model

import os

def get_matching_txt_files(folder_path, prefix):
    matching_files = []
    for filename in os.listdir(folder_path):
        if filename.startswith(prefix) and filename.endswith(".txt"):
            matching_files.append(filename)
    return matching_files

folder_path = "./data/"  # Substitua pelo caminho da sua pasta
prefix = "rolling_data"

txt_files = get_matching_txt_files(folder_path, prefix)

times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = [], [], [], [], [], [], [], []

# filenames = ["rolling_data_SBPA.txt", "rolling_data_sin_sin.txt", "rolling_data_sin_increasing_stopped.txt"]
# filenames = ["rolling_data_Sin_sampled.txt", "rolling_data_sin_increasing_stopped.txt"]
filenames = ["rolling_data_Sin_sampled.txt", "rolling_data_sin_increasing_stopped.txt", "rolling_data_squared_stop.txt", "rolling_data_sin_sin_stopped.txt"]
# filenames = ["rolling_data_sin_sin_stopped.txt"]

# problematicos: rolling_data_sin_increasing_stopped(comeco com erro > 15), rolling_data_sin_3A,(erro por volta de 13), rolling_data_sin_increasing(inicio com erro grande)

for filename in filenames:
    times_temp, ids_temp, iqs_temp, vds_temp, vqs_temp, velocitys_temp, temps_measured_temp, positions_temp = get_data(filename)

    times += times_temp
    ids += ids_temp
    iqs += iqs_temp
    vds += vds_temp
    vqs += vqs_temp
    velocitys += velocitys_temp
    temps_measured += temps_measured_temp
    positions += positions_temp


resis = []
inv_current = []
temps_fit = []
times_fit = []
vqs_temp = []
iqs_temp = []
velocitys_temp = []

CURRENT_LIMIT = 1.7

for i in range(len(vqs)):
    if times[i] > 8 and abs(iqs[i]) > CURRENT_LIMIT:
        inv_current.append(1/iqs[i])
        temps_fit.append(temps_measured[i])
        times_fit.append(times[i])
        vqs_temp.append(vqs[i])
        iqs_temp.append(iqs[i])
        velocitys_temp.append(velocitys[i])

velocitys = np.array(velocitys_temp.copy())
vqs = vqs_temp.copy()
iqs = iqs_temp.copy()


kv = 0.01818
# kv = 0.01758
def calculate_resis(u, kv, v, i):
    return (u - kv*v)/i

resis = [calculate_resis(vqs[i], kv, velocitys[i], iqs[i]) for i in range(len(vqs))]
resis = LPF_FILTER(0.001, resis)


# Normalization 
factor_inv_current = 2
factor_velocity = 1/150

for i in range(len(inv_current)):
    velocitys[i] = velocitys[i]*factor_velocity
    inv_current[i] = inv_current[i]*factor_inv_current


velocitys = [abs(velocitys[i]) for i in range(len(velocitys))]
velocitys = LPF_FILTER(0.001, velocitys)

inv_current = [abs(inv_current[i]) for i in range(len(inv_current))]
inv_current = LPF_FILTER(0.001, inv_current)

vqs = [abs(vqs[i]) for i in range(len(vqs))]
vqs = LPF_FILTER(0.001, vqs)


# plt.plot(times_fit, resis, ".")
# plt.title("resistencia")
# plt.show()

# Criando um DataFrame com as duas colunas
x = pd.DataFrame({'resistance': resis, 'inv_current': inv_current, 'velocitys': velocitys})
# x = pd.DataFrame({'resistance': resis, 'velocitys': velocitys})

# plt.plot(times_fit, resis, '.', label="resis")
# plt.plot(times_fit, vqs, '.',label="vqs")
# # plt.plot(times_fit, inv_current, '.',label="inv_current")
# plt.plot(times_fit, velocitys, '.',label="velocitys")
# plt.title("Filename = " + filename)
# plt.xlabel('Time [s]')
# plt.ylabel('Temperature [° Celsius]')
# plt.legend()
# plt.show()



# fig, axs = plt.subplots(2, 1, figsize=(8, 6))

# # Plotando o primeiro gráfico na posição (0, 0) da grade (em cima)
# axs[0].plot(times_fit, velocitys, '.',label="velocitys")
# axs[0].plot(times_fit, inv_current, '.',label="inv_current")
# axs[0].plot(times_fit, vqs, '.',label="vqs")

# axs[0].set_xlabel('Time [s]')
# axs[0].legend()
# axs[0].grid()

# # Plotando o segundo gráfico na posição (1, 0) da grade (embaixo)
# axs[1].plot(times_fit, resis, '.', label="(U - kv*w) / i [Volt / Ampere]")
# axs[1].set_xlabel('Time [s]')
# axs[1].legend()

# plt.show()


x = sm.add_constant(x)
y = temps_fit

model = sm.OLS(y, x).fit()
resultados_regressao = []

resultados_regressao.append({
    'Arquivo': filename,
    'R²': model.rsquared,
    'Coeficientes': model.params,
    'P-Valores': model.pvalues
})

# Exibindo os resultados
for resultado in resultados_regressao:
    print("Arquivo:", resultado['Arquivo'])
    print("R²:", resultado['R²'])
    print("Coeficientes:")
    print(resultado['Coeficientes'])
    print("P-Valores:")
    print(resultado['P-Valores'])
    print("="*50)


k1 = model.params["resistance"]
k2 = model.params["inv_current"]
k3 = model.params["velocitys"]
k4 = model.params["const"]
print(f"t = {round(k1)}*(u - kv*w)/i + {round(k2,1)}*i {round(k3, 1)}*w {round(k4)}")


temps_lstq = []
for i in range(len(resis)):
    temp_lstq = k1*resis[i] + k2*inv_current[i] + k3*velocitys[i] + k4
    # temp_lstq = k1*resis[i] + k3*velocitys[i] + k4
    temps_lstq.append(temp_lstq)


# plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
# plt.plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with resistance model")
# plt.title("Filename = " + filename)
# plt.xlabel('Time [s]')
# plt.ylabel('Temperature [° Celsius]')
# plt.legend()
# plt.show()


## ******************************************* ##
# "rolling_data_sin_increasing_stopped.txt"
filenames = ["rolling_data_SBPA.txt", "rolling_data_PID.txt", "rolling_data_sin_6A.txt", "rolling_data_PID2.txt", "rolling_data_SBPA.txt"] 
# filenames = txt_files


print("Modelo com parametros ajustados")
k2 = k2 * 2
k3 = k3 / 150

# calculate termique model
def thermal_model(times_fit, iqs, ids):
    K1 = 0.0102
    K2 = 1/529
    K3 = 1 # 45/25
    T_AMBIENT = 25
    temps_model = [T_AMBIENT]
    for i in range(0, len(ids)-1):
        delta_t = temps_model[-1] - T_AMBIENT
        current = ids[i]*ids[i] + iqs[i]*iqs[i]
        temp_derivate = ((current * K1) - (delta_t * K2)) * K3
        DT = times_fit[i+1] - times_fit[i]
        temps_model.append(temps_model[-1] + ((temp_derivate) * DT))
    return temps_model



print(f"t = {round(k1)}*(u - kv*w)/i + {round(k2)}*i {round(k3, 3)}*w {round(k4)}")

def complementaryFilter(arr_hp, arr_lp, tau_hp, tau_lp):
    arr_hp = HPF_FILTER(tau_hp, arr_hp)
    arr_lp = LPF_FILTER(tau_lp, arr_lp)
    
    arr_filtered = []
    for i in range(len(arr_hp)):
        arr_filtered.append(arr_hp[i] + arr_lp[i])

    # arr_filtered = MEDIAN_FILTER(arr_filtered, 10)

    return arr_filtered

for filename in filenames:
    times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)


    resis = []
    inv_current = []
    temps_fit = []
    times_fit = []
    vqs_temp = []
    iqs_temp = []
    ids_temp = []
    velocitys_temp = []

    for i in range(len(vqs)):
        if i >times[i] > 8 and abs(iqs[i]) > CURRENT_LIMIT:
            inv_current.append(1/iqs[i])
            temps_fit.append(temps_measured[i])
            times_fit.append(times[i])
            vqs_temp.append(vqs[i])
            iqs_temp.append(iqs[i])
            ids_temp.append(iqs[i])
            velocitys_temp.append(velocitys[i])

    velocitys = np.array(velocitys_temp.copy())
    vqs = vqs_temp.copy()
    iqs = iqs_temp.copy()
    ids = ids_temp.copy()

    resis = [calculate_resis(vqs[i], kv, velocitys[i], iqs[i]) for i in range(len(vqs))]
    resis = LPF_FILTER(0.001, resis)

    velocitys = [abs(velocitys[i]) for i in range(len(velocitys))]
    velocitys = LPF_FILTER(0.001, velocitys)

    inv_current = [abs(inv_current[i]) for i in range(len(inv_current))]
    inv_current = LPF_FILTER(0.001, inv_current)

    temps_lstq = []
    for i in range(len(resis)):
        temp_lstq = k1*resis[i] + k2*inv_current[i] + k3*velocitys[i] + k4
        temps_lstq.append(temp_lstq)

    temps_model = thermal_model(times_fit, iqs, ids)

    tau = 0.001
    plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
    # plt.plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with resistance model")
    plt.plot(times_fit, complementaryFilter(temps_model, temps_lstq, 1-tau, tau), label=f"Complementary Filter tau_hp = {1-tau}, tau_lp = {tau}")
    plt.plot(times_fit, fusion_model(temps_lstq, times_fit, ids, iqs), '.', label=f"Fusion Ben")
    plt.title("Filename = " + filename)
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [° Celsius]')
    plt.legend()
    plt.show()
