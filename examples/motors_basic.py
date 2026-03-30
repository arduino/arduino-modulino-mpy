from modulino import ModulinoMotors
from time import sleep_ms

motors = ModulinoMotors()
motors.stepper_mode_enabled = False  # DC mode

for i in range(0, 101):
  print(f"Setting speed to {i}")
  motors.speed_a = i
  motors.speed_b = i
  sleep_ms(100)

for i in range(100, -1, -1):
  print(f"Setting speed to {i}")
  motors.speed_a = i
  motors.speed_b = i
  sleep_ms(100)