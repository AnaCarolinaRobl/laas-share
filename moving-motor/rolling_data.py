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
time_current = time.time()
time_temperature = time.time()
count = 0
count_courrent = 0
temp_5s = 100

temp_coef_flt = 0.001
temp_measured_flt = st.read()

while temp_measured_flt < 60:  #now - init_time < 180
    
    now = time.time()
    if now - init_time > 1:

        time_measured = now - init_time
        ref = 1 # np.sin(w*time_measured)*2*np.pi #valor a enviar para a velocidade
        derivate_ref        = w*np.cos(w*time_measured)
        capture_velocity    = ud.velocity1
        capture_position    = ud.position1

        error = ref-capture_position
        int_error += error*dt

        # offset = (5+2) / 2
        # amplitude = (5-2) / 2
        # I = np.sin(w*time_measured) * ( np.sin(w/10*time_measured)*amplitude + offset)

        if now-time_temperature > 20:
            if abs(temp_5s-temp_measured_flt)<=0.1:
                break
            time_temperature = time.time()
            temp_5s = temp_measured_flt

        #get data
        temp_measured = st.read()
        temp_measured_flt = temp_measured_flt + temp_coef_flt*(temp_measured - temp_measured_flt)

        if(temp_measured<46 and count == 0):
            if now-time_current > 0.2:
                time_current = time.time()
                I = 4*((-1)**(count_courrent))
                count_courrent += 1
                ud.refCurrent1 = I  # Iq
        else:
            count = 1
            if now-time_current > 0.3:
                time_current = time.time()
                I = 2*((-1)**(count_courrent))
                count_courrent += 1
                ud.refCurrent1 = I  # Iq

        # set current format 
        ud.refCurrent1 = I # Iq
        print("Temperature:",round(temp_measured, 1), "Time: ", round(now - init_time), "temp_5s: ", temp_5s )
        ud.transfer() # transfer
        # get data
        iq = ud.current1
        id = ud.current0
        vd = ud.adcSamples1
        vq = ud.resistance1

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
f = open("rolling_data_stable_temp.txt", "w")
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