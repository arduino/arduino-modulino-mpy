from modulino import ModulinoMovement
from machine import I2C, Pin
from time import sleep_ms

bus = I2C(0, sda=Pin(43), scl=Pin(44))
movement = ModulinoMovement(bus)

while True:
    print("🏃 Accelerometer: x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}".format(*movement.accelerometer))
    print("🌐 Gyroscope:     x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}".format(*movement.gyro))
    print("")
    sleep_ms(100)