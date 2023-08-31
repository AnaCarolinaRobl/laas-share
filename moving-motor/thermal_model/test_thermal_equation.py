# Fazer grafico dos dois em um so
import sys
sys.path.append('../')  # Adiciona o diretório pai (pasta_principal) ao PATH
from utils import get_data,thermal_model
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


### Generate Constants Thermal Model ###

#ler arquivo .txt para pegar os dados
filename = "rolling_data_2p5A.txt"
filename_2 = "rolling_data_2A.txt"
filename_3 = "rolling_data_3A_new.txt"
# i = 3
times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename_3)
times_2, ids_2, iqs_2, vds_2, vqs_2, velocitys_2, temps_measured_2, positions_2 = get_data(filename_2)
times_3, ids_3, iqs_3, vds_3, vqs_3, velocitys_3, temps_measured_3, positions_3 = get_data(filename)

def func(x, a, b, c):
    return a * np.exp(-b * x) + c

times_subida = [time for i, time in enumerate(times) if ids[i] >= 0.2]
temps_measured_subida = [temp_measured for i,temp_measured in enumerate(temps_measured) if ids[i] >= 0.2]

times_filtred = [time for i, time in enumerate(times_subida) if i < len(temps_measured_subida) - 1 and temps_measured_subida[i] != temps_measured_subida[i+1]]
ids_filtred = [ids[i] for i, id in enumerate(times_subida) if i < len(temps_measured_subida) - 1 and temps_measured_subida[i] != temps_measured_subida[i+1]]
iqs_filtred = [iqs[i] for i, iq in enumerate(times_subida) if i < len(temps_measured_subida) - 1 and temps_measured_subida[i] != temps_measured_subida[i+1]]
temps_measured_filtred = [temp_measured for i,temp_measured in enumerate(temps_measured_subida) if i < len(temps_measured_subida) - 1 and temps_measured_subida[i] != temps_measured_subida[i+1]]


times_filtred = np.array(times_filtred) / 60 # was necessary change the scale of x for the fit works
param,_ = curve_fit(func, times_filtred, temps_measured_filtred) # modelo, eixo x, eixo y
a, b, c = param

# #Get constants
a, b, c = c, a, -b # a + b*exp(c*t) = a*exp(-b*t)+c
print(f"{a} {b}*exp({c}*t)")
c = c/60 # change the unit of measure from minutes to seconds

# K1 = (b*c)/(i**2)
# K2 = -c
# T_AMBIENT = temps_measured[0]
# print("K1,K2: ", K1,K2)

count = 0

# Constants to i = 3
# K1 = 0.0102767094249931
# K2 = 0.0018960075163828988
# T_AMBIENT = temps_measured[0]
# T_AMBIENT_3 = temps_measured_3[0]

# # Constants to i = 2
# K1 = 0.011020358590325312 
# K2 = 0.001476849805192163
# T_AMBIENT = temps_measured[0]
# T_AMBIENT_3 = temps_measured_3[0]

# Median 2 A and 3 A
# K1 = (0.0102767094249931 + 0.011020358590325312 ) / 2
# K2 = (0.0018960075163828988 + 0.001476849805192163) / 2
T_AMBIENT = temps_measured[0]
T_AMBIENT_3 = temps_measured_3[0]
T_AMBIENT_2 = temps_measured_2[0]


### Simulation ###
###### Caso va testar com os valores do txt desejado comente ate a linha que define iqs ###########

# Constantes
# T_AMBIENT = 27 # °C
# K1 = 0.0102
# K2 = 1/529
# # 22*60 s enviando 3A 
# # do 22*60 s ate o 49*60 s enviando 0 amperes
# times = [i for i in range(1, 49 * 60 + 1)] # s
# ids = [3 if 0 <= i <= 22 * 60 else 0 for i in times] # A
# iqs = [0 for i in times] # A

# Mostrar valores escolhidos de corrente e tempo
# print(ids, iqs)
# plt.plot(times_filtred, temps_measured_filtred)
# plt.plot(times, iqs)
# plt.show()

