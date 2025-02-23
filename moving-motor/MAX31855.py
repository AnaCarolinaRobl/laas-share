# Original code: https://github.com/adafruit/Adafruit_CircuitPython_MAX31855/tree/main

# This code is an adaptation of the original code (link above) to receive data from the MAX31855PMB1 thermocouple using the FTDI C232HM.
# Ana Carolina Coelho Robl - jul.2023

import struct
from pyftdi.spi import SpiController
import math
import time

from IPython import embed

class SPIuDriver_Temp:
  def __init__(self):

    #Initialise SPI
    self.ctrl = SpiController()
    self.ctrl.configure('ftdi://ftdi:232h:01:6/1')
    self.spi = self.ctrl.get_port(0, mode=0, freq=5000000)


  def read(self):
    sensorPacket =  bytearray(self.spi.read(4))
    # embed()
    #decode received sensor packet

    temp, refer = struct.unpack(">hh", sensorPacket)
    refer >>= 4
    temp >>= 2

    # temperature of remote thermocouple junction
    TR = temp/4
    # temperature of device (cold junction)
    TAMB = refer*0.0625
    # thermocouple voltage based on MAX31855's uV/degC for type K (table 1)
    VOUT = 0.041276 * (TR - TAMB)
    # cold junction equivalent thermocouple voltage

    if TAMB >= 0:
      VREF = (
          -0.176004136860e-01
          + 0.389212049750e-01 * TAMB
          + 0.185587700320e-04 * math.pow(TAMB, 2)
          + -0.994575928740e-07 * math.pow(TAMB, 3)
          + 0.318409457190e-09 * math.pow(TAMB, 4)
          + -0.560728448890e-12 * math.pow(TAMB, 5)
          + 0.560750590590e-15 * math.pow(TAMB, 6)
          + -0.320207200030e-18 * math.pow(TAMB, 7)
          + 0.971511471520e-22 * math.pow(TAMB, 8)
          + -0.121047212750e-25 * math.pow(TAMB, 9)
          + 0.1185976
          * math.exp(-0.1183432e-03 * math.pow(TAMB - 0.1269686e03, 2))
      )
    else:
      VREF = (
          0.394501280250e-01 * TAMB
          + 0.236223735980e-04 * math.pow(TAMB, 2)
          + -0.328589067840e-06 * math.pow(TAMB, 3)
          + -0.499048287770e-08 * math.pow(TAMB, 4)
          + -0.675090591730e-10 * math.pow(TAMB, 5)
          + -0.574103274280e-12 * math.pow(TAMB, 6)
          + -0.310888728940e-14 * math.pow(TAMB, 7)
          + -0.104516093650e-16 * math.pow(TAMB, 8)
          + -0.198892668780e-19 * math.pow(TAMB, 9)
          + -0.163226974860e-22 * math.pow(TAMB, 10)
      )
    # total thermoelectric voltage
    VTOTAL = VOUT + VREF
    # determine coefficients
    # https://srdata.nist.gov/its90/type_k/kcoefficients_inverse.html
    if -5.891 <= VTOTAL <= 0:
      DCOEF = (
          0.0000000e00,
          2.5173462e01,
          -1.1662878e00,
          -1.0833638e00,
          -8.9773540e-01,
          -3.7342377e-01,
          -8.6632643e-02,
          -1.0450598e-02,
          -5.1920577e-04,
      )
    elif 0 < VTOTAL <= 20.644:
      DCOEF = (
          0.000000e00,
          2.508355e01,
          7.860106e-02,
          -2.503131e-01,
          8.315270e-02,
          -1.228034e-02,
          9.804036e-04,
          -4.413030e-05,
          1.057734e-06,
          -1.052755e-08,
      )
    elif 20.644 < VTOTAL <= 54.886:
      DCOEF = (
          -1.318058e02,
          4.830222e01,
          -1.646031e00,
          5.464731e-02,
          -9.650715e-04,
          8.802193e-06,
          -3.110810e-08,
      )
    else:
      raise RuntimeError(f"Total thermoelectric voltage out of range:{VTOTAL}")
    # compute temperature
    TEMPERATURE = 0
    for n, c in enumerate(DCOEF):
      TEMPERATURE += c * math.pow(VTOTAL, n)
    return round(TEMPERATURE,1)










   