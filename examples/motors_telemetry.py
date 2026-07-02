"""
This example demonstrates how to monitor the telemetry of DC motors using the ModulinoMotors class.
It shows how to read the current sense values, switch between full-scale and half-full-scale modes,
and test direction inversion.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoMotors, DecayMode
from time import sleep_ms

SLEEP_TIME = 2000  # ms
motors = ModulinoMotors()

def print_current_readings(label_a="Current A", count=5):
  """
  Prints the current sense readings for motors A and B a specified number of times.
  """
  for _ in range(count):
    a, b = motors.sensed_current
    print(f"  {label_a}: {a:7.1f} mA | Current B: {b:7.1f} mA")
    sleep_ms(SLEEP_TIME)

# Configure motors in DC mode (default)
motors.stepper_mode_enabled = False

# Use full-scale ISEN conversion first, then compare with half-full-scale later
motors.half_full_scale_enabled = False

# Set decay mode (0-3)
motors.set_decay(DecayMode.FAST)

# Set PWM frequency (200-60000 Hz)
motors.frequency = 20000

# Run motors at different speeds and monitor current sense
print("Testing DC motor telemetry...")
for speed in [30, 50, 75, 100]:
  print(f"\nSetting speed to {speed}%")
  motors.speed_a = speed
  motors.speed_b = speed
  sleep_ms(200)  # Let the motors stabilize at the new speed
  print_current_readings()

print("\nSwitching to half-full-scale (HFS) mode for telemetry...")
motors.half_full_scale_enabled = True
print_current_readings("[HFS] Current A")

# Test direction inversion
print("\nTesting direction inversion...")
motors.speed_a = 80
motors.speed_b = 80
motors.invert_a = True  # Motor A reverses
print_current_readings("Current A (inverted)", count=3)

motors.stop()
print("\nMotors stopped.")