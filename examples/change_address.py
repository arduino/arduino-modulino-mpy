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

def main():
    print()
    bus = None # Change this to the I2C bus you are using on 3rd party host boards
    devices = Modulino.available_devices(bus)

    if len(devices) == 0:
        print("No devices found on the bus. Try resetting the board.")
        return

    print("The following devices were found on the bus:")

    for index, device in enumerate(devices):
        dev_type = device.device_type if device.device_type is not None else "Unknown Device"
        print(f"{index + 1}) {dev_type} at {hex(device.address)}")

    choice_is_valid = False
    while not choice_is_valid:
        try:
            choice = int(input("\nEnter the device number for which you want to change the address: "))
        except ValueError:
            print("Invalid input. Please enter a valid device number.")
            continue
        
        if choice < 1 or choice > len(devices):
            print("Invalid choice. Please select a valid device number.")
        else:
            choice_is_valid = True

    selected_device = devices[choice - 1]


    new_address_is_valid = False
    while not new_address_is_valid:
        try:
            new_address = int(input("Enter the new address (hexadecimal or decimal): "), 0)
        except ValueError:
            print("Invalid input. Please enter a valid hexadecimal (e.g., 0x2A) or decimal (e.g., 42) address.")
            continue

        if new_address < 1 or new_address > 127:
            print("Invalid address. Address must be between 1 and 127")
        elif new_address == 100:
            print("The address 0x64 (100) is reserved for bootloader mode. Please choose a different address.")
        else:
            new_address_is_valid = True

    print(f"Changing address of device at {hex(selected_device.address)} to {hex(new_address)}...")
    selected_device.change_address(new_address)
    sleep(1) # Give the device time to reset

    # Check if the address was successfully changed
    if selected_device.connected:
        print(f"✅ Address changed successfully to {hex(new_address)}")
    else:
        print("❌ Failed to change address. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\Aborted by user")