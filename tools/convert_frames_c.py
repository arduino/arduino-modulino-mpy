"""
Script to convert C frame data in uint32_t big-endian row-major order 
into uint8_t C format column-major order for Modulino LED Matrix animations.
You can use the output of this script to provide the frame data to your animation code. E.g.:

```
constexpr uint8_t animation[][16] = {
    { 0x00, 0x00, 0x00, 0xfe, 0x82, 0x8a, 0x82, 0x8a, 0x82, 0xfe, 0x00, 0x00, 0x42, 0x00, 0x00, 0x00 },
    { 0x00, 0x00, 0x00, 0xfe, 0x82, 0x8a, 0xa2, 0x8a, 0x82, 0xfe, 0x00, 0x00, 0x42, 0x00, 0x00, 0x00 },
    { 0x00, 0x00, 0x00, 0xfe, 0x82, 0xaa, 0xa2, 0xaa, 0x82, 0xfe, 0x00, 0x00, 0xe8, 0x03, 0x00, 0x00 }
};

matrix.setMode(DisplayMode::MONOCHROMATIC_VERTICAL);
matrix.setSequence(animation);
matrix.play();
```

Usage: python convert_frames_c.py <input_file>

Expected input format:
	Data type: uint32_t (32-bit unsigned integers)
	Endianness: Big-endian bit ordering within the 32-bit words
	Pixel order: Row-major (pixels are ordered left-to-right, top-to-bottom)

Example input:
const uint32_t animation[][4] = {
	{ 0x1fc10, 0x41041041, 0x41041fc, 66 },
	{ 0x1fc10, 0x41441041, 0x41041fc, 66 }
};

Output format:
	constexpr uint8_t frames[][16] = {
		{ 0x00, 0x00, 0x00, 0xfe, 0x82, 0x82, 0x82, 0x82, 0x82, 0xfe, 0x00, 0x00, 0x42, 0x00, 0x00, 0x00 },
    	{ 0x00, 0x00, 0x00, 0xfe, 0x82, 0x8a, 0x82, 0x82, 0x82, 0xfe, 0x00, 0x00, 0x42, 0x00, 0x00, 0x00 }
	};
	- Each frame is represented as 16 bytes: 12 bytes for the column data (each byte corresponds to a column, with bits representing rows) 
	followed by 4 bytes for the duration (in milliseconds, little-endian format)
"""

import re
import struct
import sys

# Read from file provided as argument
if len(sys.argv) < 2:
	print("Usage: python convert_frames_c.py <input_file>")
	sys.exit(1)

with open(sys.argv[1], 'r') as f:
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
            linear_pixel_index = row * 12 + col
            part_index = linear_pixel_index // 32
            bit_index = 31 - (linear_pixel_index % 32)
            
            if (frame_parts[part_index] >> bit_index) & 1:
                column_buffer[col] |= (1 << row)
    
    frames.append((bytes(column_buffer), duration))

def print_as_uint32_array(frames):
	print('constexpr uint32_t frames[][4] = {')
	for frame_bytes, duration in frames:
		# Pack 12 bytes into 3x 32-bit integers (Little Endian)
		ints = struct.unpack('<III', frame_bytes)
		print(f"    {{ 0x{ints[0]:x}, 0x{ints[1]:x}, 0x{ints[2]:x}, {duration} }},")
	print('};')

def print_as_uint8_array(frames, array_name="frames", skip_duration=False):
	if skip_duration:
		print(f'constexpr uint8_t {array_name}[][12] = {{')
	else:
		print(f'constexpr uint8_t {array_name}[][16] = {{')
	for frame_bytes, duration in frames:
		byte_literals = ", ".join(f"0x{b:02x}" for b in frame_bytes)
		if skip_duration:
			print(f"    {{ {byte_literals} }}, // Duration: {duration} ms")
		else:
			# Include duration as 4 bytes at the end (Little Endian)
			duration_bytes = struct.pack('<I', duration)
			duration_literals = ", ".join(f"0x{b:02x}" for b in duration_bytes)
			print(f"    {{ {byte_literals}, {duration_literals} }},")
	print('};')

# Extract array name if present
array_name = "frames"
name_match = re.search(r"(?:const\s+)?(?:uint32_t|int|uint8_t)\s+(\w+)\s*\[", cpp_code)
if name_match:
    array_name = name_match.group(1)

print_as_uint8_array(frames, array_name=array_name, skip_duration=False)