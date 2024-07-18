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
from time import sleep

buzzer = ModulinoBuzzer()

# Super Mario Bros theme intro
melody = [
    (ModulinoBuzzer.NOTES["E5"], 125),
    (ModulinoBuzzer.NOTES["REST"], 25),
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

# Wait 2 seconds before playing the next melody
sleep(2)

# Police siren sound effect
def generate_siren(frequency_start, frequency_end, total_duration, steps, iterations):
    siren = []
    mid_point = steps // 2
    duration_rise = total_duration // 2
    duration_fall = total_duration // 2

    for _ in range(iterations):
        for i in range(steps):
            if i < mid_point:
                # Easing in rising part
                step_duration = duration_rise // mid_point + (duration_rise // mid_point * (mid_point - i) // mid_point)
                frequency = int(frequency_start + (frequency_end - frequency_start) * (i / mid_point))
            else:
                # Easing in falling part
                step_duration = duration_fall // mid_point + (duration_fall // mid_point * (i - mid_point) // mid_point)
                frequency = int(frequency_end - (frequency_end - frequency_start) * ((i - mid_point) / mid_point))

            siren.append((frequency, step_duration))

    return siren

# 4 seconds up and down siren, with 200 steps and 2 iterations
siren_melody = generate_siren(440, 880, 4000, 200, 2)

for note, duration in siren_melody:
    buzzer.tone(note, duration, blocking=True)