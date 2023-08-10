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

def MEDIAN_FILTER(arr, LENGTH):

    arr_flt = []

    for i in range(0, len(arr)):
        temps_vec = [round(arr[i], 1)]
        j = i-LENGTH
        k = i+LENGTH
        while len(temps_vec) <= (LENGTH*2+1) and j<i:
            if j>=0:
                temps_vec.append(round(arr[j], 1))
            if k < len(arr):
                temps_vec.append(round(arr[k], 1))
            j+=1
            k+=1

        x = round(sum(temps_vec)/len(temps_vec), 1)
        arr_flt.append(x)


    return arr_flt

times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)

# Filter data
TIME1 = int(len(times)/times[-1])

resis = []
current = []
temps_fit = []
times_fit = []
vqs_temp = []
iqs_temp = []
velocitys_temp = []

# velocitys = np.array(velocitys)/150  * 3

KI = 1e-1
KI_3 = 1e-2

for i in range(len(vqs)):
    if i > TIME1*8 and abs(iqs[i]) > 2.5:
        current.append(iqs[i]*KI)
        temps_fit.append(temps_measured[i])
        times_fit.append(times[i])
        vqs_temp.append(vqs[i])
        iqs_temp.append(iqs[i])
        velocitys_temp.append(velocitys[i]*KI_3)

velocitys = velocitys_temp.copy()
vqs = vqs_temp.copy()
iqs = iqs_temp.copy()


current = [abs(current[i]) for i in range(len(current))]
current = LPF_FILTER(0.001, current, current[0])


kv = 0.0178
def calculate_resis(u, kv, v, i):
    return (u - kv*v)/i

resis = [calculate_resis(vqs[i], kv, velocitys[i], iqs[i]) for i in range(len(vqs))]
resis = LPF_FILTER(0.001, resis, resis[0])

velocitys = [abs(velocitys_temp[i]) for i in range(len(velocitys_temp))]
velocitys = LPF_FILTER(0.001, velocitys, velocitys[0])

# Criando um DataFrame com as duas colunas
x = pd.DataFrame({'resistance': resis, 'current': iqs, 'velocity': velocitys})

plt.plot(times_fit, resis, 'g.', label="resis")
plt.plot(times_fit, current, 'r,',label="current")
plt.title("Filename = " + filename)
plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')
plt.legend()
plt.show()

plt.plot(times_fit, velocitys, 'r,',label="velocitys")
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


k1 = model.params["resistance"]
k2 = model.params["current"]
k3 = model.params["velocity"]
k4 = model.params["const"]
print(f"t = {round(k1, 1)}*(u - kv*w)/i {round(k2,4)}*i {round(k3, -1)}*w {k4}")


temps_lstq = []
for i in range(len(resis)):
    temp_lstq = k1*resis[i] + k2*current[i] + k3*velocitys[i] + k4
    temps_lstq.append(temp_lstq)

plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
plt.plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with resistance model")
plt.title("Filename = " + filename)
plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')
plt.legend()
plt.show()




## ******************************************* ##

filenames = ["rolling_data_sin_3A.txt", "rolling_data_sin_6A.txt", "rolling_data_Sin_sampled.txt", "rolling_data_sin.txt", "rolling_data_sin_increasing_stopped.txt"]

for filename in filenames:

    times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)

    # Filter data
    TIME1 = int(len(times)/times[-1])

    resis = []
    current = []
    temps_fit = []
    times_fit = []
    vqs_temp = []
    iqs_temp = []
    velocitys_temp = []

    # velocitys = np.array(velocitys)/150  * 3

    KI = 1e-1

    for i in range(len(vqs)):
        if i > TIME1*8 and abs(iqs[i]) > 2.5:
            current.append(iqs[i]*KI)
            temps_fit.append(temps_measured[i])
            times_fit.append(times[i])
            vqs_temp.append(vqs[i])
            iqs_temp.append(iqs[i])
            velocitys_temp.append(velocitys[i]*KI_3)

    velocitys = velocitys_temp.copy()
    vqs = vqs_temp.copy()
    iqs = iqs_temp.copy()

    current = [abs(current[i]) for i in range(len(current))]
    current = LPF_FILTER(0.001, current, current[0])


    kv = 0.0178
    resis = [calculate_resis(vqs[i], kv, velocitys[i], iqs[i]) for i in range(len(vqs))]
    resis = LPF_FILTER(0.001, resis, resis[0])


    # Criando um DataFrame com as duas colunas
    x = pd.DataFrame({'resistance': resis, 'current': current, 'velocity': velocitys})

    plt.plot(times_fit, resis, 'g.', label="resis")
    plt.plot(times_fit, current, 'r,',label="current")
    plt.title("Filename = " + filename)
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [° Celsius]')
    plt.legend()
    plt.show()


    temps_lstq = []
    for i in range(len(resis)):
        temp_lstq = k1*resis[i] + k2*current[i] + k3*velocitys[i] + k4
        temps_lstq.append(temp_lstq)


    plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
    plt.plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with resistance model")
    plt.title("Filename = " + filename)
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [° Celsius]')
    plt.legend()
    plt.show()