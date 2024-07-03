from modulino import ModulinoThermo
from machine import SoftI2C, I2C, Pin
from time import sleep

#bus = SoftI2C(sda = Pin(43), scl = Pin(44))
bus = I2C(0, sda=Pin(43), scl=Pin(44))
thermo = ModulinoThermo(bus)

while True:
    print(f"🌡️ Temperature: {thermo.temperature:.1f} °C")
    print(f"💧 Humidity: {thermo.relative_humidity:.1f} %")    
    print()
    sleep(2)