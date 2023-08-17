import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.optimize import curve_fit

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

def get_data(filename):
    # Matrix para armazenar os valores
    datas = [[] for i in range(8)]

    # Leitura do arquivo de texto
    with open("./data/" + filename, "r") as arquivo:
        # Ignora a primeira linha (cabeçalho)
        next(arquivo)
        # Lê as linhas restantes do arquivo
        for linha in arquivo:
            # Divide a linha em comando e corrente
            linha = linha.strip().split(",")
            for i in range(len(datas)):
                datas[i].append(float(linha[i]))

    return datas


def LPF_FILTER(flt_coef, ys, initial_value):    
    flt_ys = [initial_value]
    for i in range(1, len(ys)):
        flt_ys.append(((flt_ys[i-1]) + (flt_coef * ((ys[i]) - (flt_ys[i-1])))))
    return flt_ys


times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = [], [], [], [], [], [], [], []

# filenames = ["rolling_data_sin_sin.txt"]
# filenames = ["rolling_data_Sin_sampled.txt", "rolling_data_sin_increasing_stopped.txt"]
# filenames = ["rolling_data_Sin_sampled.txt", "rolling_data_sin_increasing_stopped.txt", "rolling_data_squared_stop.txt", "rolling_data_sin_sin_stopped.txt"]
filenames = txt_files

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

inv_current = []
tension_div_current = []
velocity_div_current = []

CURRENT_LIMIT = 1.9

for i in range(len(vqs)):
    if times[i] > 8 and abs(iqs[i]) > CURRENT_LIMIT:
        # raw values filtered
        temps_fit.append(temps_measured[i])
        times_fit.append(times[i])
        vqs_temp.append(vqs[i])
        iqs_temp.append(iqs[i])
        velocitys_temp.append(velocitys[i])

        # fit values filtered
        inv_current.append(1/iqs[i])
        tension_div_current.append(vqs[i]/iqs[i])
        velocity_div_current.append(velocitys[i]/iqs[i])


velocitys = velocitys_temp.copy()
vqs = vqs_temp.copy()
iqs = iqs_temp.copy()


# Normalization 
factor_current = 2
factor_velocity = 1/150

for i in range(len(inv_current)):
    velocitys[i] = velocitys[i]*factor_velocity
    inv_current[i] = inv_current[i]*factor_current


# Criando um DataFrame com as duas colunas
x = pd.DataFrame({'tension_div_current': tension_div_current, 'inv_current': inv_current, 'velocity_div_current': velocity_div_current})

plt.plot(times_fit, tension_div_current, '.', label="tension_div_current")
plt.plot(times_fit, inv_current, '.',label="inv_current")
plt.plot(times_fit, velocity_div_current, '.',label="velocity_div_current")
plt.title("Filename = " + filename)
plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')
plt.legend()
plt.show()


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


k1 = model.params["tension_div_current"]
k2 = model.params["inv_current"]
k3 = model.params["velocity_div_current"]
k4 = model.params["const"]
print(f"t = {round(k1)}*u/i + {round(k2,1)}/i {round(k3, 1)}*w/i {round(k4)}")


temps_lstq = []
for i in range(len(tension_div_current)):
    temp_lstq = k1*tension_div_current[i] + k2*inv_current[i] + k3*velocity_div_current[i] + k4
    temps_lstq.append(temp_lstq)


plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
plt.plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with original equation")
plt.title("Filename = " + filename)
plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')
plt.legend()
plt.show()


## ******************************************* ##
# "rolling_data_sin_increasing_stopped.txt"
filenames = ["rolling_data_sin_sin_stopped2.txt", "rolling_data_PID.txt", "rolling_data_sin_6A.txt", "rolling_data_PID2.txt", "rolling_data_SBPA.txt"] 
filenames = txt_files

for filename in filenames:
    times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)

    resis = []
    inv_current = []
    temps_fit = []
    times_fit = []
    vqs_temp = []
    iqs_temp = []
    velocitys_temp = []

    inv_current = []
    tension_div_current = []
    velocity_div_current = []

    for i in range(len(vqs)):
        if times[i] > 8 and abs(iqs[i]) > CURRENT_LIMIT:
            # raw values filtered
            temps_fit.append(temps_measured[i])
            times_fit.append(times[i])
            vqs_temp.append(vqs[i])
            iqs_temp.append(iqs[i])
            velocitys_temp.append(velocitys[i])

            # fit values filtered
            inv_current.append(1/iqs[i])
            tension_div_current.append(vqs[i]/iqs[i])
            velocity_div_current.append(velocitys[i]/iqs[i])


    velocitys = velocitys_temp.copy()
    vqs = vqs_temp.copy()
    iqs = iqs_temp.copy()


    # Normalization 
    factor_current = 2
    factor_velocity = 1/150

    for i in range(len(inv_current)):
        velocitys[i] = velocitys[i]*factor_velocity
        inv_current[i] = inv_current[i]*factor_current


    temps_lstq = []
    for i in range(len(tension_div_current)):
        temp_lstq = k1*tension_div_current[i] + k2*inv_current[i] + k3*velocity_div_current[i] + k4
        temps_lstq.append(temp_lstq)


    plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
    plt.plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with original equation")
    plt.title("Filename = " + filename)
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [° Celsius]')
    plt.legend()
    plt.show()