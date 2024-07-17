"""
Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoKnob, ModulinoBuzzer

knob = ModulinoKnob()
buzzer = ModulinoBuzzer()

# Select notes between 400 and 2000 Hz
notes = sorted(list(filter(lambda note: note >= 400 and note <= 2000, ModulinoBuzzer.NOTES.values())))

knob.range = (0, len(notes) - 1)
knob.on_press = lambda : buzzer.no_tone()

def on_knob_rotate_clockwise(_):
    frequency = notes[knob.value]
    print(f"🎵 Frequency: {frequency} Hz")
    buzzer.tone(frequency)

def on_knob_rotate_counter_clockwise(_):
    frequency = notes[knob.value]
    print(f"🎵 Frequency: {frequency} Hz")
    buzzer.tone(frequency)

knob.on_rotate_clockwise = on_knob_rotate_clockwise
knob.on_rotate_counter_clockwise = on_knob_rotate_counter_clockwise

while True:
    knob.update()
        