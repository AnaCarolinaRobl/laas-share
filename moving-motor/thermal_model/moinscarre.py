import matplotlib.pyplot as plt
import sys
sys.path.append('../')  # Adiciona o diretório pai (pasta_principal) ao PATH
import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.optimize import curve_fit
from utils import get_data, LPF_FILTER, HPF_FILTER, complementaryFilter, fusion_model, thermal_model

import os


times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = [], [], [], [], [], [], [], []

# filenames = ["rolling_data_Sin_sampled.txt", "rolling_data_sin_increasing_stopped.txt", "rolling_data_squared_stop.txt", "rolling_data_sin_sin_stopped.txt", "rolling_data_sin_3A.txt"]
# filenames = ["rolling_data_Sin_sampled.txt", "rolling_data_sin_increasing_stopped.txt", "rolling_data_squared_stop.txt", "rolling_data_sin_sin_stopped.txt", "rolling_data_sin_3A.txt"]


# filenames = ["rolling_data_sin_sin.txt", "rolling_data_sin_increasing_stopped.txt", "rolling_data_sin_sin_stopped.txt", "rolling_data_PID_SIN.txt"]
filenames = ["rolling_data_2A.txt", "rolling_data_2p5A.txt", "rolling_data_3A_new.txt"]
# filenames = ["rolling_data_PID_SIN_0.txt"]
# filenames, CURRENT_LIMIT_TRAIN, CURRENT_LIMIT = ["rolling_data_PID2.txt", "rolling_data_PID.txt"], 1.7, 3
# filenames, CURRENT_LIMIT_TRAIN, CURRENT_LIMIT = ["rolling_data_Sin_sampled.txt", "rolling_data_sin_increasing_stopped.txt", "rolling_data_squared_stop.txt", "rolling_data_sin_sin_stopped.txt"], 1.7, 3


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

t=5
time = 0
temperature = temps_measured[0]
T_AMB = temps_measured[0]
# i = ids[0]

deltas_temperature = []
deltas_temperature_derivade = []
i_carre = []
i_moy = 0
count = 0
timess = []
is_moy = []
### soma dos 5
for i in (range(len(times))):
    i_moy+=abs(ids[i])
    count+=1
    if(times[i]-time>=t):
        time=times[i]
        delta_temperature = temps_measured[i] - temperature
        delta_temperature_AMB = temps_measured[i] - T_AMB
        i_moy = i_moy/count
        is_moy.append(i_moy)
        i_carre.append(i_moy**2)
        deltas_temperature.append(delta_temperature_AMB)
        deltas_temperature_derivade.append(delta_temperature/t)
        temperature = temps_measured[i]
        timess.append(times[i])
        i_moy = 0
        count = 0

        
# plt.plot(timess, deltas_temperature)
# plt.show()

# Criando um DataFrame com as duas colunas
x = pd.DataFrame({'i_carre': i_carre, 'deltas_temperature': deltas_temperature})

y = deltas_temperature_derivade

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


K1 = model.params["i_carre"]
K2 = model.params["deltas_temperature"]

print(f"t = {K1}*i**2 + {K2}*delta_t ")

## ******************************************* ##

# filenames = ["rolling_data_PID2.txt"] 
filenames = ["rolling_data_PID_SIN_0.txt","rolling_data_PID_SIN_1.txt","rolling_data_PID_SIN_2.txt" ] 
# filenames = txt_files

for filename in filenames:
    times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)
    temps_fusion=[temps_measured[0]]

    # K1 = 0.0102
    # K2 = 1/529
    # K1 = 0.010294078001999562 
    # K2 = 0.0011876190612097718
    T_AMBIENT = 26
    THRUST_LIM_VELOCITY = 20
    THRUST_LIM_CURRENT = 3
    tau = 0.001
    r, v, inv_i = 0.33, 0, .25
    thrust_values = []
    rs, vs, inv_is = [], [], []

    # CURRENT_LIMIT = 2
    for i in range(len(vqs) - 1):
        # thermal model
        delta_t = temps_fusion[-1] - T_AMBIENT
        current = ids[i]*ids[i]+iqs[i]*iqs[i]
        temp_derivate = (current * K1) + (delta_t * K2)
        DT = times[i+1] - times[i]

        temp_thermal = temps_fusion[-1] + ((temp_derivate) * DT)
        # temps_fusion.append(temp_thermal)

        temps_fusion.append(temp_thermal)
        rs.append(0)
        inv_is.append(0)
        vs.append(0)
        thrust_values.append(0)

        


    times = np.array(times)
    thrust_values += [thrust_values[-1]]

    thrust_values = np.array(thrust_values)
    iqs = np.array(iqs)
    temps_fusion = np.array(temps_fusion)

    # Criando a figura e os subplots
    fig, axs = plt.subplots(2, 1, figsize=(8, 6))
    # Plotando o primeiro gráfico na posição (0, 0) da grade (em cima)
    axs[0].plot(times/60, temps_measured, 'g.', label="Measured Temperature")
    axs[0].plot(times/60, temps_fusion, '.', label=f"Fusion Ben")
    # axs[0].plot(times[(thrust_values > 0.1)]/60, temps_fusion[thrust_values > 0.1] , 'r.', label='thrust_values > 0.1')
    # axs[0].plot(times[(abs(iqs) > CURRENT_LIMIT)]/60, temps_fusion[abs(iqs) > CURRENT_LIMIT] , '.', label='iqs > CURRENT_LIMIT')
    # axs[0].plot(times, np.array(thrust_values+[thrust_values[-1]])/np.max(thrust_values), '.', label=f"thrust_values")


    axs[0].set_xlabel('Time [Minutes]')
    axs[0].set_ylabel('Temperature [° Celsius]')
    axs[0].set_title(f"Filename = {filename[13:]}")
    axs[0].legend()
    axs[0].grid()

    # axs[1].plot(rs, '.', label="rs")
    # axs[1].plot(vs, '.', label="vs")
    # axs[1].plot(inv_is, '.', label="inv_is")
    # axs[1].plot(times, thrust_values, '.', label="thrust")
    # axs[1].plot(times, np.array(abs(iqs)), '.', label="iqs")
    # axs[1].plot(times, np.array(rs+[rs[-1]])/np.max(rs), '.', label=f"rs")
    # axs[1].plot(times, np.array(vs+[vs[-1]])/np.max(vs), '.', label=f"vs")
    # axs[1].plot(times, np.array(inv_is+[inv_is[-1]])/np.max(inv_is), '.', label=f"inv_is")
    # axs[1].plot(times, np.array(velocitys / max(velocitys)), '.', label="velocitys")
    # axs[1].legend()
    # axs[1].set_xlabel('Time [s]')
    # axs[1].set_ylabel('Current [Ampere]')

    plt.show()
