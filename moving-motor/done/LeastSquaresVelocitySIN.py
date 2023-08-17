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



times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)


# Calcular a derivada dos dados
derivada = np.gradient(iqs, times)
# Filter data
TIME1 = int(len(times)/times[-1])

resis = []
velocity_div_current = []
devCurrent_div_current = []
inv_current = []
temps_fit = []
times_fit = []
vqs_temp = []
iqs_temp = []
velocitys_temp = []

plt.plot(times, velocitys, 'b.',label="velocitys")
plt.legend()
plt.grid()
plt.show()

velocitys = np.array(velocitys)/150  * 3

for i in range(len(vqs)):
    if iqs[i] != 0 and abs(vqs[i]) > 0.96 and i > TIME1*8 and abs(velocitys[i]) < 3 and iqs[i] > 0.5:
        resis.append(vqs[i]/iqs[i]) 
        velocity_div_current.append(velocitys[i]/iqs[i])
        inv_current.append(1/iqs[i])
        devCurrent_div_current.append(derivada[i]/iqs[i])
        temps_fit.append(temps_measured[i])
        times_fit.append(times[i])
        vqs_temp.append(vqs[i])
        iqs_temp.append(iqs[i])
        velocitys_temp.append(velocitys[i])

velocitys_temp = [abs(velocitys_temp[i]) for i in range(len(velocitys_temp))]
plt.plot(times_fit, velocitys_temp, 'b.',label="velocitys_temp")
plt.legend()
plt.grid()
plt.show()

vqs = vqs_temp.copy()
iqs = iqs_temp.copy()


# vqs delay treated
# vqs = [abs(vqs[i]) for i in range(len(vqs))]
# iqs = [abs(iqs[i]) for i in range(len(iqs))]
# resis = [vqs[i]/iqs[i] for i in range(len(vqs))]

# vqs = LPF_FILTER(0.0001, vqs, vqs[0])
# iqs = LPF_FILTER(0.0001, iqs, iqs[0])

# velocity_div_current = [abs(velocity_div_current[i]) for i in range(len(velocity_div_current))]
# velocity_div_current = LPF_FILTER(0.0001, velocity_div_current, velocity_div_current[0])

# plt.plot(times_fit[:TIME1*10], iqs[:TIME1*10], 'r.',label="Iq")
# plt.plot(times_fit[:TIME1*10], vqs[:TIME1*10], 'b.',label="Vqs")


# Criando um DataFrame com as duas colunas
# x = pd.DataFrame({'resistance': resis, 'velocity_div_current': velocity_div_current, 'inv_current': inv_current, 'devCurrent_div_current': devCurrent_div_current})
x = pd.DataFrame({'resistance': resis, 'velocity_div_current': velocity_div_current, 'inv_current': inv_current})
# x = pd.DataFrame({'resistance': resis, 'velocity_div_current': velocity_div_current})

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
k2 = model.params["velocity_div_current"]
k3 = model.params["inv_current"]
k4 = 0 # model.params["devCurrent_div_current"]
k5 = model.params["const"]
print(f"t = {round(k1, 1)}*u/i {round(k2, 5)}*w/i {round(k3,4)}*1/i + {round(k4,6)}*di/i + {round(k5, -1)}")




def model_function(x, k1, k2, k3):
    u, i, w = x
    return ((u - k1*w) / i) * k2 + k3

x_data = [uqs, iqs, velocitys]
params, covariance = curve_fit(model_function, x_data.T, temps_measured)


temps_lstq = []


# temps_lstq = []
# for i in range(len(resis)):
#     temp_lstq = k1*resis[i] + k2*velocity_div_current[i] + k3*inv_current[i] + k4*(devCurrent_div_current[i]) + k5
#     temp_lstq = round(temp_lstq, 1)
#     temps_lstq.append(temp_lstq)


# temps_lstq_flt = LPF_FILTER(0.001, temps_lstq, temps_lstq[0])

plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
plt.plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with resistance model")
# plt.plot(times_fit, temps_lstq_flt, 'b.',label="Estimated Temperature with resistance model and filter")

plt.title("Filename = " + filename)
plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')
plt.legend()
plt.show()


## ******************************************* ##

filename = "rolling_data_Sin.txt"

times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)

derivada = np.gradient(iqs, times)
resis = []
velocity_div_current = []
devCurrent_div_current = []
inv_current = []
temps_fit = []
times_fit = []
vqs_temp = []
iqs_temp = []



for i in range(len(vqs)):
    if iqs[i] != 0 and abs(vqs[i]) > 0.96 and i > TIME1*8 and abs(velocitys[i]) < 1 and abs(iqs[i])>0.5:
        resis.append(vqs[i]/iqs[i]) # 0.5 
        velocity_div_current.append(velocitys[i]/iqs[i]) # 25
        inv_current.append(1/iqs[i])
        devCurrent_div_current.append(derivada[i]/iqs[i])
        temps_fit.append(temps_measured[i])
        times_fit.append(times[i])
        vqs_temp.append(vqs[i])
        iqs_temp.append(iqs[i])

vqs = vqs_temp.copy()
iqs = iqs_temp.copy()

# plt.plot(times_fit[:TIME1*10], iqs[:TIME1*10], 'r.',label="Iq")
# plt.plot(times_fit[:TIME1*10], vqs[:TIME1*10], 'b.',label="Vqs")
plt.plot(times_fit, velocity_div_current, 'b.',label="Iqs")
plt.legend()
plt.grid()
plt.show()

# vqs delay treated
vqs = [abs(vqs[i]) for i in range(len(vqs))]
iqs = [abs(iqs[i]) for i in range(len(iqs))]

# vqs = LPF_FILTER(0.0001, vqs, vqs[0])
# iqs = LPF_FILTER(0.0001, iqs, iqs[0])


resis = [vqs[i]/iqs[i] for i in range(len(vqs))]
# resis_flt = LPF_FILTER(0.0001, resis, resis[0])


temps_lstq = []
velos = []
resiss = []

for i in range(len(resis)):
    temp_lstq = k1*resis[i] + k2*velocity_div_current[i] + k3*inv_current[i] + k4*(devCurrent_div_current[i]) + k5
    temp_lstq = round(temp_lstq, 1)
    temps_lstq.append(temp_lstq)
    velos.append(k2*velocity_div_current[i])
    resiss.append(k1*resis[i])


plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
plt.plot(times_fit, temps_lstq, 'r.',label="Estimated Temperature with resistance model")

plt.title("Filename = " + filename)
plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')
plt.legend()
plt.show()