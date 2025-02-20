import os
import sys
from machine import I2C, Pin
import time
from micropython import const

BOOTLOADER_I2C_ADDRESS = const(0x64)
ACK = const(0x79)
BUSY = const(0x76)

CMD_GET = const(0x00) # Gets the version and the allowed commands
CMD_GET_LENGTH_V12 = const(20) # Length of the response data
CMD_GET_VERSION = const(0x01) # Gets the protocol version
CMD_GET_ID = const(0x02) # Get chip ID
CMD_ERASE = const(0x44) # Erase memory
CMD_GO = const(0x21) # Jumps to user application code located in the internal flash memory
CMD_WRITE_NO_STRETCH = const(0x32) # Writes up to 256 bytes to the memory, starting from an address specified
CHUNK_SIZE = const(128) # Size of the memory chunk to write

# Define I2C pins and initialize I2C
i2c = I2C(0, freq=100000)

def send_reset(address):
    """
    Send a reset command to the I2C device at the given address.

    :param address: I2C address of the device.
    :return: 0 if the reset command was sent successfully, otherwise -1.
    """
    buffer = b'DIE'
    buffer += b'\x00' * (8 - len(buffer)) # Pad buffer to 8 bytes

    try:
        print(f"🔄 Resetting device at address {hex(address)}")
        i2c.writeto(address, buffer, True)
        print("✅ Reset command sent successfully")
        time.sleep(0.25) # Wait for the device to reset
        return True
    except OSError as e:
        # ENODEV can be thrown if either the device reset while writing out the buffer or if the device
        # was already in bootloader mode in which case there is no device at the original address
        if e.errno == 19:
            time.sleep(0.25) # Wait for the device to reset
            return True
        else:
            print(f"Error sending reset command: {e}")
            return False

def wait_for_ack():
    """
    Wait for an acknowledgment from the I2C device.

    :return: True if an acknowledgment was received, otherwise False.
    """
    res = i2c.readfrom(BOOTLOADER_I2C_ADDRESS, 1)[0]
    if res != ACK:
        while res == BUSY:
            time.sleep(0.1)
            res = i2c.readfrom(BOOTLOADER_I2C_ADDRESS, 1)[0]
        if res != ACK:
            print(f"❌ Error processing command. Result code: {hex(res)}")
            return False
    return True

def execute_command(opcode, command_params, response_length = 0, verbose=False):
    """
    Execute an I2C command on the device.

    :param opcode: The command opcode.
    :param command_params: The buffer containing the command parameters.
    :param response_length: The expected length of the response data frame.
    :param verbose: Whether to print debug information.
    :return: The number of response bytes read, or None if an error occurred.
    """
    if verbose:
        print(f"🕵️ Executing command {hex(opcode)}")

    cmd = bytes([opcode, 0xFF ^ opcode]) # Send command code and complement (XOR = 0x00)
    i2c.writeto(BOOTLOADER_I2C_ADDRESS, cmd, True)
    if not wait_for_ack():
        print(f"❌ Command not acknowledged: {hex(opcode)}")
        return None

    if command_params is not None:
        i2c.writeto(BOOTLOADER_I2C_ADDRESS, command_params, True)
        if not wait_for_ack():
            print("❌ Command failed")
            return None

    if response_length == 0:
        return None

    data = i2c.readfrom(BOOTLOADER_I2C_ADDRESS, response_length)

    if not wait_for_ack():
        print("❌ Failed completing command")
        return None

    return data

