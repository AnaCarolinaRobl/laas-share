import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Nome do arquivo de texto
nome_arquivo = "rolling_data.txt"

# Listas para armazenar os valores
times = []
ids, iqs = [], []
vds, vqs = [], []
temps_measured = []
temps_model_omodri = []
temps_lstq = []

# Leitura do arquivo de texto
with open(nome_arquivo, "r") as arquivo:
    # Ignora a primeira linha (cabeçalho)
    next(arquivo)
    
    # Lê as linhas restantes do arquivo
    for linha in arquivo:

        time, id, iq, vd, vq, temp_measured, temp_lstq, temp_model = linha.strip().split(",")
        
        times.append(float(time))
        ids.append(float(id))
        iqs.append(float(iq))
        vds.append(float(vd))
        vqs.append(float(vq))
        temps_measured.append(float(temp_measured))
        temps_model_omodri.append(float(temp_model))
        temps_lstq.append(float(temp_lstq))
        velocitys.append(floar(velocity))


resis = []
velocity_div_current = []
temps_fit = []
for i in range(len(ids)):
    if ids[i] != 0 and vds[i]/16 > 0.06:
        resis.append(round(vds[i]/ids[i], 3))
        velocity_div_current.append(round(velocitys[i]/ids[i], 4))
        temps_fit.append(round(temps_measured[i]))

# Criando um DataFrame com as duas colunas
x = pd.DataFrame({'Resistance': resis, 'velocity_div_current': velocity_div_current})

# Adicionando uma constante para o termo de interceptação
x = sm.add_constant(x)
y = temps_fit

# Realizando a regressão linear
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


k1 = model.params["Resistance"]
k2 = model.params["velocity_div_current"]
k3 = model.params["const"]
print(f"t = {round(k1)}*u/i {round(k2)}/i {round(k3,1)}")


# WEIGTHED LINEAR REGRESSION
#define weights to use
wt = 1 / smf.ols('fit.resid.abs() ~ fit.fittedvalues', data=df).fit().fittedvalues**2

#fit weighted least squares regression model
fit_wls = sm.WLS(y, X, weights=wt).fit()

#view summary of weighted least squares regression model
print(fit_wls.summary())