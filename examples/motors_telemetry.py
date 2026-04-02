from modulino import ModulinoMotors, DecayMode
from time import sleep_ms

SLEEP_TIME = 2000  # ms
motors = ModulinoMotors()

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
  for i in range(5):
    sensed_current_a, sensed_current_b = motors.sensed_current
    print(
      f"  Current A: {sensed_current_a:7.1f} mA | "
      f"Current B: {sensed_current_b:7.1f} mA"
    )
    sleep_ms(SLEEP_TIME)

print("\nSwitching to half-full-scale (HFS) mode for telemetry...")
motors.half_full_scale_enabled = True
for i in range(5):
  sensed_current_a, sensed_current_b = motors.sensed_current
  print(
    f"  [HFS] Current A: {sensed_current_a:7.1f} mA | "
    f"Current B: {sensed_current_b:7.1f} mA"
  )
  sleep_ms(SLEEP_TIME)

# Test direction inversion
print("\nTesting direction inversion...")
motors.speed_a = 80
motors.speed_b = 80
motors.invert_a = True  # Motor A reverses

for i in range(3):
  sensed_current_a = motors.sensed_current_a
  sensed_current_b = motors.sensed_current_b
  print(
    f"  Current A (inverted): {sensed_current_a:7.1f} mA | "
    f"Current B: {sensed_current_b:7.1f} mA"
  )
  sleep_ms(SLEEP_TIME)

motors.stop()
print("\nMotors stopped.")