def flash_firmware(firmware_path, verbose=False):
    """
    Flash the firmware to the I2C device.

    :param firmware: The binary firmware data.
    :param length: The length of the firmware data.
    :param verbose: Whether to print debug information.
    :return: True if the flashing was successful, otherwise False.
    """
    data = execute_command(CMD_GET_VERSION, None, 1, verbose)
    if data is None:
        print("❌ Failed to get protocol version")
        return False
    print(f"ℹ️ Protocol version: {data[0] & 0xF}.{data[0] >> 4}")

    data = execute_command(CMD_GET, None, CMD_GET_LENGTH_V12, verbose)
    if data is None:
        print("❌ Failed to get command list")
        return False
    
    print(f"ℹ️ Bootloader version: {(data[1] & 0xF)}.{data[1] >> 4}")
    print("👀 Supported commands:")
    print(", ".join([hex(byte) for byte in data[2:]]))

    data = execute_command(CMD_GET_ID, None, 3, verbose)
    if data is None:
        print("❌ Failed to get device ID")
        return False
    
    chip_id = (data[0] << 8) | data[1] # Chip ID: Byte 1 = MSB, Byte 2 = LSB
    print(f"ℹ️ Chip ID: {chip_id}")

    print("🗑️ Erasing memory...")
    erase_params = bytearray([0xFF, 0xFF, 0x0]) # Mass erase flash
    #execute_command(CMD_ERASE, erase_params, 0, verbose)

    with open(firmware_path, 'rb') as file:
        firmware_data = file.read()
    total_bytes = len(firmware_data)

    print(f"🔥 Flashing {total_bytes} bytes of firmware")
    for i in range(0, total_bytes, CHUNK_SIZE):
        progress_bar(i, total_bytes)
        start_address = bytearray([8, 0, i // 256, i % 256]) # 4-byte address: byte 1 = MSB, byte 4 = LSB
        checksum = 0
        for b in start_address:
            checksum ^= b        
        start_address.append(checksum)
        data_slice = firmware_data[i:i + CHUNK_SIZE]
        if not write_firmware_page(start_address, data_slice):
            print(f"❌ Failed to write page {hex(i)}")
            return False
        time.sleep(0.01) # Give the device some time to process the data

    progress_bar(total_bytes, total_bytes)  # Complete the progress bar

    print("🏃 Starting firmware")
    go_params = bytearray([0x8, 0x00, 0x00, 0x00, 0x8])
    #execute_command(CMD_GO, go_params, 0, verbose) # Jump to the application

    return True

def write_firmware_page(command_params, firmware_data):
    """
    Write a page of the firmware to the I2C device.

    :param command_params: The buffer containing the command parameters.
    :param firmware_data: The buffer containing the firmware data.
    :return: True if the page was written successfully, otherwise False.
    """
    cmd = bytes([CMD_WRITE_NO_STRETCH, 0xFF ^ CMD_WRITE_NO_STRETCH])
    i2c.writeto(BOOTLOADER_I2C_ADDRESS, cmd)
    if not wait_for_ack():
        print("❌ Write command not acknowledged")
        return False
    
    i2c.writeto(BOOTLOADER_I2C_ADDRESS, command_params)
    if not wait_for_ack():
        print("❌ Failed to write command parameters")
        return False
    
    data_size = len(firmware_data)
    tmp_buffer = bytearray(data_size + 2) # Data plus size and checksum
    tmp_buffer[0] = data_size - 1 # Size of the data # TODO Arduino code uses data_size - 1
    tmp_buffer[1:data_size + 1] = firmware_data
    tmp_buffer[-1] = 0 # Checksum placeholder
    for i in range(data_size + 1): # Calculate checksum over size byte + data bytes
        tmp_buffer[-1] ^= tmp_buffer[i]
    
    i2c.writeto(BOOTLOADER_I2C_ADDRESS, tmp_buffer)    
    if not wait_for_ack():
        print("❌ Failed to write firmware")
        return False
    
    return True

def progress_bar(current, total, bar_length=40):
    """
    Print a progress bar to the terminal.

    :param current: The current progress value.
    :param total: The total progress value.
    :param bar_length: The length of the progress bar in characters.
    """
    percent = float(current) / total
    arrow = '-' * int(round(percent * bar_length))
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
    if len(bin_files) == 1:
        confirm = input(f"👀 Found one bin file: {bin_files[0]}. Do you want to flash it? (yes/no) ")
        if confirm.lower() == 'yes':
            return bin_files[0]
    else:
        print("👀 Found bin files:")
        for index, file in enumerate(bin_files):
            print(f"{index + 1}. {file}")
        choice = int(input("Select the file to flash (number): "))
        return bin_files[choice - 1]

def select_i2c_device():
    """
    Scan the I2C bus for devices and prompt the user to select one.

    :return: The selected I2C device address.
    """
    devices = i2c.scan()
    print("👀 I2C devices found:")
    for index, device in enumerate(devices):
        print(f"{index + 1}. Address: {hex(device)}")
    choice = int(input("Select the I2C device to flash (number): "))
    return devices[choice - 1]

def setup():
    """
    Setup function to initialize the flashing process.
    Finds .bin files, scans for I2C devices, and flashes the selected firmware.
    """

    bin_files = find_bin_files()
    if not bin_files:
        print("❌ No .bin files found in the root directory.")
        return

    bin_file = "node_base.bin" # select_file(bin_files)

    device_address = 30 # select_i2c_device()    
    if send_reset(device_address):
        print("✅ Device reset successfully")
    else:
        print("❌ Failed to reset device")
        return

    print(f"🕵️ Flashing {bin_file} to device at address {hex(BOOTLOADER_I2C_ADDRESS)}")
    
    if flash_firmware(bin_file):
        print("✅ Firmware flashed successfully")
    else:
        print("❌ Failed to flash firmware")

# Start the setup
setup()
