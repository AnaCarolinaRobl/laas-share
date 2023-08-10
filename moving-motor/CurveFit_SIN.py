import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.optimize import curve_fit



# Normalizando os dados
scaler = StandardScaler()

# Nome do arquivo de texto
filename = "rolling_data_sin_6A.txt"

def get_data(filename):
    # Matrix para armazenar os valores
    datas = [[] for i in range(8)]

    # Leitura do arquivo de texto
    with open(filename, "r") as arquivo:
        # Ignora a primeira linha (cabeçalho)
        next(arquivo)
        # Lê as linhas restantes do arquivo
        for linha in arquivo:
            # Divide a linha em comando e corrente
            linha = linha.strip().split(",")
            for i in range(len(linha)):
                datas[i].append(float(linha[i]))

    return datas


def LPF_FILTER(flt_coef, ys, initial_value):
    flt_ys = [initial_value]
    for i in range(1, len(ys)):
        flt_ys.append(((flt_ys[i-1]) + (flt_coef * ((ys[i]) - (flt_ys[i-1])))))
    return flt_ys


times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)


# Filter data
TIME1 = int(len(times)/times[-1])

# data to fitting
temps_fit = []
times_fit = []
vqs_fit = []
iqs_fit = []
velocitys_fit = []

# data to fitting
temps_fit2 = []
times_fit2 = []
vqs_fit2 = []
iqs_fit2 = []
velocitys_fit2 = []

# velocitys = np.array(velocitys) / 150 * 3

for i in range(len(vqs)):
    if i > TIME1 and abs(iqs[i]) > 2.5:
        temps_fit.append(temps_measured[i])
        times_fit.append(times[i])
        vqs_fit.append(vqs[i])
        iqs_fit.append(iqs[i])
        velocitys_fit.append(velocitys[i])


    
# Filter data
# TIME1 = int(len(times_estimate)/times_estimate[-1])

# plt.plot(times_fit, iqs_fit, 'g.', label="Y_data")
# plt.plot(times_fit, vqs_fit, 'g.', label="Y_data")
# plt.plot(times_fit, velocitys_fit, 'g.', label="Y_data")
# plt.xlabel('Time [s]')
# plt.ylabel('Temperature [° Celsius]')
# plt.legend()
# plt.show()


def model_function(x, k1, k2):
    u, w = x
    return (u - k1*w)*k2


# Fitting to find Kv
x_data = [vqs_fit, velocitys_fit]
y_data = iqs_fit
params,_ = curve_fit(model_function, x_data, y_data)
kv, k2 = params
print(params)

y_estimed = []
for i in range(len(iqs_fit)):
    y_estimed.append((vqs_fit[i] - kv*velocitys_fit[i])*k2)

# plt.plot(times_fit, y_data, 'g.', label="Y_data")
# plt.plot(times_fit, y_estimed, label="Estimated")
# plt.title("CurveFIT with " + filename)
# plt.xlabel('Time [s]')
# plt.ylabel('Current [A]')
# plt.legend()
# plt.show()


# Ajusta os espaços entre os subplots para evitar sobreposição de títulos e rótulos
# plt.tight_layout()
# plt.show()


## ******************************************* ##
# CURVE FIT TEMPERATURA = RESISTANCE*k1 + k2


filename = "rolling_data_sin_increasing.txt"
times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)

temps_fit = []
times_fit = []
vqs_temp = []
iqs_temp = []
velocitys_temp = []

for i in range(len(vqs)):
    if iqs[i] != 0 and i > TIME1*8 and abs(iqs[i])>2.5:
        temps_fit.append(temps_measured[i])
        times_fit.append(times[i])
        vqs_temp.append(vqs[i])
        iqs_temp.append(iqs[i])
        velocitys_temp.append(velocitys[i])

vqs = vqs_temp.copy()
iqs = iqs_temp.copy()
velocitys = velocitys_temp.copy()


def calculate_resis(u, kv, v, i):
    return (u - kv*v)/i

resis = [calculate_resis(vqs[i], kv, velocitys[i], iqs[i]) for i in range(len(vqs))]
resis_flt = LPF_FILTER(0.001, resis, resis[0])

plt.plot(times_fit, resis_flt, 'g.', label="Resistance Filter")
plt.legend()
plt.show()


def temp_function(res, k1, k2):
    return res*k1 + k2

x_data = resis_flt
y_data = temps_fit
params,_ = curve_fit(temp_function, x_data, y_data)
k1_temp, k2_temp = params


temps_estimed= [temp_function(resis_flt[i], k1_temp, k2_temp) for i in range(len(resis_flt))]

plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
plt.plot(times_fit, temps_estimed, 'r.',label="Estimated Temperature with resistance model")

plt.title("Filename = " + filename)
plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')
plt.legend()
plt.show()




# *************************************** #

filename = "rolling_data_sin_6A.txt"
times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)

temps_fit = []
times_fit = []
vqs_temp = []
iqs_temp = []
velocitys_temp = []

for i in range(len(vqs)):
    if iqs[i] != 0 and i > TIME1*8 and abs(iqs[i])>2.5:
        temps_fit.append(temps_measured[i])
        times_fit.append(times[i])
        vqs_temp.append(vqs[i])
        iqs_temp.append(iqs[i])
        velocitys_temp.append(velocitys[i])

vqs = vqs_temp.copy()
iqs = iqs_temp.copy()
velocitys = velocitys_temp.copy()

resis = [calculate_resis(vqs[i], kv, velocitys[i], iqs[i]) for i in range(len(vqs))]
resis_flt = LPF_FILTER(0.001, resis, resis[0])

plt.plot(times_fit, resis_flt, 'g.', label="Resistance Filter")
plt.legend()
plt.show()


def temp_function(res, k1, k2):
    return res*k1 + k2

# x_data = resis_flt
# y_data = temps_fit
# params,_ = curve_fit(temp_function, x_data, y_data)
# k1_temp, k2_temp = params


temps_estimed= [temp_function(resis_flt[i], k1_temp, k2_temp) for i in range(len(resis_flt))]

plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
plt.plot(times_fit, temps_estimed, 'r.',label="Estimated Temperature with resistance model")

plt.title("Filename = " + filename)
plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')
plt.legend()
plt.show()
