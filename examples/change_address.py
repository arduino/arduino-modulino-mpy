"""
This example shows how to change the I2C address of a Modulino device.
After changing the address, the device will be reset and the new address will be verified.
From then on, when creating a Modulino object, you should use the new address.
e.g. ModulinoBuzzer(address=0x2A)

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from sys import exit
from time import sleep
from modulino import Modulino

print()
bus = None # Change this to the I2C bus you are using on 3rd party host boards
devices = Modulino.available_devices(bus)

if len(devices) == 0:
    print("No devices found on the bus. Try resetting the board.")
    exit(1)

print("The following devices were found on the bus:")

for index, device in enumerate(devices):
    print(f"{index + 1}) {device.device_type} at {hex(device.address)}")

choice = int(input("\nEnter the device number for which you want to change the address: "))

if choice < 1 or choice > len(devices):
    print("Invalid choice. Please select a valid device number.")
    exit(1)

selected_device = devices[choice - 1]
new_address = int(input("Enter the new address (hexadecimal or decimal): "), 0)

if new_address < 0 or new_address > 127:
    print("Invalid address. Address must be between 0 and 127")
    exit(1)

print(f"Changing address of device at {hex(selected_device.address)} to {hex(new_address)}...")
selected_device.change_address(new_address)
sleep(1) # Give the device time to reset

# Check if the address was successfully changed
if selected_device.connected:
    print(f"✅ Address changed successfully to {hex(new_address)}")
else:
    print("❌ Failed to change address. Please try again.")