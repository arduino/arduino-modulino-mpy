"""
This example demonstrates how to control a stepper motor using the ModulinoMotors class. 
It shows how to switch between full-step and half-step modes, set different RPM targets, 
and manage the release of the motor after movement.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoMotors, DecayMode
from time import sleep_ms

motors = ModulinoMotors(steps_per_revolution=20)

print("Stepper Motor Example")
print("=====================\n")

# Switch to stepper mode
print("Switching to stepper mode...")
motors.stepper_mode_enabled = True

# Configure stepper parameters
print("Configuring stepper settings...")
motors.half_step_enabled = False  # Full step mode
motors.set_decay(DecayMode.FAST)
motors.stepper_direction_inverted = False  # Normal direction

print("Moving stepper with different RPM targets...\n")

def wait_until_idle():
  """Waits until the stepper motor is no longer busy (i.e., has completed its movement)."""
  while True:
    motors.update()  # Update internal state
    if not motors.busy:
      break
    sleep_ms(10)

def run_move(steps, rpm, release_delay_ms, description):
  """
  Moves the stepper motor the specified number of steps at the given RPM, with an optional release delay.
  """
  print(f"{description} | release_delay_ms={release_delay_ms}")
  motors.move_stepper_rpm(steps, rpm, release_delay_ms=release_delay_ms)
  wait_until_idle()
  sleep_ms(150)
  print(f"  Busy: {motors.busy}, Target release state: {motors.release_on_complete}\n")

# Define step sequences and target RPM
step_sequences = [
  (10, 60, 0, "Fast move: 10 steps at 60 RPM, hold at target"),
  (20, 30, 50, "Medium move: 20 steps at 30 RPM, release after 50ms"),
  (5, 10, 0, "Slow move: 5 steps at 10 RPM, keep holding torque"),
  (-10, 40, 50, "Reverse: 10 steps backward at 40 RPM, release after 50ms"),
]

# Run the defined step sequences
for steps, rpm, release_delay_ms, description in step_sequences:
  run_move(steps, rpm, release_delay_ms, description)

# Demonstrate step mode switching
print("Switching to half-step mode...")
motors.half_step_enabled = True
run_move(10, 30, 0, "Half-step move: 10 steps at 30 RPM, hold")
run_move(-10, 30, 50, "Half-step move: 10 steps reverse at 30 RPM, release after 50ms")

# Switch back to full step
print("Switching back to full-step mode...")
motors.half_step_enabled = False
run_move(10, 30, 0, "Full-step move: 10 steps at 30 RPM, hold")

print("Stepper example finished.")
motors.release()  # Ensure motor coils are de-energized at the end