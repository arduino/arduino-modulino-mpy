"""
Script to convert C++ frame data into Python format for Modulino LED Matrix animations.
You can use the output of this script to provide the frame data to 
an Animation object. E.g.:

```
from modulino import ModulinoLEDMatrix, Animation
led_matrix = ModulinoLEDMatrix(use_grayscale=False)

animation = [
    (b'\x00\x00\x00\xfe\x82\x8a\x82\x8a\x82\xfe\x00\x00', 250),
    (b'\x00\x00\x00\xfe\x82\x8a\xa2\x8a\x82\xfe\x00\x00', 250),
    (b'\x00\x00\x00\xfe\x82\xaa\xa2\xaa\x82\xfe\x00\x00', 1000)
]

animation = Animation(led_matrix, animation)
animation.play()
```

Usage: python convert_frames_mpy.py <input_file> [--order {row-major,column-major}]

Expected input format:
	Data type: uint32_t (32-bit unsigned integers)
	Endianness: Big-endian bit ordering within the 32-bit words
	Pixel order: Column-major by default (pixels ordered top-to-bottom, left-to-right), but can be set to row-major via --order.

Example input:

const uint32_t animation[][4] = {
    { 0x1fc10, 0x41041041, 0x41041fc, 66 },
    { 0x1fc10, 0x41441041, 0x41041fc, 66 }
};

Output format:
	Python list of tuples: [(frame_bytes, duration), ...]
	- frame_bytes: 12 bytes representing the 12 columns of the LED matrix in column-major order (each byte corresponds to a column, with bits representing rows)
	- duration: integer representing the duration of the frame in milliseconds
    
"""

import re
import sys
import argparse

parser = argparse.ArgumentParser(description="Convert C++ frame data into Python format for Modulino LED Matrix animations.")
parser.add_argument("input_file", help="Input file containing C++ frame data")
parser.add_argument("--order", choices=["row-major", "column-major"], default="column-major", help="Pixel order of the input data (default: column-major)")

args = parser.parse_args()

with open(args.input_file, 'r') as f:
	cpp_code = f.read()

if not cpp_code.strip():
	print("Input file is empty.")
	sys.exit(1)

# RegEx to match content inside brackets
pattern = re.compile(r"\{\s*(0x[0-9a-fA-F]+)\s*,\s*(0x[0-9a-fA-F]+)\s*,\s*(0x[0-9a-fA-F]+)\s*,\s*(\d+)\s*\}")

frames = []

for match in pattern.finditer(cpp_code):
    frame_parts = [int(match.group(i), 16) for i in range(1, 4)]
    duration = int(match.group(4))
    
    # Conversion logic
    column_buffer = bytearray(12)
    for col in range(12):
        for row in range(8):
            if args.order == "row-major":
                linear_pixel_index = row * 12 + col
            else:
                linear_pixel_index = col * 8 + row
            
            part_index = linear_pixel_index // 32
            bit_index = 31 - (linear_pixel_index % 32)
            
            if (frame_parts[part_index] >> bit_index) & 1:
                column_buffer[col] |= (1 << row)
    
    frames.append((bytes(column_buffer), duration))

def to_hex_literal(b):
    return "b'" + "".join(f"\\x{x:02x}" for x in b) + "'"

# Extract array name if present
array_name = "frames"
name_match = re.search(r"(?:const\s+)?(?:uint32_t|int|uint8_t)\s+(\w+)\s*\[", cpp_code)
if name_match:
    array_name = name_match.group(1)

# Print the python list repr
print(f'{array_name} = [')
for frame_bytes, duration in frames:
    print(f"    ({to_hex_literal(frame_bytes)}, {duration}),")
print(']')
