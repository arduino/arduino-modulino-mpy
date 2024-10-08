"""
This example shows how to use the Modulino library with a third party board.
When running on a non-Arduino board, the I2C bus must be initialized manually.
Usually the available I2C buses are predefined and can be accessed by their number, e.g. I2C(0).
If not, the pins for SDA and SCL must be specified.

Please note that the Modulinos are designed to work with a bus frequency of 100kHz.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import Modulino
from modulino import ModulinoPixels
from machine import I2C, Pin

# The modulinos use a frequency of 100kHz by default.
bus = I2C(0, freq=100000)
# bus = I2C(0, scl=Pin(18), sda=Pin(19), freq=100000) # If you need to specify the pins

# In case the board was reset during a previous operation the modulinos might
# end up with a stuck bus. To get them unstuck we need to reset the bus.
bus = Modulino.reset_bus(bus)

# Do something with your modulino...
# For example controlling the pixels:
pixels = ModulinoPixels(bus)
pixels.set_all_rgb(0, 255, 0, 100)
pixels.show()
