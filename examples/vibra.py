"""
This example demonstrates how to use the ModulinoVibra class to control a vibration motor.
It cycles through different vibration patterns with varying power levels and durations.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoVibra, PowerLevel
from time import sleep

vibra = ModulinoVibra()

pattern = [
    (500, PowerLevel.GENTLE),
    (1000, PowerLevel.MODERATE),
    (1500, PowerLevel.MEDIUM),
    (2000, PowerLevel.INTENSE),
    (2500, PowerLevel.POWERFUL),
    (3000, PowerLevel.MAXIMUM)
]

for duration, power in pattern:
    vibra.on(duration, power, blocking=True)
    sleep(0.5)  # Pause between vibrations
