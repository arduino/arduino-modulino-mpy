from modulino import Modulino
from machine import I2C

bus = I2C(0, freq=100000)

# In case the board was reset in the mean time some modulinos might
# be stuck in a pending operation. To get them unstuck we need to reset the bus.
bus = Modulino.reset_bus(bus)

# Do something with your modulino...
