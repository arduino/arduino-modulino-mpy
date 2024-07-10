from modulino import ModulinoKnob
from time import sleep

knob = ModulinoKnob()
knob.value = 128 # (Optional) Set an initial value
previous_knob_value = None

while True:
    new_knob_value = knob.value
    if new_knob_value != previous_knob_value:
        previous_knob_value = new_knob_value
        print(f"🎛️ Value: {new_knob_value}")
    
    #print(f"🔘 Pressed: {knob.pressed}")
    sleep(0.1)