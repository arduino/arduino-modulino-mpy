"""
This example demonstrates how to use the Modulino Relay module 
to turn a relay on and off repeatedly.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoRelay
from time import sleep

relay = ModulinoRelay()
print(f"Relay is currently {'on' if relay.is_on else 'off'}")

while True:
    print("Turning relay on")
    relay.on()
    sleep(1)  # Keep the relay on for 1 second
    print("Turning relay off")
    relay.off()
    sleep(1)  # Keep the relay off for 1 second