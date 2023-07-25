#!/usr/bin/python3
from param import offsets #Edit offset.py according to your testbench
from delta_utils import *
import time
from odri_spi_ftdi import SPIuDriver

import matplotlib.pyplot as plt
import numpy as np


I_MEASURE_RESISTANCE = 3 # I used to measure resistence, he should be in id for now


dt = 0.005
ud = SPIuDriver(absolutePositionMode=False, waitForInit=True)
ud.transfer()
N=30000 #30 seconds
t = time.perf_counter()
i=0
p0 = np.array([0,0.1])
R = 0.02
courante = []
commande= [] 

# Inicializa listas vazias para os valores
valores_x = []
valores_y = []


Ilim=7 # A
I= I_MEASURE_RESISTANCE


id_measured = 0
vd_defined = 0
get_data = False
count = 0
comm = 0
tinit = time.time()
res_vec = [0,0,0,0,0,0]
res_ind = 0
res_mean = 0

time_init = 0

while True:

  if ud.is_ready1 == 1 and time_init == 0 and  id_measured > 3:
    time_init = time.time()
    print("Comecou !")

  if (time.time() - time_init) > 100 and time_init != 0: 
    break

  ud.refVelocity1 = I # Id
  
  # if get_data and count > 1 and I > 0.02 and abs(id_measured - I) < 0.01:
  courante.append(round(id_measured, 3))
  commande.append(round(comm, 4))
  velo = ud.adcSamples1

  if res_ind == 6:
    res_ind = 0

  res = round(ud.resistance1, 4)
  res_vec[res_ind] = res
  res_mean = round(sum(res_vec)/6, 4)

  res_ind += 1

  print("id sended, measured: ", round(I, 3), ", ", 
          round(id_measured, 3))
  

  ud.transfer() #transfer
  
  id_measured  = ud.velocity1
  vd_defined   = ud.current1
  v_bus        = ud.velocity0
  timer = ud.resistance0
  comm = vd_defined / v_bus
  print("Time:", timer)

  #wait for next control cycle
  t +=dt
  while(time.perf_counter()-t<dt):
    pass
    time.sleep(0.0001)

ud.stop() # Terminate


# Save data in file

f = open("Commande_Courante.txt", "w")

f.write("commande, current \n")
for i in range(len(commande)):
  f.write(str(commande[i]) + ", " + str(courante[i]) + "\n")
f.close()
