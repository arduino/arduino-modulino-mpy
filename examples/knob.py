from modulino import ModulinoKnob
from time import sleep

knob = ModulinoKnob()
knob.value = 128 # (Optional) Set an initial value

knob.on_press = lambda: print("🔘 Pressed!")
knob.on_release = lambda: print("🔘 Released!")
knob.on_rotate_clockwise = lambda value: print(f"🎛️ Rotated clockwise! Value: {value}")
knob.on_rotate_counter_clockwise = lambda value: print(f"🎛️ Rotated counter clockwise! Value: {value}")

while True:
    if(knob.update()):
        print("👀 Knob changed!")

    sleep(0.1)