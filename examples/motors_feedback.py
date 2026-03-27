from modulino import ModulinoMotors
from time import sleep_ms

motors = ModulinoMotors()

motors.speed_a = 100
motors.speed_b = 100

while True:
  print(f"Motor A: {motors.sense_a}, Motor B: {motors.sense_b}")
  sleep_ms(1000)