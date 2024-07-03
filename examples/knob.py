from modulino import ModulinoKnob
from machine import SoftI2C, I2C, Pin
from time import sleep

bus = I2C(0, sda=Pin(43), scl=Pin(44))
knob = ModulinoKnob(bus)
knob.begin()

while True:
    print(f"🎛️ Value: {knob.get()}")
    sleep(0.1)