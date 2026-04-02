from modulino import ModulinoMotors, DecayMode
from time import sleep_ms

motors = ModulinoMotors()
motors.stepper_mode_enabled = False  # DC mode
# Set decay mode to slow for more gradual current changes
motors.set_decay(DecayMode.SLOW)

for i in range(0, 101):
  print(f"Setting speed to {i}")
  motors.speed_a = i
  motors.speed_b = i
  sleep_ms(100)

sleep_ms(1000)

for i in range(100, -1, -1):
  print(f"Setting speed to {i}")
  motors.speed_a = i
  motors.speed_b = i
  sleep_ms(100)