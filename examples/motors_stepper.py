from modulino import ModulinoMotors
from time import sleep_ms

motors = ModulinoMotors(steps_per_revolution=200)

print("Stepper Motor Example")
print("=====================\n")

# Switch to stepper mode
print("Switching to stepper mode...")
motors.stepper_mode_enabled = True

# Configure stepper parameters
print("Configuring stepper settings...")
motors.half_step_enabled = False  # Full step mode
motors.set_decay(ModulinoMotors.DecayMode.FAST)

print("Moving stepper with different RPM targets...\n")

# Define step sequences and target RPM
step_sequences = [
  (100, 60, "Fast move: 100 steps at 60 RPM"),
  (200, 30, "Medium move: 200 steps at 30 RPM"),
  (50, 10, "Slow move: 50 steps at 10 RPM"),
  (-100, 40, "Reverse: 100 steps backward at 40 RPM"),
]

for steps, rpm, description in step_sequences:
  print(description)
  motors.move_stepper_rpm(steps, rpm)
  
  # Wait for move to complete (rough estimate)
  effective_steps_per_rev = motors.steps_per_revolution * (2 if motors.half_step_enabled else 1)
  move_time = int((abs(steps) * 60000) / (rpm * effective_steps_per_rev)) + 100
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
motors.move_stepper_rpm(100, 30)
sleep_ms(600)
print("Half-step move complete.\n")

# Switch back to full step
print("Switching back to full-step mode...")
motors.half_step_enabled = False
motors.move_stepper_rpm(100, 30)
sleep_ms(600)
print("Full-step move complete.\n")

print("Stepper example finished.")
