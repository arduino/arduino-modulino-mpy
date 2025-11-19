"""
This example shows how to use the ModulinoMovement class to read the accelerometer 
and gyroscope values from the Modulino.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoMovement
from time import sleep_ms

movement = ModulinoMovement()

while True:
    acc = movement.acceleration
    gyro = movement.angular_velocity
    
    print(f"🏃 Acceleration: x:{acc.x:>8.3f} y:{acc.y:>8.3f} z:{acc.z:>8.3f}")
    print(f"💪 Acceleration Magnitude: {movement.acceleration_magnitude:>8.3f} g")
    print(f"🌐 Angular Velocity: x:{gyro.x:>8.3f} y:{gyro.y:>8.3f} z:{gyro.z:>8.3f}")
    print("")
    sleep_ms(100)
