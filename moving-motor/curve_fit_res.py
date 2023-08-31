import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.optimize import curve_fit
from utils import get_data, LPF_FILTER, HPF_FILTER, complementaryFilter, fusion_model, thermal_model, get_matching_txt_files

txt_files = get_matching_txt_files()

times_raw, ids_raw, iqs_raw, vds_raw, vqs_raw, velocitys_raw, temps_measured_raw, positions_raw = [], [], [], [], [], [], [], []

filenames = ["rolling_data_sin_increasing_stopped.txt"]
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


CURRENT_LIMIT =0.3
# CURRENT_LIMIT = 1.95
# CURRENT_LIMIT = 1.2

resis = []
inv_current = []
times_fit = []
vqs = []
iqs = []
velocitys = []

for i in range(len(vqs_raw)):
    # if times_raw[i] > 130 and times_raw[i] < 140 and abs(iqs_raw[i]) > CURRENT_LIMIT:
    if abs(iqs_raw[i]) > CURRENT_LIMIT:
        times_fit.append(times_raw[i])
        vqs.append(vqs_raw[i])
        iqs.append(iqs_raw[i])
        velocitys.append(velocitys_raw[i])

def estimate_curent(x, kv, offset, inv_res):
    u, w, _ = x
    return (u - kv*w - offset)*inv_res 


# Fitting to find Kv
x_data = [vqs, velocitys, [1]*len(vqs)]
y_data = iqs
params,_ = curve_fit(estimate_curent, x_data, y_data)
kv, offset, inv_res = params
print("Params: ", params)

y_estimed = []
for i in range(len(iqs)):
    y_estimed.append((vqs[i] - kv*velocitys[i] - offset)*inv_res )

# plt.plot(times_fit, y_data, 'g.', label="Y_data")
# plt.plot(times_fit, y_estimed, ',', label="(vqs[i] - kv*velocitys[i] - offset)*inv_res")
plt.plot(times_fit, (np.array(y_estimed)/inv_res)/np.array(y_data), ',', label="resis")
plt.title("CurveFIT with " + filename)
plt.xlabel('Time [s]')
plt.legend()
plt.show()

def calculate_resis(vqs, velocity, kv, offset, iqs):
    return ((vqs[i] - kv*velocitys[i] - offset)/iqs)

resis = []
for i in range(len(vqs)):
    resis.append((vqs[i] - kv*velocitys[i] - offset)/iqs[i])

plt.plot(times_fit, resis, 'g.', label="resis")
plt.plot(times_fit, LPF_FILTER(0.001, resis), '.', label="resis")
plt.title("CurveFIT with " + filename)
plt.xlabel('Time [s]')
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


def process_data(times, ids, iqs, vds, vqs, velocitys, temps_measured, positions):
    resis = []
    temps_fit = []
    times_fit = []
    vqs_temp = []
    iqs_temp = []
    velocitys_temp = []

    resis = []


    for i in range(len(vqs)):
        if times[i] > 8 and abs(iqs[i]) > CURRENT_LIMIT:
            # raw values filtered
            temps_fit.append(temps_measured[i])
            times_fit.append(times[i])
            vqs_temp.append(vqs[i])
            iqs_temp.append(iqs[i])
            velocitys_temp.append(velocitys[i])

            resis.append((vqs[i] - kv*velocitys[i] - offset)/iqs[i])

    resis = LPF_FILTER(0.001, resis)

    iqs_temp = [abs(iqs[i]) for i in range(len(iqs_temp))]
    iqs_temp = LPF_FILTER(0.001, iqs_temp)
    
    velocitys_temp = [abs(velocitys_temp[i]) for i in range(len(velocitys_temp))]
    velocitys_temp = LPF_FILTER(0.001, velocitys_temp)

    plt.plot(times_fit, resis, '.', label="resis")
    # plt.plot(times_fit, inv_current, '.', label="inv_current")
    plt.title("Filename = " + filename)
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [° Celsius]')
    plt.legend()
    plt.show()

    return resis, times_fit, temps_fit, iqs_temp, velocitys_temp

resis, times_fit, temps_fit, iqs, velocitys = process_data(times, ids, iqs, vds, vqs, velocitys, temps_measured, positions)

# Criando um DataFrame com as duas colunas
x = pd.DataFrame({'resis': resis, "iqs": iqs, "velocitys": velocitys})
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
k3_temp = model.params["iqs"]
k4_temp = model.params["velocitys"]
print(f"t = {k1_temp}*resis + {k2_temp}")

temps_lstq = []
for i in range(len(resis)):
    temp_lstq = k1_temp*resis[i] + k2_temp + k3_temp*iqs[i] + k4_temp*velocitys[i]
    temps_lstq.append(temp_lstq)


plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
plt.plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with original equation")
plt.title("Filename = " + filename)
plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')
plt.legend()
plt.show()
