from pyftdi.gpio import GpioAsyncController
from MAX31855 import SPIuDriver_Temp
from pyftdi.spi import SpiController

import time

# Instantiate a SPI controller
spi = SpiController()

# Configure the first interface (IF/1) of the first FTDI device as a
# SPI master
spi.configure('ftdi://ftdi:232h/1')

# Get a SPI port to a SPI slave w/ /CS on A*BUS3 and SPI mode 0 @ 12MHz
slave = spi.get_port(cs=0, freq=12E6, mode=0)

# Get GPIO port to manage extra pins, use A*BUS4 as GPO, A*BUS4 as GPI
gpio = spi.get_gpio()
gpio.set_direction(0x30, 0x10)

# Assert GPO pin
gpio.write(0x10)
# Write to SPI slace
slave.write(b'hello world!')
# Release GPO pin
gpio.write(0x00)
# Test GPI pin
pin = bool(gpio.read() & 0x80)
print(pin)

from array import array as Array
from pyftdi.ftdi import Ftdi
acbus_direction = 0x01 # Bit C0 is output for reset
ctrl._ftdi.write_data(Array('B', [Ftdi.SET_BITS_HIGH, 0x00, acbus_direction]))
time.sleep(1.0)
ctrl._ftdi.write_data(Array('B', [Ftdi.SET_BITS_HIGH, 0x01, acbus_direction]))
time.sleep(1.0)