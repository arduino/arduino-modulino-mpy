from modulino import ModulinoBuzzer
from machine import SoftI2C, I2C, Pin
from time import sleep

bus = I2C(0, sda=Pin(43), scl=Pin(44))
buzzer = ModulinoBuzzer(bus)
buzzer.begin()

# Super Mario Bros theme
buzzer.tone(659, 125)
sleep(0.2)
buzzer.tone(659, 125)
sleep(0.2)
buzzer.tone(659, 125)
sleep(0.2)
buzzer.tone(523, 125)
sleep(0.2)
buzzer.tone(659, 125)
sleep(0.2)
buzzer.tone(784, 125)
sleep(0.2)
buzzer.tone(392, 125)
sleep(0.2)
buzzer.no_tone()