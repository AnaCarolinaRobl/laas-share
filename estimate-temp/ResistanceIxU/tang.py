import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def filtrar_valores_arquivo(nome_arquivo):
    valores_filtrados = []
    with open(nome_arquivo, 'r') as arquivo:
        # linhas = arquivo.readlines()
        # Ignora a primeira linha (cabeçalho)
        next(arquivo)
        for linha in arquivo:
            comando, corrente = linha.strip().split(',')
            comando = float(comando)
            if 0.06 <= comando <= 0.1:
                valores_filtrados.append((float(comando), float(corrente)))
    return valores_filtrados

def funcao_ajuste(comando, parametro1, parametro2):
    # Defina sua função de ajuste aqui
    return parametro1 * comando + parametro2

arquivos = ['26.txt', '33.txt', '39.txt', '44.txt', '50.txt','57.txt','63.txt','69.txt','75.txt']
valores_finais = []
resistencias = []
temp = []

VBUS = 16

for arquivo in arquivos:
    valores_arquivo = filtrar_valores_arquivo(arquivo)
    valores_finais.extend(valores_arquivo)
    comandos = [comando*VBUS for comando, _ in valores_arquivo]
    correntes = [corrente for _, corrente in valores_arquivo]
    correntes = np.array(correntes)
    
    # Parâmetros iniciais para o ajuste
    p0 = [1, 1]
    
    # Realiza o ajuste de curva
    parametros, _ = curve_fit(funcao_ajuste, comandos, correntes, p0=p0)
    resistencias.append((float(1/parametros[0])))
    temp.append(float(arquivo.split('.')[0]))



    # print(f"Ajuste para o arquivo {arquivo}:")
    # print("Parâmetros ajustados:", parametros)
    # print()


    # # Plota o gráfico
    # plt.figure()
    
    # # Gera pontos para a curva ajustada
    # comandos_ajuste = np.linspace(0.06, 0.1, 100)
    # correntes_ajuste = funcao_ajuste(comandos_ajuste, *parametros)
    # plt.plot(comandos_ajuste, correntes_ajuste, 'r', label='Ajuste')
    
    # plt.title(f"Ajuste para o arquivo {arquivo}")
    # plt.xlabel('Tempo')
    # plt.ylabel('Comando')
    # plt.legend()
    # plt.show()


####### Sem Curve.fit #######

# plt.plot(temp, resistencias, 'b.', label= '75 degrés')
# plt.legend()
# plt.xlabel('Commande')
# plt.ylabel('Courante')
# plt.title('Commande x Courante')
# plt.grid(True)
# plt.show()


####### Com Curve.fit #######
parametros, _ = curve_fit(funcao_ajuste, resistencias, temp, p0=p0)
print(resistencias)
plt.figure()

# Gera pontos para a curva ajustada
resistencias_ajuste = np.linspace(resistencias[0], resistencias[-1], 100)
temp_ajuste = funcao_ajuste(resistencias_ajuste, *parametros)
plt.plot(resistencias_ajuste, temp_ajuste,'r', label = f'y={int(parametros[0])}x {int(parametros[1])}')
plt.plot(resistencias, temp,'b.', label = 'Data')
plt.title("Resistance x Temperature ")
plt.ylabel('Temperature [°Celsius]')
plt.xlabel('Resistance [Ohms]')
plt.legend()
plt.show()
