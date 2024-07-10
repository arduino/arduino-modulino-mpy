from modulino import Modulino
from machine import I2C, Pin

# The modulinos use a frequency of 100kHz by default.
bus = I2C(0, freq=100000)
# bus = I2C(0, scl=Pin(18), sda=Pin(19), freq=100000) # If you need to specify the pins

# In case the board was reset in the mean time some modulinos might
# be stuck in a pending operation. To get them unstuck we need to reset the bus.
bus = Modulino.reset_bus(bus)

# Do something with your modulino...
