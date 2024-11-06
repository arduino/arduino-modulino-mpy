import os
import sys
from machine import I2C, Pin
import time
from micropython import const

BOOTLOADER_I2C_ADDRESS = const(0x64)

# Define I2C pins and initialize I2C
i2c = I2C(0, freq=100000)

def send_reset(address):
    """
    Send a reset command to the I2C device at the given address.

    :param address: I2C address of the device.
    :return: 0 if the reset command was sent successfully, otherwise -1.
    """
    buffer = b'DIE'
    # Pad buffer to 40 bytes
    buffer += b'\x00' * (40 - len(buffer))

    try:
        print(f"Sending reset command to address {hex(address)}")
        i2c.writeto(address, buffer, True)
    except OSError as e:
        pass

    time.sleep(0.25)
    devices = i2c.scan()

    if address in devices:
        return False
    elif BOOTLOADER_I2C_ADDRESS in devices:
        return True

def execute_command(opcode, command_buffer, command_length, response_buffer, response_length, verbose=True):
    """
    Execute an I2C command on the device.

    :param opcode: The command opcode.
    :param command_buffer: The buffer containing the command data.
    :param command_length: The length of the command data.
    :param response_buffer: The buffer to store the response data.
    :param response_length: The expected length of the response data.
    :param verbose: Whether to print debug information.
    :return: The number of response bytes read, or -1 if an error occurred.
    """
    if verbose:
        print("Executing command")

    cmd = bytes([opcode, 0xFF ^ opcode])
    i2c.writeto(100, cmd)
    if command_length > 0:
        i2c.writeto(100, command_buffer)
    
    time.sleep(0.1)
    ack = i2c.readfrom(100, 1)[0]
    if ack != 0x79:
        print(f"Error first ack: {hex(ack)}")
        return -1
    
    if command_length > 0:
        ack = i2c.readfrom(100, 1)[0]
        if ack != 0x79:
            while ack == 0x76:
                time.sleep(0.1)
                ack = i2c.readfrom(100, 1)[0]
            if ack != 0x79:
                print(f"Error second ack: {hex(ack)}")
                return -1
    
    if response_length > 0:
        data = i2c.readfrom(100, response_length + 1)
        for i in range(response_length):
            response_buffer[i] = data[i + 1]
        
        ack = i2c.readfrom(100, 1)[0]
        if ack != 0x79:
            print(f"Error: {hex(ack)}")
            return -1
    
    return response_length

def flash_firmware(firmware, length, verbose=True):
    """
    Flash the firmware to the I2C device.

    :param firmware: The binary firmware data.
    :param length: The length of the firmware data.
    :param verbose: Whether to print debug information.
    :return: True if the flashing was successful, otherwise False.
    """
    if verbose:
        print("Flashing firmware")
    
    response_buffer = bytearray(255)
    if execute_command(0, None, 0, response_buffer, 20, verbose) < 0:
        print("Failed :(")
        return False
    for byte in response_buffer:
        print(hex(byte))

    if verbose:
        print("Getting device ID")
    if execute_command(2, None, 0, response_buffer, 3, verbose) < 0:
        print("Failed to get device ID")
        return False
    for byte in response_buffer:
        print(hex(byte))

    if verbose:
        print("Mass erase")
    erase_buffer = bytearray([0xFF, 0xFF, 0x0])
    if execute_command(0x44, erase_buffer, 3, None, 0, verbose) < 0:
        print("Failed to mass erase")
        return False

    for i in range(0, length, 128):
        progress_bar(i, length)
        write_buffer = bytearray([8, 0, i // 256, i % 256])
        if write_firmware_page(0x32, write_buffer, 5, firmware[i:i + 128], 128, verbose) < 0:
            print(f"Failed to write page {hex(i)}")
            return False
        time.sleep(0.01)

    progress_bar(length, length)  # Complete the progress bar

    print("Starting firmware")
    jump_buffer = bytearray([0x8, 0x00, 0x00, 0x00, 0x8])
    if execute_command(0x21, jump_buffer, 5, None, 0, verbose) < 0:
        print("Failed to start firmware")
        return False

    return True

def write_firmware_page(opcode, command_buffer, command_length, firmware_buffer, firmware_length, verbose=True):
    """
    Write a page of the firmware to the I2C device.

    :param opcode: The command opcode.
    :param command_buffer: The buffer containing the command data.
    :param command_length: The length of the command data.
    :param firmware_buffer: The buffer containing the firmware data.
    :param firmware_length: The length of the firmware data.
    :param verbose: Whether to print debug information.
    :return: The number of bytes written, or -1 if an error occurred.
    """
    cmd = bytes([opcode, 0xFF ^ opcode])
    i2c.writeto(100, cmd)
    
    if command_length > 0:
        command_buffer[command_length - 1] = 0
        for i in range(command_length - 1):
            command_buffer[command_length - 1] ^= command_buffer[i]
        i2c.writeto(100, command_buffer)
    
    ack = i2c.readfrom(100, 1)[0]
    if ack != 0x79:
        print(f"Error first ack: {hex(ack)}")
        return -1
    
    tmp_buffer = bytearray(firmware_length + 2)
    tmp_buffer[0] = firmware_length - 1
    tmp_buffer[1:firmware_length + 1] = firmware_buffer
    tmp_buffer[firmware_length + 1] = 0
    for i in range(firmware_length + 1):
        tmp_buffer[firmware_length + 1] ^= tmp_buffer[i]
    
    i2c.writeto(100, tmp_buffer)
    ack = i2c.readfrom(100, 1)[0]
    if ack != 0x79:
        print(f"Error: {hex(ack)}")
        return -1
    
    return firmware_length

def progress_bar(current, total, bar_length=40):
    """
    Print a progress bar to the terminal.

    :param current: The current progress value.
    :param total: The total progress value.
    :param bar_length: The length of the progress bar in characters.
    """
    percent = float(current) / total
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f"\rProgress: [{arrow}{spaces}] {int(round(percent * 100))}%")
    sys.stdout.flush()

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
    if len(bin_files) == 1:
        confirm = input(f"Found one bin file: {bin_files[0]}. Do you want to flash it? (yes/no) ")
        if confirm.lower() == 'yes':
            return bin_files[0]
    else:
        print("Found bin files:")
        for index, file in enumerate(bin_files):
            print(f"{index + 1}. {file}")
        choice = int(input("Select the file to flash (number): "))
        return bin_files[choice - 1]

def scan_i2c_devices():
    """
    Scan the I2C bus for devices and prompt the user to select one.

    :return: The selected I2C device address.
    """
    devices = i2c.scan()
    print("I2C devices found:")
    for index, device in enumerate(devices):
        print(f"{index + 1}. Address: {hex(device)}")
    choice = int(input("Select the I2C device to flash (number): "))
    return devices[choice - 1]

def setup():
    """
    Setup function to initialize the flashing process.
    Finds .bin files, scans for I2C devices, and flashes the selected firmware.
    """
    print("Starting setup")

    bin_files = find_bin_files()
    if not bin_files:
        print("No .bin files found in the root directory.")
        return

    bin_file = select_file(bin_files)

    device_address = scan_i2c_devices()
    print(f"Resetting device at address {hex(device_address)}")
    if send_reset(device_address):
        print("Device reset successfully")
    else:
        print("Failed to reset device")
        return

    print(f"Flashing {bin_file} to device at address {hex(BOOTLOADER_I2C_ADDRESS)}")
    
    with open(bin_file, 'rb') as file:
        firmware = file.read()
    
    if flash_firmware(firmware, len(firmware)):
        print("PASS")
    else:
        print("FAIL")

# Start the setup
# setup()