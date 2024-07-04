from modulino import ModulinoDistance
from machine import I2C, Pin
from time import sleep_ms

bus = I2C(0, sda=Pin(43), scl=Pin(44))
distance = ModulinoDistance(bus)
distance.begin()

while True:
    print(f"📏 Distance: {distance.distance} cm")
    print("")
    sleep_ms(500)