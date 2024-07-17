"""
Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoKnob, ModulinoBuzzer

class ConstrainedIndex:
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.value = min

    def increment(self):
        self.value = min(self.value + 1, self.max)
        return self.value

    def decrement(self):
        self.value = max(self.value - 1, self.min)
        return self.value

knob = ModulinoKnob()
buzzer = ModulinoBuzzer()

# Select notes between 400 and 2000 Hz
notes = sorted(list(filter(lambda note: note >= 400 and note <= 2000, ModulinoBuzzer.NOTES.values())))

note_index = ConstrainedIndex(0, len(notes) - 1)
knob.on_press = lambda : buzzer.no_tone()

def on_knob_rotate_clockwise(_):
    note_index.increment()
    frequency = notes[note_index.value]
    print(f"🎵 Frequency: {frequency} Hz")
    buzzer.tone(frequency)

def on_knob_rotate_counter_clockwise(_):
    note_index.decrement()
    frequency = notes[note_index.value]
    print(f"🎵 New frequency: {frequency} Hz")
    buzzer.tone(frequency)

knob.on_rotate_clockwise = on_knob_rotate_clockwise
knob.on_rotate_counter_clockwise = on_knob_rotate_counter_clockwise

while True:
    knob.update()
        