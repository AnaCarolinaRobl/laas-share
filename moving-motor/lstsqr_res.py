import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.optimize import curve_fit
from utils import get_data, LPF_FILTER, HPF_FILTER, complementaryFilter, fusion_model, thermal_model, get_matching_txt_files

txt_files = get_matching_txt_files()

times_raw, ids_raw, iqs_raw, vds_raw, vqs_raw, velocitys_raw, temps_measured_raw, positions_raw = [], [], [], [], [], [], [], []

filenames = ["rolling_data_sin_sin_stopped.txt"]
# filenames = ["rolling_data_sin_sin.txt"]
# filenames = ["rolling_data_sin_3A.txt"]
# filenames = ["rolling_data_PID.txt"]


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


CURRENT_LIMIT = 1.6
# CURRENT_LIMIT = 1.95
# CURRENT_LIMIT = 1.2

resis = []
inv_current = []
times_fit = []
vqs = []
iqs = []
velocitys = []

for i in range(len(vqs_raw)):
    if times_raw[i] > 130 and times_raw[i] < 140 and abs(iqs_raw[i]) > CURRENT_LIMIT:
        times_fit.append(times_raw[i])
        vqs.append(vqs_raw[i])
        iqs.append(iqs_raw[i])
        velocitys.append(velocitys_raw[i])


# Criando um DataFrame com as duas colunas
x = pd.DataFrame({'vqs': vqs, 'velocitys': velocitys})

plt.plot(times_fit, vqs, '.', label="vqs")
plt.plot(times_fit, velocitys, '.',label="velocitys")
plt.plot(times_raw, temps_measured_raw, '.', label="temps_measured_raw")
plt.title("Filename = " + filename)
plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')
plt.legend()
plt.show()


x = sm.add_constant(x)
y = iqs

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

k1 = model.params["vqs"]
k2 = model.params["velocitys"]
k3 = model.params["const"]
print(f"i = {k1}*u + {k2}*v + {k3}")
r = 1/k1
kv = k2/r
print(f"Resis = {r}, Kv = {kv}")


iqs_estimed = []
for i in range(len(vqs)):
    iqs_estimed.append(k1*vqs[i] + k2*velocitys[i] + k3)


# plt.plot(times_fit, iqs, 'g.', label="Measured Current")
# plt.plot(times_fit, iqs_estimed, 'r,',label="Estimated Current")
# plt.title("Filename = " + filename)
# plt.xlabel('Time [s]')
# plt.ylabel('Current [Ampere]')
# plt.legend()
# plt.show()


resis_estimed = []
for i in range(len(vqs)):
    resis_estimed.append((vqs[i] + kv*velocitys[i] + k3) / iqs[i])

# plt.plot(times_fit, iqs, 'g.', label="Measured Current")
plt.plot(times_fit, resis_estimed, 'r,',label="Estimated Current")
plt.title("Filename = " + filename)
plt.xlabel('Time [s]')
plt.ylabel('Current [Ampere]')
plt.legend()
plt.show()

#######################################################################
# TEMPERATURE FIT

filenames = ["rolling_data_Sin_sampled.txt", "rolling_data_sin_increasing_stopped.txt", "rolling_data_squared_stop.txt", "rolling_data_sin_sin_stopped.txt"]
# problematicos: rolling_data_sin_increasing_stopped(comeco com erro > 15), rolling_data_sin_3A,(erro por volta de 13), rolling_data_sin_increasing(inicio com erro grande)

times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = [], [], [], [], [], [], [], []

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

CURRENT_LIMIT = 1.6
factor_current = 2
factor_velocity = 1/75

def process_data(times, ids, iqs, vds, vqs, velocitys, temps_measured, positions):
    resis = []
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
            resis.append((vqs[i] + kv*velocitys[i] + k3) / iqs[i])

    # plt.plot(times_fit, velocity_div_current, '.', label="velocity_div_current")
    # plt.plot(times_fit, inv_current, '.', label="inv_current")
    # plt.title("Filename = " + filename)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [° Celsius]')
    # plt.legend()
    # plt.show()

    return resis, times_fit, temps_fit

resis, times_fit, temps_fit = process_data(times, ids, iqs, vds, vqs, velocitys, temps_measured, positions)

# Criando um DataFrame com as duas colunas
x = pd.DataFrame({'resis': resis})
x = sm.add_constant(x)
y = temps_fit

model = sm.OLS(y, x).fit()

resultado = {
    'Arquivo': filename,
    'R²': model.rsquared,
    'Coeficientes': model.params,
    'P-Valores': model.pvalues
}

print("Arquivo:", resultado['Arquivo'])
print("R²:", resultado['R²'])
print("Coeficientes:")
print(resultado['Coeficientes'])
print("P-Valores:")
print(resultado['P-Valores'])
print("="*50)


k1_temp = model.params["resis"]
k2_temp = model.params["const"]
print(f"t = {k1_temp}*resis + {k2_temp}")

temps_lstq = []
for i in range(len(resis)):
    temp_lstq = k1_temp*resis[i] + k2_temp
    temps_lstq.append(temp_lstq)


plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
plt.plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with original equation")
plt.title("Filename = " + filename)
plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')
plt.legend()
plt.show()
