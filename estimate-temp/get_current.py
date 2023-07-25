#!/usr/bin/python3
from param import offsets #Edit offset.py according to your testbench
from delta_utils import *
import time
from odri_spi_ftdi import SPIuDriver

import matplotlib.pyplot as plt
import numpy as np


I_MEASURE_RESISTANCE = 0 # I used to measure resistence, he should be in id for now



dt = 0.001
ud = SPIuDriver(absolutePositionMode=False, waitForInit=True)
# ud.goto(0,0)
# ud.goto(0,0)
ud.transfer()
N=30000 #30 seconds
t = time.perf_counter()
i=0
p0 = np.array([0,0.1])
R = 0.02
courante = []
commande= [] 


# Initialize the plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
line, = ax.plot(courante, commande)

# Set plot properties
ax.set_xlabel('Commande')
ax.set_ylabel('Courante')
ax.set_title('Real-time Data')

# Inicializa listas vazias para os valores
valores_x = []
valores_y = []


Ilim=6 # A
I= I_MEASURE_RESISTANCE


id_measured = 0
temperature = 0
get_data = False
count = 0
comm = 0

tinit = time.time()

res_vec = [0,0,0,0,0,0]
res_ind = 0
res_mean = 0

while (I<=Ilim):
  
  ud.refVelocity1 = I # Id
  
  if ud.is_ready1 == 1:
    count += 1
    get_data = True

    if count == 10:
      I += 0.02 # Scrolls through all currents at 0.1 step 
      count = 0
  
  if res_ind == 6:
    res_ind = 0

  res = round(ud.resistance1, 4)
  res_vec[res_ind] = res
  res_mean = round(sum(res_vec)/6, 4)

  res_ind += 1


  if get_data and count > 1 and abs(id_measured - I) < 0.1:
    courante.append(round(id_measured, 3))
    commande.append(round(comm, 4))
    vbus = ud.velocity0
    print("resistencia: ", res_mean, "id sended, measured: ", round(I, 3), ", ", 
          round(id_measured, 3), "Ud:", round(temperature,4), "vbus: ", vbus)
  
  ud.transfer() #transfer
  
  id_measured  = ud.velocity1
  temperature   = ud.current1

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
