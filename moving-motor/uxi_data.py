#!/usr/bin/python3
import time
from odri_spi_ftdi import SPIuDriver
from MAX31855 import SPIuDriver_Temp
import matplotlib.pyplot as plt
import numpy as np
import time


dt = 0.001
ud = SPIuDriver(absolutePositionMode=False, waitForInit=True)
st = SPIuDriver_Temp()
# ud.goto(0,0)
# ud.goto(0,0)
ud.transfer()
N=30000 #30 seconds
t = time.perf_counter()
i=0
p0 = np.array([0,0.1])
R = 0.02
w = 10 # rad/s


ids, iqs = [],[]
vds, vqs = [], []
times = []
temps_measured = []
temps_lstq = []
velocitys = []
speeds = []
positions = []

id_measured = 0
ud_defined = 0
comm = 0
init_time = 0
add_i = .5

start_time = False
warming = True

I=0
count=0
kd= 0 # 10**(-4)*2
kp=2/9
ki = 0
alpha=0
int_error = 0
error=0
now = 0
iq = 0
vq = 0
temp_measured = 0
init_time = time.time()
time_current = 0
count = 0
di = 0.01

while I <= 5:
    
    now = time.time()
    if now - init_time > 5:
        if (I == 5):
            break
        time_measured = now - init_time
        I += di
        ud.refCurrent1 = I # Iq
        print("I=",round(I,2), "Iq=",round(iq,2),"Temperature:",round(temp_measured, 1), "Time: ", round(now - init_time), "Error: ", ud.error )
        ud.transfer() # transfer
        # get data
        temp_measured = st.read()
        iq = ud.current1
        id = ud.current0
        vd = ud.adcSamples1
        vq = ud.resistance1
        capture_velocity    = ud.velocity1
        capture_position    = ud.position1

        # store data on the lists
        times.append(round(time_measured, 4))
        temps_measured.append(round(temp_measured, 1))
        ids.append(round(id, 3))
        iqs.append(round(iq, 3))
        vds.append(round(vd, 4))
        vqs.append(round(vq, 4))
        velocitys.append(round(capture_velocity, 3))
        positions.append(round(capture_position, 2))

    else:
        # set current format
        ud.current0 = I # Id
        ud.transfer() # transfer
        
    #wait for next control cycle
    t +=dt
    while(time.perf_counter()-t<dt):
        pass

ud.stop() # Terminate


# Save data in file
f = open("uxi_data.txt", "w")
f.write("Time, Id, Iq, Ud, Uq, Velocity, Temperature, Position\n")

for i in range(len(times)):
    f.write(str(times[i]) + ", " 
            + str(ids[i]) + ", " 
            + str(iqs[i]) + ", "
            + str(vds[i]) + ", " 
            + str(vqs[i]) + ", " 
            + str(velocitys[i]) + ", " 
            + str(temps_measured[i]) + ", " 
            + str(positions[i])
            + "\n")
f.close()

# gravar
# tempo, id, ud, temperatura medida