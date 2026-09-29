"""
This example shows how to use the built-in pedometer of the Modulino Movement
to count steps. The step detection runs on the sensor itself, so the step count
keeps increasing in the background even while your code is busy doing other things.
Attach the Modulino to your shoe, or hold it in your hand while walking, to see it in action.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoMovement
from time import sleep_ms

movement = ModulinoMovement()

# Steps are only counted after 5 consecutive steps have been detected,
# which helps to filter out false positives e.g. from shaking the device.
# Omit this line to use the default of 10 steps.
movement.pedometer_debounce_steps = 5
movement.pedometer_enabled = True
movement.reset_step_count()

last_step_count = None

while True:
    step_count = movement.step_count

    if step_count != last_step_count:
        print(f"👣 Steps: {step_count}")
        last_step_count = step_count

    sleep_ms(100)
