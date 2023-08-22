import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.optimize import curve_fit
from numpy import linalg
from scipy.optimize import minimize
from utils import get_matching_txt_files, get_data, LPF_FILTER


txt_files = get_matching_txt_files()

times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = [], [], [], [], [], [], [], []

# filenames = ["rolling_data_PID2.txt"]
# filenames = ["rolling_data_Sin_sampled.txt", "rolling_data_sin_increasing_stopped.txt"]
# filenames = ["rolling_data_Sin_sampled.txt", "rolling_data_sin_increasing_stopped.txt", "rolling_data_squared_stop.txt", "rolling_data_sin_sin_stopped.txt"]
filenames = ["rolling_data_sin_sin_stopped.txt"]
# filenames = txt_files

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

CURRENT_LIMIT = 1.6
factor_current = 2
factor_velocity = 1/75


def process_data(times, ids, iqs, vds, vqs, velocitys, temps_measured, positions):
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


    velocitys = [abs(velocitys[i]) for i in range(len(velocitys))]
    velocitys = LPF_FILTER(0.001, velocitys)

    iqs = [abs(iqs[i]) for i in range(len(iqs))]
    iqs = LPF_FILTER(0.001, iqs)

    vqs = [abs(vqs[i]) for i in range(len(vqs))]
    vqs = LPF_FILTER(0.001, vqs)


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

    for i in range(len(inv_current)):
        velocity_div_current[i] = velocity_div_current[i]*factor_velocity
        inv_current[i] = inv_current[i]*factor_current


    plt.plot(times_fit, velocity_div_current, '.', label="velocity_div_current")
    plt.plot(times_fit, inv_current, '.', label="inv_current")
    plt.title("Filename = " + filename)
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [° Celsius]')
    plt.legend()
    plt.show()

    return tension_div_current, inv_current, velocity_div_current, times_fit, temps_fit

tension_div_current, inv_current, velocity_div_current, times_fit, temps_fit = process_data(times, ids, iqs, vds, vqs, velocitys, temps_measured, positions)

# Criando um DataFrame com as duas colunas
x = pd.DataFrame({'tension_div_current': tension_div_current, 'inv_current': inv_current, 'velocity_div_current': velocity_div_current})


# x = np.array([tension_div_current, inv_current, velocity_div_current, [1]*len(velocity_div_current)]).T
# y = np.array(temps_fit)
# x = [tension_div_current, inv_current, velocity_div_current, [1]*len(velocity_div_current)]
x = pd.DataFrame({'tension_div_current': tension_div_current, 'inv_current': inv_current, "velocity_div_current": velocity_div_current})
x = sm.add_constant(x)
y = temps_fit

# model = sm.OLS(y, x).fit()

# resultado = {
#     'Arquivo': filename,
#     'R²': model.rsquared,
#     'Coeficientes': model.params,
#     'P-Valores': model.pvalues
# }

# print("Arquivo:", resultado['Arquivo'])
# print("R²:", resultado['R²'])
# print("Coeficientes:")
# print(resultado['Coeficientes'])
# print("P-Valores:")
# print(resultado['P-Valores'])
# print("="*50)


# k1 = model.params["tension_div_current"]
# k2 = model.params["inv_current"]
# k3 = model.params["velocity_div_current"]
# k4 = model.params["const"]
# print(f"t = {round(k1)}*u/i + {round(k2,1)}/i {round(k3, 1)}*w/i {round(k4)}")


# Função que você deseja ajustar
def model_function(params, x):
    a, b, c, d = params
    return a * x[:, 0]**2 + b * x[:, 1] + c * x[:, 2] + d

# Função de erro a ser minimizada
def error_function(params, x, y):
    predictions = model_function(params, x)
    return np.sum((y - predictions)**2)

x_data = np.array([tension_div_current, inv_current, velocity_div_current, [1]*len(velocity_div_current)]).T
y_data = np.array(temps_fit)
initial_parameters = [465, -101, 8.6, -94]
result = minimize(error_function, initial_parameters, args=(x_data, y_data))

# Os parâmetros otimizados são armazenados em result.x
k1, k2, k3, k4 = result.x


print(result.x)

# k1, k2, k3, k4 = [465, -101, 8.6, -94]
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
# filenames = ["rolling_data_sin_sin_stopped2.txt", "rolling_data_PID.txt", "rolling_data_sin_6A.txt", "rolling_data_PID2.txt", "rolling_data_SBPA.txt"] 
# filenames = txt_files
for filename in filenames:
    times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)
    tension_div_current, inv_current, velocity_div_current, times_fit, temps_fit = process_data(times, ids, iqs, vds, vqs, velocitys, temps_measured, positions)
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