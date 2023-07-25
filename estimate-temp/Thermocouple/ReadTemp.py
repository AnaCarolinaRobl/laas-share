from MAX31855 import SPIuDriver_Temp
from odri_spi_ftdi import SPIuDriver
import time

N=30000 #30 seconds

ud = SPIuDriver(absolutePositionMode=False, waitForInit=False)

ctrl = ud.getCtrl()
st = SPIuDriver_Temp(ctrl)


for i in range(N):

    print(f'temp:', st.read())
    time.sleep(0.1)