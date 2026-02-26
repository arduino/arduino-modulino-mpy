"""
This script measures how long it takes for a modulino with MCU in
bootloader mode to become available again after a reset.
Probing the I2C bus for the device address causes the bootloader to reset the MCU.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from machine import I2C
from time import ticks_ms, ticks_diff

def device_available(bus, address: int) -> bool:
    try:
        bus.writeto(address, b'')
        return True
    except OSError:
        return False

def run_test():
    bus = I2C(0) # Adjust the I2C bus number as needed
    address = 100 # Bootloader address

    if not device_available(bus, address):
        print(f"Device at address {address} is not available.")
        return
    
    print(f"Device at address {address} is available. Device is resetting...")
    timestamp = ticks_ms()

    while not device_available(bus, address):
        pass

    elapsed_time = ticks_diff(ticks_ms(), timestamp)
    print(f"Device at address {address} became available again after {elapsed_time} ms.")    

if __name__ == "__main__":
    run_test()
    # Results are in the ballpark of 6236 ms.
