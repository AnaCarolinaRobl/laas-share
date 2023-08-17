import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.preprocessing import StandardScaler


# Normalizando os dados
scaler = StandardScaler()

# Nome do arquivo de texto
nome_arquivo = "rolling_data_Sin.txt"

# Listas para armazenar os valores
times = []
ids, iqs = [], []
vds, vqs = [], []
temps_measured = []
positions = []
velocitys = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:
        # Divide a linha em comando e corrente
        time, id, iq, vd, vq, velocity, temp_measured, position = linha.strip().split(",")
        
        # Converte os valores para float e adiciona às listas
        times.append(float(time))
        ids.append(float(id))
        iqs.append(float(iq))
        vds.append(float(vd))
        vqs.append(float(vq))
        velocitys.append(float(velocity))
        temps_measured.append(float(temp_measured))
        positions.append(float(position))

# Calcular a derivada dos dados
derivada = np.gradient(iqs, times)

# Filter data
TIME1 = int(len(times)/220)
# delay_tension = int(len(times)/(220*20))
# vqs = [vqs[i + delay_tension] for i in range(len(vqs) - delay_tension)]

not_filtered_vqs = vqs.copy()
not_filtered_iqs = iqs.copy()
not_filtered_velocity = velocitys.copy()

def LPF_FILTER(flt_coef, ys, initial_value):
    flt_ys = [initial_value]
    for i in range(1, len(ys)):
        flt_ys.append(((flt_ys[i-1]) + (flt_coef * ((ys[i]) - (flt_ys[i-1])))))
    return flt_ys


resis = []
velocity_div_current = []
devCurrent_div_current = []
inv_current = []
temps_fit = []
times_fit = []
vqs_temp = []
iqs_temp = []

for i in range(len(vqs)):
    if iqs[i] != 0 and abs(vqs[i]) > 0.96 and i > TIME1*8 and velocitys[i] < 10:
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

# vqs delay treated
vqs = [abs(vqs[i]) for i in range(len(vqs))]
iqs = [abs(iqs[i]) for i in range(len(iqs))]
velocity_div_current = [abs(velocity_div_current[i]) for i in range(len(velocity_div_current))]


vqs = LPF_FILTER(0.0001, vqs, 2.4)
iqs = LPF_FILTER(0.0001, iqs, 3.5)
# velocity_div_current = LPF_FILTER(0.001, velocity_div_current, 15)

plt.plot(times_fit, iqs, label ="Iqs")
plt.plot(times_fit, vqs, label ="Vqs")
# plt.plot(times_fit, velocity_div_current, label ="velocity_div_current")
plt.legend()
plt.grid()
plt.show()


# resis_flt = [vqs[i]/iqs[i] for i in range(len(vqs))]
resis_flt = [vqs[i]/iqs[i] for i in range(len(vqs))]
resis_flt = LPF_FILTER(0.0001, resis_flt, resis_flt[0])

# resis_flt=resis
plt.plot(times_fit, resis_flt, label="resis_flt")
plt.legend()
plt.show()

# Criando um DataFrame com as duas colunas
x = pd.DataFrame({'resistance': resis_flt, 'velocity_div_current': velocity_div_current, 'inv_current': inv_current, 'devCurrent_div_current': devCurrent_div_current})
# x = pd.DataFrame({'resistance': resis_flt, 'inv_current': inv_current, 'devCurrent_div_current': devCurrent_div_current})

# Adicionando uma constante para o termo de interceptação
x = sm.add_constant(x)

y = temps_fit

# Realizando a regressão
model = sm.OLS(y, x).fit()
resultados_regressao = []

# Salvando os resultados da regressão
resultados_regressao.append({
    'Arquivo': arquivo,
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
k4 = model.params["devCurrent_div_current"]
k5 = model.params["const"]
print(f"t = {round(k1, -1)}*u/i {round(k2, 5)}*w/i {round(k3,4)}*1/i + {round(k4,6)}*di/i + {round(k5, -1)}")
# print(f"t = {round(k1, -1)}*u/i {round(k3,4)}*1/i + {round(k4,6)}*di/i + {round(k5, -1)}")