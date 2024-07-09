from modulino import ModulinoKnob
from time import sleep

knob = ModulinoKnob()
knob.begin()
previous_knob_value = None

while True:
    new_knob_value = knob.get()
    if new_knob_value != previous_knob_value:
        previous_knob_value = new_knob_value
        print(f"🎛️ Value: {new_knob_value}")
    
    print(f"🔘 Pressed: {knob.pressed}")
    sleep(0.1)