"""
This example demonstrates how to use the ModulinoKnob and ModulinoBuzzer classes to play different notes using a buzzer.

The knob is used to select the note to play. The knob is rotated clockwise to increase the frequency of the note and counter-clockwise to decrease it.
Once the knob is pressed, the buzzer stops playing the note.
Only the notes between 400 and 2000 Hz from the predefined list are played in this example.
You can run print(ModulinoBuzzer.NOTES) to see the full list of available notes.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoKnob, ModulinoBuzzer

knob = ModulinoKnob()
buzzer = ModulinoBuzzer()

# Select notes between 400 and 2000 Hz
notes = sorted(list(filter(lambda note: note >= 400 and note <= 2000, ModulinoBuzzer.NOTES.values())))

knob.range = (0, len(notes) - 1)
knob.on_press = lambda : buzzer.no_tone()

def on_knob_rotate_clockwise(value):
    frequency = notes[value]
    print(f"🎵 Frequency: {frequency} Hz")
    buzzer.tone(frequency)

def on_knob_rotate_counter_clockwise(value):
    frequency = notes[value]
    print(f"🎵 Frequency: {frequency} Hz")
    buzzer.tone(frequency)

knob.on_rotate_clockwise = on_knob_rotate_clockwise
knob.on_rotate_counter_clockwise = on_knob_rotate_counter_clockwise

while True:
    knob.update()
        