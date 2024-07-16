"""
This example shows how to use the ModulinoBuzzer class to play a melody using the buzzer of the Modulino.

You can print the available notes with `print(ModulinoBuzzer.NOTES)`
Use the blocking parameter to add a delay between the notes which effectively makes
the tones play for the specified duration.
If you set blocking to False, following tones will overwrite the previous ones unless you
manually add a delay between them.
You can always use no_tone() to stop the current tone no matter the duration set.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoBuzzer

buzzer = ModulinoBuzzer()

# Super Mario Bros theme intro
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

for note, duration in melody:
    buzzer.tone(note, duration, blocking=True)