while count<=3:
    if(count==0):
        # Constants to i = 2
        K1 = 0.011020358590325312 
        K2 = 0.001476849805192163
        legenda = "Temperature Estimation Model 2 A"
    elif(count==1):
        # Constants to i = 2.5
        K1 = 0.010294078001999562  #0.0102767094249931
        K2 = 0.0011876190612097718 #0.0018960075163828988
        legenda = "Temperature Estimation Model 2.5 A"
    elif(count==2):
        i=3
        K1 = (b*c)/(i**2)
        K2 = -c
        T_AMBIENT = temps_measured[0]
        legenda = "Temperature Estimation Model 3 A" 
        print("K1,K2: ", K1,K2) 
    else:
        # Median 2 A and 3 A
        K1 = (0.0102767094249931 + 0.011020358590325312 ) / 2
        K2 = (0.0018960075163828988 + 0.001476849805192163) / 2
        legenda = "Temperature Estimation Model Average"   

    #### Test termique model ####
    times_filtred, ids_filtred, iqs_filtred, temps_measured_filtred = [], [], [], []
    for i in range(len(times) - 1):
        if(temps_measured[i] != temps_measured[i+1]):
            times_filtred.append(times[i])
            ids_filtred.append(ids[i])
            iqs_filtred.append(iqs[i])
            temps_measured_filtred.append(temps_measured[i])

    times_filtred = np.array(times_filtred)

    temps_model = thermal_model(times_filtred, iqs_filtred, ids_filtred, K1, K2, T_AMBIENT)


    times_filtred_2, ids_filtred_2, iqs_filtred_2, temps_measured_filtred_2 = [], [], [], []
    for i in range(len(times_2) - 1):
        if(temps_measured_2[i] != temps_measured_2[i+1]):
            times_filtred_2.append(times_2[i])
            ids_filtred_2.append(ids_2[i])
            iqs_filtred_2.append(iqs_2[i])
            temps_measured_filtred_2.append(temps_measured_2[i])

    times_filtred_2 = np.array(times_filtred_2)

    temps_model_2 = thermal_model(times_filtred_2, iqs_filtred_2, ids_filtred_2, K1, K2, T_AMBIENT_2)

    times_filtred_3, ids_filtred_3, iqs_filtred_3, temps_measured_filtred_3 = [], [], [], []
    for i in range(len(times_3) - 1):
        if(temps_measured_3[i] != temps_measured_3[i+1]):
            times_filtred_3.append(times_3[i])
            ids_filtred_3.append(ids_3[i])
            iqs_filtred_3.append(iqs_3[i])
            temps_measured_filtred_3.append(temps_measured_3[i])

    times_filtred_3 = np.array(times_filtred_3)

    temps_model_3 = thermal_model(times_filtred_3, iqs_filtred_3, ids_filtred_3, K1, K2, T_AMBIENT_3)


    # Criando a figura e os subplots
    fig, axs = plt.subplots(3, 1, figsize=(8, 6))

    # Plotando o primeiro gráfico na posição (0, 0) da grade (em cima)
    axs[0].plot(times_filtred/60, temps_model,label = legenda)
    axs[0].plot(times_filtred/60, temps_measured_filtred,label = "Temperature Measured")
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Temperature [° Celsius]')
    axs[0].set_title("Rise with a current of 3 A and decrease with 0 A")
    axs[0].legend()
    axs[0].grid()


  # Plotando o segundo gráfico na posição (1, 0) da grade (embaixo)
    axs[1].plot(times_filtred_2/60, temps_model_2,label = legenda)
    axs[1].plot(times_filtred_2/60, temps_measured_filtred_2,label = "Temperature Measured")
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel('Temperature [° Celsius]')
    axs[1].set_title("Rise with a current of 2 A and decrease with 0 A")
    axs[1].legend()
    axs[1].grid()

    # Plotando o segundo gráfico na posição (1, 0) da grade (embaixo)
    axs[2].plot(times_filtred_3/60, temps_model_3,label = legenda)
    axs[2].plot(times_filtred_3/60, temps_measured_filtred_3,label = "Temperature Measured")
    axs[2].set_xlabel('Time [s]')
    axs[2].set_ylabel('Temperature [° Celsius]')
    axs[2].set_title("Rise with a current of 2.5 A and decrease with 0 A")
    axs[2].legend()
    axs[2].grid()


    plt.subplots_adjust(hspace=1)  # Ajuste o valor conforme necessário
    plt.show()
    count+=1