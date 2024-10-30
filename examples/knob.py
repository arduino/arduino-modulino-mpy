"""
This example shows how to use the ModulinoKnob class to read the value of a rotary encoder knob.

The knob is used to increase or decrease a value. The knob is rotated clockwise to increase the value and counter-clockwise to decrease it.

You can register callbacks for the following events:
- Press: The knob is pressed.
- Release: The knob is released.
- Rotate clockwise: The knob is rotated clockwise.
- Rotate counter clockwise: The knob is rotated counter clockwise.

Use reset() to reset the knob value to 0.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoKnob
from time import sleep

knob = ModulinoKnob()
knob.value = 5 # (Optional) Set an initial value
knob.range = (-10, 10) # (Optional) Set a value range

def on_release():
    knob.reset()
    print("🔘 Released! Knob's value was reset.")

knob.on_press = lambda: print("🔘 Pressed!")
knob.on_release = on_release
knob.on_rotate_clockwise = lambda steps, value: print(f"🎛️ Rotated {steps} steps clockwise! Value: {value}")
knob.on_rotate_counter_clockwise = lambda steps, value: print(f"🎛️ Rotated {steps} steps counter clockwise! Value: {value}")

while True:
    if(knob.update()):
        print("👀 Knob value or state changed!")

    sleep(0.1)