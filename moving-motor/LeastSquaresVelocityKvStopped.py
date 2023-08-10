import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.optimize import curve_fit


# Normalizando os dados
scaler = StandardScaler()

# Nome do arquivo de texto
filename = "rolling_data.txt"
# filename = "rolling_data_PID.txt"

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
            if filename == "rolling_data_PID.txt":
                linha.pop()
            
            for i in range(len(linha)):
                datas[i].append(float(linha[i]))

    return datas

def LPF_FILTER(flt_coef, ys, initial_value):
    flt_ys = [initial_value]
    for i in range(1, len(ys)):
        flt_ys.append(((flt_ys[i-1]) + (flt_coef * ((ys[i]) - (flt_ys[i-1])))))
    return flt_ys

times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)

# Cria uma figura com 2 linhas e 2 colunas de subplots
fig, axs = plt.subplots(2, 3, figsize=(12, 8))

axs[0, 0].plot(times, iqs, ',',label="Iqs_Raw")
axs[0, 0].plot(times, vqs, ',', label="Vqs_Raw")
axs[0, 0].set_xlabel('Time [s]')
axs[0, 0].set_ylabel('(Current)(Tension)[(A)(V)]')
axs[0, 0].set_title("Unfiltered Tension and Current")
axs[0, 0].legend()

axs[0, 1].plot(times, velocitys, ',',label="Velocitys_Raw")
axs[0, 1].set_xlabel('Time [s]')
axs[0, 1].set_ylabel('Velocity[rad/s]')
axs[0, 1].set_title("Unfiltered Velocity")
axs[0, 1].legend()

# Filter data
TIME1 = int(len(times)/times[-1])

resis = []
current = []
temps_fit = []
times_fit = []
vqs_temp = []
iqs_temp = []
velocitys_temp = []

KI = 0.2

for i in range(len(vqs)):
    if i > TIME1*8 and abs(iqs[i]) > 2.5:
        current.append(iqs[i]*KI)
        temps_fit.append(temps_measured[i])
        times_fit.append(times[i])
        vqs_temp.append(vqs[i])
        iqs_temp.append(iqs[i])
        velocitys_temp.append(velocitys[i])

velocitys = np.array(velocitys_temp.copy())
vqs = vqs_temp.copy()
iqs = iqs_temp.copy()

kv = 0.0178
def calculate_resis(u, kv, v, i):
    return (u - kv*v)/i

def calculate_resis_i(u, kv, v, i):
    return (u - kv*v)

resis_i = [calculate_resis_i(vqs[i], kv, velocitys[i], iqs[i]) for i in range(len(vqs))]
# resis_i = LPF_FILTER(0.001, resis_i, resis_i[0])

resis = [calculate_resis(vqs[i], kv, velocitys[i], iqs[i]) for i in range(len(vqs))]
resis = LPF_FILTER(0.001, resis, resis[0])

velocitys = velocitys/150
velocitys = [abs(velocitys[i]) for i in range(len(velocitys))]
velocitys = LPF_FILTER(0.001, velocitys, velocitys[0])

current = [abs(current[i]) for i in range(len(current))]
current = LPF_FILTER(0.001, current, current[0])

# Criando um DataFrame com as duas colunas
x = pd.DataFrame({'resistance': resis, 'current': current, 'velocitys': velocitys})

axs[0, 2].plot(times_fit, resis_i, ',',label="U-Kv*w")
axs[0, 2].plot(times_fit, iqs, ',',label="Iqs_Filtred")
axs[0, 2].set_xlabel('Time [s]')
axs[0, 2].set_ylabel('(Resistance*Courrent)(Courrent)[(Ohms*A)(A)]')
axs[0, 2].set_title("Filtered U-Kv*w(Low pass filter and only positive values)")
axs[0, 2].legend()

axs[1, 0].plot(times_fit, current, ',',label="Iqs_Filtred")
axs[1, 0].plot(times_fit, velocitys, ',',label="Velocitys_Filtred")
axs[1, 0].set_xlabel('Time [s]')
axs[1, 0].set_ylabel('(Current)(Velocity)[(A)(rad/s)]')
axs[1, 0].set_title("Filtered Data(Low pass filter and only positive values)")
axs[1, 0].legend()

