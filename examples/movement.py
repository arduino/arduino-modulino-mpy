from modulino import ModulinoMovement
from time import sleep_ms

movement = ModulinoMovement()

while True:
    print("🏃 Accelerometer: x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}".format(*movement.accelerometer))
    print("🌐 Gyroscope:     x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}".format(*movement.gyro))
    print("")
    sleep_ms(100)