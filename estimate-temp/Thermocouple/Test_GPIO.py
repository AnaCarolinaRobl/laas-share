from pyftdi.gpio import GpioAsyncController
from MAX31855 import SPIuDriver_Temp
from pyftdi.spi import SpiController

import time

GPIO0 = 0x10
GPIO1 = 0x20
GPIO2 = 0x40
GPIO3 = 0x80
ALL   = 0Xff

ud = SPIuDriver_Temp()


# Configura os pinos digitais
# gpio = GpioAsyncController()
# gpio.configure('ftdi://ftdi:232h/1')

# Congifuracao SPI
ctrl = SpiController(cs_count=2)
ctrl.configure('ftdi://ftdi:232h/1') # Configure the first interface (IF/2) of the FTDI device as a SPI master
spi = ctrl.get_port(1, mode=0, freq=5000000)
gpio = ctrl.get_gpio()

# spi.write(b"hello!")



spi1 = ctrl.get_port(0, mode=0, freq=5000000)
spi1.write(b"hello!")

# gpio.set_direction(GPIO0, GPIO0)

# gpio.write(GPIO0)
# time.sleep(0.5)

# gpio.write(0x00)
# time.sleep(2e-3)

# time.sleep(5e-10)
# gpio.write(GPIO0)




# gpio.close()