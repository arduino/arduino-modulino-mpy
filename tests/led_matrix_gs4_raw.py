"""
Test script for controlling an LED matrix in 4-bit grayscale (GS4) mode
using raw bytearray data.
"""

from machine import I2C
from time import sleep_ms

bus = I2C(0)
dev_addr = 0x39

# After boot the LED matrix is in monochrome mode
# We need to switch it to GS4 (4-bit grayscale) mode
buffer = b'GS4'
buffer += b'\x00' * (12 - len(buffer))
bus.writeto(dev_addr, buffer)

pixel_data = bytearray(48)
# Each pixels is represented by 4-bits (nibble) for grayscale (0-15)
# Therefore, 16 pixels can be stored in 8 bytes

def set_pixel(pixel_index: int, brightness: int) -> None:
    """
    Sets the brightness of a specific pixel.

    Parameters:
        pixel_index (int): The index of the pixel (0-95).
        brightness (int): The brightness level (0-15).
    """
    if pixel_index < 0 or pixel_index > 95:
        raise ValueError("Pixel index must be between 0 and 95")
    if brightness < 0 or brightness > 15:
        raise ValueError("Brightness must be between 0 and 15")

    byte_index = pixel_index // 2
    if pixel_index % 2 == 0:
        # Even index - set high nibble
        pixel_data[byte_index] = (pixel_data[byte_index] & 0x0F) | (brightness << 4)
    else:
        # Odd index - set low nibble
        pixel_data[byte_index] = (pixel_data[byte_index] & 0xF0) | brightness

def fade_in_pixel(pixel_index: int, delay_ms: int = 100) -> None:
    for i in range(16):
        set_pixel(pixel_index, i)
        bus.writeto(dev_addr, pixel_data)
        sleep_ms(delay_ms)

# Set each row of 12 pixels to increasing brightness
for row in range(8):
    for col in range(12):
        pixel_index = row * 12 + col
        brightness = col  # Brightness increases from 0 to 11
        set_pixel(pixel_index, brightness)

for p in range(96):
    # Print each pixel in decimal format, odd indexes are high nibbles
    index = p // 2
    brightness = None
    
    if p % 2 == 0:
        brightness = pixel_data[index] & 0x0F
    else:
        brightness = (pixel_data[index] >> 4) & 0x0F
        
    print(f"Index {p}: Byte {index} Brightness {brightness}")
print()

bus.writeto(dev_addr, pixel_data)