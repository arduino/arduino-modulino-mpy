from modulino import ModulinoMotors
from time import sleep_ms

motors = ModulinoMotors()

print("Stepper Motor Example")
print("=====================\n")

# Switch to stepper mode
print("Switching to stepper mode...")
motors.stepper_mode_enabled = True

# Configure stepper parameters
print("Configuring stepper settings...")
motors.half_step_enabled = False  # Full step mode
motors.half_full_scale_enabled = False  # Full range
motors.set_decay(0)

print("Moving stepper with different periods...\n")

# Define step sequences and periods (microseconds between steps)
step_sequences = [
  (100, 5000, "Fast move: 100 steps, 5ms period"),
  (200, 10000, "Medium move: 200 steps, 10ms period"),
  (50, 20000, "Slow move: 50 steps, 20ms period"),
  (-100, 5000, "Reverse: 100 steps backward, 5ms period"),
]

for steps, period, description in step_sequences:
  print(description)
  motors.move_stepper(steps, period)
  
  # Wait for move to complete (rough estimate)
  move_time = (abs(steps) * period) // 1000 + 100
  sleep_ms(move_time)
  
  # Check status
  for _ in range(3):
    busy = motors.busy
    mode = "stepper" if motors.stepper_mode_enabled else "DC"
    print(f"  Status - Mode: {mode}, Busy: {busy}")
    sleep_ms(50)
  print()

# Demonstrate step mode switching
print("Switching to half-step mode...")
motors.half_step_enabled = True
motors.move_stepper(100, 5000)
sleep_ms(600)
print("Half-step move complete.\n")

# Switch back to full step
print("Switching back to full-step mode...")
motors.half_step_enabled = False
motors.move_stepper(100, 5000)
sleep_ms(600)
print("Full-step move complete.\n")

# Demonstrate half-full-scale mode
print("Enabling half-full-scale (HFS) mode...")
motors.half_full_scale_enabled = True
motors.move_stepper(50, 5000)
sleep_ms(300)
print("HFS move complete.\n")

print("Stepper example finished.")
