#!/usr/bin/python3
from param import offsets #Edit offset.py according to your testbench
from delta_utils import *
import time
from odri_spi_ftdi import SPIuDriver

import matplotlib.pyplot as plt
import numpy as np
import time
import keyboard as kb


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


ids, iqs = []
vds, vqs = []
times = []
temps_measured = []
temps_model = []
temps_lstq = []


I= 3

id_measured = 0
ud_defined = 0
comm = 0
init_time = 0
add_i = .5

K1, K2, K3 = 490, -125, -97.5

start_time = False

TempAmbiente = float(input('Digite a temperatura ambiente: '))
# temperatures.append(TempAmbiente)
temp = TempAmbiente

init_time = time.time()
while True:

    # set current format
    ud.refVelocity1 = I # Id
    ud.transfer() # transfer

    if time.time() - init_time > 1:
        I += add_i
        if warming:
            if I == 6:
                add_i = -0.5
            elif I == 3:
                add_i = 0.5
        else:
            if I == 3:
                add_i = -0.5
            elif I == 0:
                add_i = 0.5

        # get data
        id  = ud.velocity1
        temperature_model = ud.current1
        vq = ud.coilRes1
        vd  = ud.adcSamples1
        iq  = ud.current0

        time_measured = time.time() - init_time


        # define temperature by least squares model
        current = id + iq
        voltage = vd + vq
        if current != 0:
            temp_lstq = K1 * (voltage / current) + K2 * (1 / current) + K3
            temp_lstq = round(temp_lstq, 1)
        else:
            temp_lstq = 0
        

        # store data on the lists
        times.append(round(time_measured, 4))
        temps_measured.append(round(temp_measured, 1))
        ids.append(round(id, 3))
        iqs.append(round(id, 3))
        vds.append(round(vd, 4))
        vqs.append(round(vd, 4))
        temps_lstq.append(round(temp_lstq, 1))

        print( "id measured", round(id, 3), 
            "temperatura medida: ", round(temp_measured, 1), "temperatura estimada: ", temp_lstq)


        # update temperature
        key = str(input('Subiu(ENTER), Desceu (d), Sortie (s), Up Current (x)'))  
        if key == '':
            temp_measured = temp_measured+0.1
        elif key == 'd':  
            temp_measured = temp_measured-0.1
        elif key == 'x':  
            I += 1
        
        # change between warming or cooling
        if key == 'i':  
            warming = not warming
            I = 0 if warming else 3
        
        # finish test
        if key == 's':
            break 

    #wait for next control cycle
    t +=dt
    while(time.perf_counter()-t<dt):
        pass

ud.stop() # Terminate


# Save data in file
f = open("data.txt", "w")
f.write("Time, Id, , Iq, Ud, Uq, Temperature Measured, Temperature_LSTQ, Temperature_Model\n")

for i in range(len(times)):
    f.write(str(times[i]) + ", " 
            + str(ids[i]) + ", " 
            + str(iqs[i]) + ", "
            + str(vds[i]) + ", " 
            + str(vqs[i]) + ", " 
            + str(temps_measured[i]) + ", " 
            + str(temps_lstq[i]) + ", "
            + str(temps_model[i])
            +"\n")
f.close()

# gravar
# tempo, id, ud, temperatura medida