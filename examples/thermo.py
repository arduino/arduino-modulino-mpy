from modulino import ModulinoThermo
from time import sleep
from sys import exit

thermo_module = ModulinoThermo()

if not thermo_module:
    print("🤷 No thermo modulino found")    
    exit()

while True:
    print(f"🌡️ Temperature: {thermo_module.temperature:.1f} °C")
    print(f"💧 Humidity: {thermo_module.relative_humidity:.1f} %")    
    print()
    sleep(2)