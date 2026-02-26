"""
This script is a firmware updater for the Modulino devices. 

It uses the I2C bootloader to flash the firmware to the device. 
The script finds all .bin files in the root directory and prompts the user to select a file to flash. 
It then scans the I2C bus for devices and prompts the user to select a device to flash.
You must either know the I2C address of the device to be flashed or make sure that only one device is connected. 
The script sends a reset command to the device, erases the memory, and writes the firmware to the device in chunks. 
Finally, it starts the new firmware on the device.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

import os
import sys
import time
from micropython import const
from machine import I2C
from modulino import Modulino, DeviceManager

BOOTLOADER_I2C_ADDRESS = const(0x64)
ACK = const(0x79)
NACK = const(0x1F)
BUSY = const(0x76)

CMD_GET = const(0x00) # Gets the version and the allowed commands
CMD_GET_LENGTH_V12 = const(20) # Length of the response data
CMD_GET_VERSION = const(0x01) # Gets the protocol version
CMD_GET_ID = const(0x02) # Get chip ID
CMD_ERASE_NO_STRETCH = const(0x45) # Erase memory. Returns busy state while operation is ongoing
CMD_GO = const(0x21) # Jumps to user application code located in the internal flash memory
CMD_WRITE_NO_STRETCH = const(0x32) # Writes up to 256 bytes to the memory, starting from an address specified

CHUNK_SIZE = const(128) # Size of the memory chunk to write

bus = None # Change this to the I2C bus you are using on 3rd party host boards

def wait_for_ack(bus):
    """
    Wait for an acknowledgment from the I2C device.

    :return: True if an acknowledgment was received, otherwise False.
    """
    res = bus.readfrom(BOOTLOADER_I2C_ADDRESS, 1)[0]
    while res == BUSY:
        time.sleep(0.1)
        res = bus.readfrom(BOOTLOADER_I2C_ADDRESS, 1)[0]
    if res == ACK:
        return True
    elif res == NACK:
        print("❌ Command not acknowledged (NACK)")
        return False
    
    print(f"❌ Error processing command. Result code: {hex(res)}")
    return False

def execute_command(bus, opcode, command_params, response_length = 0, verbose=False):
    """
    Execute an I2C command on the device.

    :param bus: The I2C bus to use.
    :param opcode: The command opcode.
    :param command_params: The buffer containing the command parameters.
    :param response_length: The expected length of the response data frame.
    :param verbose: Whether to print debug information.
    :return: The number of response bytes read, or None if an error occurred.
    """
    if verbose:
        print(f"🕵️ Executing command {hex(opcode)}")

    cmd = bytes([opcode, 0xFF ^ opcode]) # Send command code and complement (XOR = 0x00)
    bus.writeto(BOOTLOADER_I2C_ADDRESS, cmd, True)
    if not wait_for_ack(bus):
        raise RuntimeError(f"❌ Command not acknowledged: {hex(opcode)}")

    if command_params is not None:
        bus.writeto(BOOTLOADER_I2C_ADDRESS, command_params, True)
        if not wait_for_ack(bus):
            raise RuntimeError("❌ Command failed")

    if response_length == 0:
        return None

    data = bus.readfrom(BOOTLOADER_I2C_ADDRESS, response_length)

    if not wait_for_ack(bus):
        raise RuntimeError("❌ Failed completing command")

    return data

def erase_memory(device : Modulino, verbose=False):
    """
    Erase the memory of the I2C device.

    :param device: The Modulino device to erase.
    :param verbose: Whether to print debug information.
    """
    bus = device.i2c_bus
    print("🗑️ Erasing memory...")
    erase_params = bytearray([0xFF, 0xFF, 0x0]) # Mass erase flash
    execute_command(bus, CMD_ERASE_NO_STRETCH, erase_params, 0, verbose)

def flash_firmware(device : Modulino, firmware_path, verbose=False):
    """
    Flash the firmware to the I2C device.

    :param device: The Modulino device to flash.
    :param firmware_path: The binary firmware path.
    :param verbose: Whether to print debug information.
    :return: True if the flashing was successful, otherwise False.
    """
    bus = device.i2c_bus
    erase_memory(device, verbose)

    with open(firmware_path, 'rb') as file:
        firmware_data = file.read()
    total_bytes = len(firmware_data)

    print(f"🔥 Writing {total_bytes} bytes")
    bytes_written = 0
    chunk_starts = range(0, total_bytes, CHUNK_SIZE)
    
    # Write chunks in reverse order so that the first chunk (containing the header) is written last.
    # This prevents the bootloader from jumping to a partially written application if the update fails.
    for i in reversed(chunk_starts):
        display_progress_bar(bytes_written, total_bytes)
        addr = 0x08000000 + i
        start_address = bytearray([
            (addr >> 24) & 0xFF,
            (addr >> 16) & 0xFF,
            (addr >> 8) & 0xFF,
            addr & 0xFF
        ])
        checksum = 0
        for b in start_address:
            checksum ^= b        
        start_address.append(checksum)
        data_slice = firmware_data[i:i + CHUNK_SIZE]
        if not write_firmware_page(bus, start_address, data_slice):
            print(f"❌ Failed to write page {hex(i)}")
            return False
        time.sleep(0.01) # Give the device some time to process the data
        bytes_written += len(data_slice)

    display_progress_bar(total_bytes, total_bytes)  # Complete the progress bar

    print("🏃 Launching new firmware")
    go_params = bytearray([0x8, 0x00, 0x00, 0x00, 0x8])
    execute_command(bus, CMD_GO, go_params, 0, verbose) # Jump to the application

    return True

def write_firmware_page(bus, command_params, firmware_data):
    """
    Write a page of the firmware to the I2C device.

    :param bus: The I2C bus to use.
    :param command_params: The buffer containing the command parameters.
    :param firmware_data: The buffer containing the firmware data.
    :return: True if the page was written successfully, otherwise False.
    """
    cmd = bytes([CMD_WRITE_NO_STRETCH, 0xFF ^ CMD_WRITE_NO_STRETCH])
    bus.writeto(BOOTLOADER_I2C_ADDRESS, cmd)
    if not wait_for_ack(bus):
        print("❌ Write command not acknowledged")
        return False
    
    bus.writeto(BOOTLOADER_I2C_ADDRESS, command_params)
    if not wait_for_ack(bus):
        print("❌ Failed to write command parameters")
        return False
    
    data_size = len(firmware_data)
    tmp_buffer = bytearray(data_size + 2) # Data plus size and checksum
    tmp_buffer[0] = data_size - 1 # Size of the data
    tmp_buffer[1:data_size + 1] = firmware_data
    tmp_buffer[-1] = 0 # Checksum placeholder
    for i in range(data_size + 1): # Calculate checksum over size byte + data bytes
        tmp_buffer[-1] ^= tmp_buffer[i]
    
    bus.writeto(BOOTLOADER_I2C_ADDRESS, tmp_buffer)    
    if not wait_for_ack(bus):
        print("❌ Failed to write firmware")
        return False
    
    return True

def display_progress_bar(current, total, bar_length=40):
    """
    Print a progress bar to the terminal.

    :param current: The current progress value.
    :param total: The total progress value.
    :param bar_length: The length of the progress bar in characters.
    """
    percent = float(current) / total
    arrow = '=' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f"\rProgress: [{arrow}{spaces}] {int(round(percent * 100))}%")
    if current == total:
        sys.stdout.write('\n')

def find_bin_files():
    """
    Find all .bin files in the root directory.

    :return: A list of .bin file names.
    """
    return [file for file in os.listdir('/') if file.endswith('.bin')]

def select_file(bin_files):
    """
    Prompt the user to select a .bin file to flash.

    :param bin_files: A list of .bin file names.
    :return: The selected .bin file name.
    """
    if len(bin_files) == 0:
        print("❌ No .bin files found in the root directory.")
        return None

    if len(bin_files) == 1:
        confirm = input(f"📄 Found one binary file: {bin_files[0]}. Do you want to flash it? (yes/no) ")
        if confirm.lower() == 'yes':
            return bin_files[0]
        else:
            return None
    
    print("📄 Found binary files:")
    for index, file in enumerate(bin_files):
        print(f"{index + 1}. {file}")
    choice = int(input("Select the file to flash (number): "))
    if choice < 1 or choice > len(bin_files):
        return None
    return bin_files[choice - 1]

def select_device(devices: list) -> Modulino:
    """
    Prompt the user to select a device from the list.

    :param devices: A list of available devices.
    :return: The selected Modulino device.
    """

    if len(devices) == 0:
        print("❌ No devices found")
        return None

    if len(devices) == 1:
        device = devices[0]
        confirm = input(f"🔌 Found {device.name} at address {hex(device.address)}. Do you want to update this device? (yes/no) ")
        if confirm.lower() == 'yes':
            return devices[0]
        else:
            return None

    print("🔌 Devices found:")
    for index, device in enumerate(devices):
        print(f"{index + 1}) {device.name} at {hex(device.address)}")
    choice = int(input("Select the device to flash (number): "))
    if choice < 1 or choice > len(devices):
        return None
    return devices[choice - 1]

def print_device_info(device : Modulino):
    """
    Print information about the selected device.

    :param device: The Modulino device.
    """

    bus = device.i2c_bus
    data = execute_command(bus, CMD_GET_VERSION, None, 1)
    if data is None:
        print("❌ Failed to get protocol version")
        return False
    print(f"ℹ️ Protocol version: {data[0] & 0xF}.{data[0] >> 4}")

    data = execute_command(bus, CMD_GET, None, CMD_GET_LENGTH_V12)
    if data is None:
        print("❌ Failed to get command list")
        return False
    
    print(f"ℹ️ Bootloader version: {(data[1] & 0xF)}.{data[1] >> 4}")
    print("👀 Supported commands:")
    print(", ".join([hex(byte) for byte in data[2:]]))

    data = execute_command(bus, CMD_GET_ID, None, 3)
    if data is None:
        print("❌ Failed to get device ID")
        return False
    
    chip_id = (data[0] << 8) | data[1] # Chip ID: Byte 1 = MSB, Byte 2 = LSB
    print(f"ℹ️ Chip ID: {chip_id}")

def run(bus: I2C):
    """
    Initialize the flashing process.
    Finds .bin files, scans for I2C devices, and flashes the selected firmware.

    :param bus: The I2C bus to use. If None, the default I2C bus will be used.
    """

    bin_files = find_bin_files()
    if not bin_files:
        print("❌ No .bin files found in the root directory.")
        return

    bin_file = select_file(bin_files)
    if bin_file is None:
        print("❌ No file selected")
        return

    device_manager = DeviceManager(i2c_bus=bus)
    devices = device_manager.available_devices()
    device_scan_timestamp = time.ticks_ms() # Remeber when the scan was performed
    device = select_device(devices)

    if device is None:
        print("❌ No device selected")
        return
    
    if device.address != BOOTLOADER_I2C_ADDRESS:
        print(f"🔄 Resetting device at address {hex(device.address)}")
        if device.enter_bootloader():
            print("✅ Device reset successfully")
        else:
            print("❌ Failed to reset device")
            return
    else:
        # If the device is already in bootloader mode, give it some time to be ready to receive commands
        # As a result of scanning, devices in bootloader mode reset and need some time (~6.5 seconds) before they can receive commands.
        print("⏱️ Waiting for device to be ready...")
        remaining_time = 6500 - time.ticks_diff(time.ticks_ms(), device_scan_timestamp)
        if remaining_time > 0:
            time.sleep_ms(remaining_time)

    print(f"🕵️ Flashing {bin_file} to device at address {hex(BOOTLOADER_I2C_ADDRESS)}")
    
    print_device_info(device)

    if flash_firmware(device, bin_file):
        print("✅ Firmware flashed successfully")
    else:
        print("❌ Failed to flash firmware")

if __name__ == "__main__":
    print()    
    run(bus)
