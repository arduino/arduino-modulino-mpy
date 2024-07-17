"""
This example shows how to use the ModulinoDistance class to read the distance from the Time of Flight sensor of the Modulino.
The sensor works by sending out short pulses of light and then measure the time it takes for some of the emitted light to come back
when it hits an object. The time it takes for the light to come back is directly proportional to the distance between the sensor and the object.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoDistance
from time import sleep_ms

distance = ModulinoDistance()

while True:
    print(f"📏 Distance: {distance.distance} cm")
    sleep_ms(50)