"""
Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

import time
from modulino import ModulinoPressure

pressure_modulino = ModulinoPressure()

while True:
    print("Pressure: %.2f hPa" % pressure_modulino.pressure)
    print("Temperature: %.2f C" % pressure_modulino.temperature)
    print("Altitude: %.2f m" % pressure_modulino.altitude)
    time.sleep(1)