"""
This example shows how to use the ModulinoThermo class to read the temperature and humidity from the Modulino.

If those values are temporarily unavailable, they will be set to None.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoThermo
from time import sleep

thermo_module = ModulinoThermo()

while True:    
    temperature = thermo_module.temperature
    humidity = thermo_module.relative_humidity
    
    if temperature != None and humidity != None:
        print(f"🌡️ Temperature: {temperature:.1f} °C")
        print(f"💧 Humidity: {humidity:.1f} %")    
        print()
        
    sleep(2)