from pyftdi.spi import SpiController

# Configurar o primeiro dispositivo FTDI C232HM (IF/1)
ctrl1 = SpiController()
info1 = ctrl1.get_info()
print("Informações do dispositivo 1:", info1)
ctrl1.configure('ftdi://ftdi:232h/1')  # Configurar a primeira interface (IF/1) do primeiro dispositivo FTDI como um mestre SPI

# Configurar o segundo dispositivo FTDI C232HM (IF/1)
ctrl2 = SpiController()
info2 = ctrl2.get_info()
print("Informações do dispositivo 2:", info2)
ctrl2.configure('ftdi://ftdi:232h/1')  # Configurar a primeira interface (IF/1) do segundo dispositivo FTDI como um mestre SPI
