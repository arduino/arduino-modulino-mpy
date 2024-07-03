from modulino import ModulinoKnob
from machine import SoftI2C, I2C, Pin
from time import sleep

knob = ModulinoKnob()
knob.begin()

while True:
    print(f"🎛️ Value: {knob.get()}")
    sleep(0.1)