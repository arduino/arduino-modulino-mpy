from modulino import ModulinoMotors
from time import sleep_ms

motors = ModulinoMotors()

# Configure motors in DC mode (default)
motors.stepper_mode_enabled = False

# Set decay mode (0-3)
motors.set_decay(0)

# Set PWM frequency (200-60000 Hz)
motors.frequency = 5000

# Run motors at different speeds and monitor current sense
print("Testing DC motor telemetry...")
for speed in [30, 50, 75, 100]:
  print(f"\nSetting speed to {speed}%")
  motors.speed_a = speed
  motors.speed_b = speed
  
  for i in range(5):
    sense_a, sense_b = motors.sense
    busy = motors.busy
    print(f"  Sense A: {sense_a:5d} | Sense B: {sense_b:5d} | Busy: {busy}")
    sleep_ms(200)

# Test direction inversion
print("\nTesting direction inversion...")
motors.speed_a = 80
motors.speed_b = 80
motors.invert_a = True  # Motor A reverses

for i in range(3):
  sense_a, sense_b = motors.sense
  print(f"  Sense A (inverted): {sense_a:5d} | Sense B: {sense_b:5d}")
  sleep_ms(200)

motors.stop()
print("\nMotors stopped.")