from modulino import ModulinoButtons
from machine import SoftI2C, I2C, Pin
from time import sleep

bus = I2C(0, sda=Pin(43), scl=Pin(44))
buttons = ModulinoButtons(bus)
buttons.begin()

while True:
    buttons.update()
    
    if buttons.is_pressed(0) == True:
      buttons.set_leds(1, 0, 0)
    elif buttons.is_pressed(1) == True:
      buttons.set_leds(0, 1, 0)
    elif buttons.is_pressed(2) == True:
      buttons.set_leds(0, 0, 1)
    else:
      buttons.set_leds(0, 0, 0)