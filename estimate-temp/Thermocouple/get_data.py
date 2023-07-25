#!/usr/bin/python3
import time
from odri_spi_ftdi import SPIuDriver
from MAX31855 import SPIuDriver_Temp

import matplotlib.pyplot as plt
import numpy as np
import time
import keyboard as kb


dt = 0.005
ud = SPIuDriver(absolutePositionMode=False, waitForInit=True)

ctrl = ud.getCtrl()
st = SPIuDriver_Temp(ctrl)

ud.transfer()

N=30000 #30 seconds
t = time.perf_counter()
i=0
p0 = np.array([0,0.1])
R = 0.02


courantes = []
commandes = [] 
times = []
temperatures = []
temperatures_estimated = []


I= 3

id_measured = 0
ud_defined = 0
comm = 0
init_time = 0
add_i = .5

current_time = 0
K1, K2, K3 = 490, -125, -97.5


init_time = time.time()
temp = 27

while (temp < 70) or (mow - init_time < 300):

    # set current format
    ud.refVelocity1 = I # Id
    ud.transfer() # transfer
    temp = st.read()

    now = time.time()

    if now - current_time > 0.2: 
        I += add_i
        if I == 6:
            add_i = -0.5
        elif I == 3:
            add_i = 0.5
        current_time = now
        print("temp, time, current: ", round(temp,1), round(now), round(I, 2))


    if now - init_time > 1:

        # get data
        id_measured  = ud.velocity1
        ud_defined   = ud.adcSamples1
        time_measured = now - init_time
        if id_measured != 0:
            estimated_temperature = K1 * (ud_defined / id_measured) + K2 * (1 / id_measured) + K3
            estimated_temperature = round(estimated_temperature, 1)
        else:
            estimated_temperature = 0

        # store data on the lists
        times.append(round(time_measured, 4))
        temperatures.append(temp)
        courantes.append(round(id_measured, 3))
        commandes.append(round(ud_defined, 4))
        temperatures_estimated.append(round(estimated_temperature, 1))

        # print( "id measured", round(id_measured, 3), 
        #     "temperatura medida: ", temp, "temperatura estimada: ", estimated_temperature)

    #wait for next control cycle
    t +=dt
    while(time.perf_counter()-t<dt):
        pass

ud.stop() # Terminate


# Save data in file
f = open("data.txt", "w")
f.write("Time, Id, Ud, Temperature Measured, Temperature Estimated\n")

for i in range(len(times)):
    print(commandes[i])
    f.write(str(times[i]) + ", " + str(courantes[i]) + ", " + 
        str(commandes[i]) + ", " + str(temperatures[i]) + ", " + str(temperatures_estimated[i]) +"\n")
f.close()

# gravar
# tempo, id, ud, temperatura medida