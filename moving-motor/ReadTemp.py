from MAX31855 import SPIuDriver_Temp
import time

N=30000 #30 seconds
st = SPIuDriver_Temp()


for i in range(N):

    print(f'temp:', st.read())
    time.sleep(0.1)