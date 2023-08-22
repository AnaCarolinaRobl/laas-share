import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.optimize import curve_fit
from utils import get_data, LPF_FILTER, HPF_FILTER, complementaryFilter, fusion_model, thermal_model

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

times_raw, ids_raw, iqs_raw, vds_raw, vqs_raw, velocitys_raw, temps_measured_raw, positions_raw = [], [], [], [], [], [], [], []

# filenames = ["rolling_data_SBPA.txt", "rolling_data_sin_sin.txt", "rolling_data_sin_increasing_stopped.txt"]
# filenames = ["rolling_data_Sin_sampled.txt", "rolling_data_sin_increasing_stopped.txt"]
# filenames = ["rolling_data_Sin_sampled.txt", "rolling_data_sin_increasing_stopped.txt", "rolling_data_squared_stop.txt", "rolling_data_sin_sin_stopped.txt"]
filenames = ["rolling_data_PID2.txt"]

# problematicos: rolling_data_sin_increasing_stopped(comeco com erro > 15), rolling_data_sin_3A,(erro por volta de 13), rolling_data_sin_increasing(inicio com erro grande)

for filename in filenames:
    times_temp, ids_temp, iqs_temp, vds_temp, vqs_temp, velocitys_temp, temps_measured_temp, positions_temp = get_data(filename)

    times_raw += times_temp
    ids_raw += ids_temp
    iqs_raw += iqs_temp
    vds_raw += vds_temp
    vqs_raw += vqs_temp
    velocitys_raw += velocitys_temp
    temps_measured_raw += temps_measured_temp
    positions_raw += positions_temp




CURRENT_LIMITS = np.linspace(0.7, 2, 70)
RS = []
best_cl = 0
best_r = 0

CURRENT_LIMIT = 1.6
CURRENT_LIMIT = 1.95
CURRENT_LIMIT = 1.2

for CURRENT_LIMIT in CURRENT_LIMITS:

    resis = []
    inv_current = []
    temps_fit = []
    times_fit = []
    vqs = []
    iqs = []
    velocitys = []

    for i in range(len(vqs_raw)):
        if times_raw[i] > 8 and abs(iqs_raw[i]) > CURRENT_LIMIT:
            inv_current.append(1/iqs_raw[i])
            temps_fit.append(temps_measured_raw[i])
            times_fit.append(times_raw[i])
            vqs.append(vqs_raw[i])
            iqs.append(iqs_raw[i])
            velocitys.append(velocitys_raw[i])

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
    
    r = resultado['R²']
    RS.append(r)
    print(CURRENT_LIMIT, r)

    if r > best_r:
        best_r = r
        best_cl = CURRENT_LIMIT



plt.plot(CURRENT_LIMITS, RS, ".")
plt.title("Current limit [A] x R²")
plt.xlabel('Current [A]')
plt.ylabel('R²')
plt.show()

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
# filenames = ["rolling_data_sin_increasing.txt", "rolling_data_PID.txt", "rolling_data_Sin_sampled.txt", "rolling_data_PID2.txt", "rolling_data_SBPA.txt"] 
# filenames = txt_files


k2 = k2 * 2
k3 = k3 / 150
print("Modelo com parametros ajustados")
print(f"t = {round(k1)}*(u - kv*w)/i + {round(k2)}*i {round(k3, 3)}*w {round(k4)}")



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
    iqs_raw = iqs.copy()

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



    # Criando a figura e os subplots
    fig, axs = plt.subplots(2, 1, figsize=(8, 6))

    # Plotando o primeiro gráfico na posição (0, 0) da grade (em cima)
    tau = 0.001
    axs[0].plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
    axs[0].plot(times_fit, temps_lstq, 'r,', label="Estimated Temperature")
    # axs[0].plot(times_fit, complementaryFilter(temps_model, temps_lstq, 1-tau, tau), ":", label=f"Complementary Filter tau_hp = {1-tau}, tau_lp = {tau}")
    # axs[0].plot(times_fit, fusion_model(temps_lstq, times_fit, ids, iqs), ':', label=f"Fusion Ben")

    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Temperature [° Celsius]')
    axs[0].set_title(f"Filename = {filename[12:]}, current limit = {CURRENT_LIMIT} and R^2 = {round(resultado['R²'], 2)}")
    axs[0].legend()
    axs[0].grid()

    # axs[1].plot(times, iqs_raw, 'r.')
    axs[1].plot(times_fit, iqs, 'r.')
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel('Current [Ampere]')

    plt.show()
