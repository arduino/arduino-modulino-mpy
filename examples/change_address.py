from sys import exit
from machine import I2C
from time import sleep

pinstrap_map = {
    0x3C: "BUZZER",
    0x7C: "BUTTONS",
    0x76: "ENCODER",
    0x74: "ENCODER",
    0x6C: "SMARTLEDS"
}

def pinstrap_to_name(address):
    if address in pinstrap_map:
        return pinstrap_map[address]
    return "UNKNOWN"

bus = I2C(0)
devices_on_bus = bus.scan()

print()

if len(devices_on_bus) == 0:
    print("No devices found on the bus. Try resetting the board.")
    exit(1)

print("The following devices were found on the bus:")

for index, device_address in enumerate(devices_on_bus):
    pinstrap_address = bus.readfrom(device_address, 1)
    device_name = pinstrap_to_name(pinstrap_address[0])
    print(f"{index + 1}) {device_name} at {hex(device_address)}")

choice = int(input("\nEnter the device number for which you want to change the address: "))
if choice < 1 or choice > len(devices_on_bus):
    print("Invalid choice. Please select a valid device number.")
    exit(1)

selected_device_address = devices_on_bus[choice - 1]

# Read address from user input
new_address = int(input("Enter the new address (hexadecimal or decimal): "), 0)

if new_address < 0 or new_address > 127:
    print("Invalid address. Address must be between 0 and 127")
    exit(1)

print(f"Changing address of device at {hex(selected_device_address)} to {hex(new_address)}...")

data = bytearray(40)
# Set the first two bytes to 'C' and 'F' followed by the new address
data[0:2] = b'CF'
data[2] = new_address * 2

try:
  bus.writeto(selected_device_address, data)
except OSError:
  pass # Device resets immediately and causes ENODEV to be thrown which is expected
sleep(1)

# Check if the address was successfully changed
devices_on_bus = bus.scan()
if new_address in devices_on_bus:
    print(f"✅ Address changed successfully to {hex(new_address)}")
else:
    print("❌ Failed to change address. Please try again.")