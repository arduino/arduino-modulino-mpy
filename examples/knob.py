"""
Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoKnob
from time import sleep

knob = ModulinoKnob()
knob.value = 5 # (Optional) Set an initial value
knob.range = (-10, 10) # (Optional) Set a value range

knob.on_press = lambda: print("🔘 Pressed!")
knob.on_release = lambda: knob.reset()
knob.on_rotate_clockwise = lambda value: print(f"🎛️ Rotated clockwise! Value: {value}")
knob.on_rotate_counter_clockwise = lambda value: print(f"🎛️ Rotated counter clockwise! Value: {value}")

while True:
    if(knob.update()):
        print("👀 Knob value or state changed!")

    sleep(0.1)