from modulino import ModulinoThermo
from time import sleep

thermo_module = ModulinoThermo()

while True:
    print(f"🌡️ Temperature: {thermo_module.temperature:.1f} °C")
    print(f"💧 Humidity: {thermo_module.relative_humidity:.1f} %")    
    print()
    sleep(2)