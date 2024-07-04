from modulino import ModulinoThermo
from machine import I2C, Pin
from time import sleep

bus = I2C(0, sda=Pin(43), scl=Pin(44))
thermo_module = ModulinoThermo(bus)

while True:
    print(f"🌡️ Temperature: {thermo_module.temperature:.1f} °C")
    print(f"💧 Humidity: {thermo_module.relative_humidity:.1f} %")    
    print()
    sleep(2)