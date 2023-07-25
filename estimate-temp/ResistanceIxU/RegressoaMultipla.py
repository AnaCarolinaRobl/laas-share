import pandas as pd
import statsmodels.api as sm

# Lista dos nomes dos arquivos
arquivos = ['26.txt', '33.txt', '39.txt', '44.txt', '50.txt', '57.txt', '63.txt', '69.txt', '75.txt']

# Lista para armazenar os resultados das regressões
resultados_regressao = []
resis=[]
inv_current=[]
t=[]
VBUS = 16


# Executando a regressão para cada arquivo
for arquivo in arquivos:
    temp = float(arquivo.split('.')[0])
    # Lendo o arquivo de dados
    with open(arquivo, "r") as arquivo:
        # Ignora a primeira linha (cabeçalho)
        next(arquivo)
        # Lê as linhas restantes do arquivo
        for linha in arquivo:
            # Divide a linha em comando e corrente
            u, i = linha.strip().split(",")
            u = float(u)
            i = float(i)
            if(float(u)>=0.06):
                # Converte os valores para float e adiciona às listas
                u = VBUS*u
                
                resis.append(round(u/i, 3))
                inv_current.append(round(1/i,3))
                t.append(temp)


# Criando um DataFrame com as duas colunas
x = pd.DataFrame({'Resistance': resis, 'inv_current': inv_current})
# Adicionando uma constante para o termo de interceptação
x = sm.add_constant(x)

y = t

# Realizando a regressão
model = sm.OLS(y, x).fit()

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
k2 = model.params["inv_current"]
k3 = model.params["const"]

print(f"t = {round(k1)}*u/i {round(k2)}/i {round(k3,1)}")