from modulino import ModulinoBuzzer

buzzer = ModulinoBuzzer()

melody = [
    (ModulinoBuzzer.NOTES["E5"], 125),
    (ModulinoBuzzer.NOTES["E5"], 125),
    (ModulinoBuzzer.NOTES["REST"], 125),
    (ModulinoBuzzer.NOTES["E5"], 125),
    (ModulinoBuzzer.NOTES["REST"], 125),
    (ModulinoBuzzer.NOTES["C5"], 125),
    (ModulinoBuzzer.NOTES["E5"], 125),
    (ModulinoBuzzer.NOTES["REST"], 125),
    (ModulinoBuzzer.NOTES["G5"], 125),
    (ModulinoBuzzer.NOTES["REST"], 375),
    (ModulinoBuzzer.NOTES["G4"], 250)
]

# Super Mario Bros theme
for note, duration in melody:
    buzzer.tone(note, duration, blocking=True)