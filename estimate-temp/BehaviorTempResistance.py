#!/usr/bin/python3
from param import offsets #Edit offset.py according to your testbench
from delta_utils import *
import time
from odri_spi_ftdi import SPIuDriver

import math
import matplotlib.pyplot as plt
import numpy as np
import time
import keyboard as kb

I_MEASURE_RESISTANCE = 0 # I used to measure resistence, he should be in id for now

dt = 0.005
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
timer =[]
temps = []
res_ind=0
res_vec=[0,0,0,0,0,0]


Ilim=6 # A
I= I_MEASURE_RESISTANCE


id_measured = 0
vd_defined = 0
get_data = False
count = 0
comm = 0
init_time = 0


TempAmbiente = float(input('Digite a temperatura ambiente: '))
temps.append(round(TempAmbiente, 1))
temp = TempAmbiente

W = .2

senos = []
t = 0
ts = []
resistances = []

while True:
  
  # Seno de entrada
  t += 1
  I = math.sin(t * W)*2 + 5
  senos.append(I)
  ts.append(t)

  ud.refVelocity1 = I # Id

  courante.append(round(id_measured, 3))
  commande.append(round(comm, 4))
  velo = ud.adcSamples1

  print( "id sended, measured: ", round(I, 3), ", ", 
      round(id_measured, 3))
  

  ud.transfer() #transfer
  
  id_measured  = ud.velocity1
  vd_defined   = ud.current1
  v_bus        = ud.velocity0
  
  if res_ind == 6:
    res_ind = 0

  res = round(ud.resistance1, 4)
  res_vec[res_ind] = res
  res_mean = round(sum(res_vec)/6, 4)

  res_ind += 1



  comm = vd_defined / v_bus

  if(id_measured >= (I-0.1)):
    
    resistances.append(res_mean)

    key = str(input('Subiu(ENTER), Desceu (d) et sortie (s)'))  
    # if kb.is_pressed('d'):
    if key == '':
      temp = temp+0.1
      temps.append(round(temp, 1))

    # if kb.is_pressed('a'):
    if key == 'd':  
      temp = temp-0.1
      temps.append(round(temp, 1))
    if key == 's':
      break 


  #wait for next control cycle
  t +=dt
  while(time.perf_counter()-t<dt):
    pass
    time.sleep(0.0001)


ud.stop() # Terminate


# Save data in file

f = open("ResitanceXTemperature.txt", "w")

f.write("Resistance, Temperature \n")
for i in range(len(resistances)):
  f.write(str(resistances[i]) + ", " + str(temps[i]) + "\n")
f.close()
