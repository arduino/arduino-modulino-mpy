from modulino import ModulinoBuzzer

buzzer = ModulinoBuzzer()

melody = [
    (ModulinoBuzzer.PITCHES["NOTE_E5"], 125),
    (ModulinoBuzzer.PITCHES["NOTE_E5"], 125),
    (ModulinoBuzzer.PITCHES["REST"], 125),
    (ModulinoBuzzer.PITCHES["NOTE_E5"], 125),
    (ModulinoBuzzer.PITCHES["REST"], 125),
    (ModulinoBuzzer.PITCHES["NOTE_C5"], 125),
    (ModulinoBuzzer.PITCHES["NOTE_E5"], 125),
    (ModulinoBuzzer.PITCHES["REST"], 125),
    (ModulinoBuzzer.PITCHES["NOTE_G5"], 125),
    (ModulinoBuzzer.PITCHES["REST"], 375),
    (ModulinoBuzzer.PITCHES["NOTE_G4"], 250)
]

# Super Mario Bros theme
for note, duration in melody:
    buzzer.tone(note, duration, blocking=True)