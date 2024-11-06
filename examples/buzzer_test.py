from modulino import ModulinoBuzzer
from time import sleep

buzzer = ModulinoBuzzer()

buzzer.tone(ModulinoBuzzer.NOTES["E5"], 0, blocking=True)
sleep(2)
buzzer.no_tone()