axs[1, 1].plot(times_fit, resis, ',',label="Resistances_Filtred")
axs[1, 1].set_xlabel('Time [s]')
axs[1, 1].set_ylabel('Resistance[Ohms]')
axs[1, 1].set_title("Filtered Resistance(Low pass filter and only positive values)")
axs[1, 1].legend()

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
k2 = model.params["current"]
k3 = model.params["const"]
k4 = model.params["velocitys"]
print(f"t = {round(k1, 1)}*(u - kv*w)/i {round(k2,4)}*1/i {round(k3, -1)}")


temps_lstq = []
for i in range(len(resis)):
    temp_lstq = k1*resis[i] + k2*current[i] + k3 + k4*velocitys[i]
    temps_lstq.append(temp_lstq)


# axs[1, 1].plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
# axs[1, 1].plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with resistance model")
# axs[1, 1].set_title("Filename = " + filename)
# axs[1, 1].set_xlabel('Time [s]')
# axs[1, 1].set_ylabel('Temperature [° Celsius]')
# axs[1, 1].legend()

# Ajusta os espaços entre os subplots para evitar sobreposição de títulos e rótulos
plt.tight_layout()

plt.show()


## ******************************************* ##

# filenames = ["rolling_data_sin_increasing_stopped.txt", "rolling_data_sin_3A.txt", "rolling_data_Sin_sampled.txt", "rolling_data_squared_stop.txt"]
# # filenames = []

# for filename in filenames:
#     times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)

#     # Filter data
#     TIME1 = int(len(times)/times[-1])

#     resis = []
#     current = []
#     temps_fit = []
#     times_fit = []
#     vqs_temp = []
#     iqs_temp = []
#     velocitys_temp = []

#     KI = 0.2

#     for i in range(len(vqs)):
#         if i > TIME1*8 and abs(iqs[i]) > 2.5:
#             current.append(iqs[i]*KI)
#             temps_fit.append(temps_measured[i])
#             times_fit.append(times[i])
#             vqs_temp.append(vqs[i])
#             iqs_temp.append(iqs[i])
#             velocitys_temp.append(velocitys[i])

#     velocitys = np.array(velocitys_temp.copy())
#     vqs = vqs_temp.copy()
#     iqs = iqs_temp.copy()

#     resis = [calculate_resis(vqs[i], kv, velocitys[i], iqs[i]) for i in range(len(vqs))]
#     resis = LPF_FILTER(0.001, resis, resis[0])

#     velocitys = velocitys/150
#     velocitys = [abs(velocitys[i]) for i in range(len(velocitys))]
#     velocitys = LPF_FILTER(0.001, velocitys, velocitys[0])

#     current = [abs(current[i]) for i in range(len(current))]
#     current = LPF_FILTER(0.001, current, current[0])

#     # Criando um DataFrame com as duas colunas
#     x = pd.DataFrame({'resistance': resis, 'current': current, 'velocitys': velocitys})

#     # plt.plot(times_fit, resis, 'g.', label="resis")
#     # plt.plot(times_fit, current, 'r,',label="current")
#     # plt.plot(times_fit, velocitys, 'r,',label="velocitys")
#     # plt.title("Filename = " + filename)
#     # plt.xlabel('Time [s]')
#     # plt.ylabel('Temperature [° Celsius]')
#     # plt.legend()
#     # plt.show()

#     temps_lstq = []
#     for i in range(len(resis)):
#         temp_lstq = k1*resis[i] + k2*current[i] + k3 + k4*velocitys[i]
#         temps_lstq.append(temp_lstq)


#     plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
#     plt.plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with resistance model")
#     plt.title("Filename = " + filename)
#     plt.xlabel('Time [s]')
#     plt.ylabel('Temperature [° Celsius]')
#     plt.legend()
#     plt.show()