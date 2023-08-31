# Depois se eu quiser continuar na parte da aquisicao dos dados  da temperatura com a pygame
import sys
sys.path.append('../')  # Adiciona o diretório pai (pasta_principal) ao PATH
from utils import get_data,thermal_model
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


### Generate Constants Thermal Model ###

#ler arquivo .txt para pegar os dados
filename = "rolling_data_2A.txt"
times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)

for i in range(len(times)):
    pass