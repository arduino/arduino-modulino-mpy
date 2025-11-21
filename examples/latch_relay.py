"""
This example demonstrates how to use the Modulino Latch Relay module 
to turn a relay on and off repeatedly.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoLatchRelay
from time import sleep_ms

relay = ModulinoLatchRelay()
initial_state = relay.is_on

if initial_state is None:
    print("Relay state is unknown (last state before poweroff is maintained)")
else:
    print(f"Relay is currently {'on' if initial_state else 'off'}")

while True:    
    print("Turning relay on")
    relay.on()
    sleep_ms(150) # Wait for the relay to settle
    print(f"Relay is currently {'on' if relay.is_on else 'off'}")
    sleep_ms(1000)  # Keep the relay on for 1 second
    print("Turning relay off")
    relay.off()
    sleep_ms(150) # Wait for the relay to settle
    print(f"Relay is currently {'on' if relay.is_on else 'off'}")
    sleep_ms(1000)  # Keep the relay off for 1 second
