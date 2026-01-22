"""
Convert images (individual files or inside a zip) to Modulino MPY frames (Python list of byte arrays).
Optionally rotate images to adjust for orientation.

Example usage:
  python convert_frames_mpy.py images.zip --rotate -90 > animation.py
"""
import argparse
import sys
import zipfile
import io
import math
import os
from typing import List, Tuple, Optional
from PIL import Image

def gamma_correct(pixel_value: int) -> int:
    """
    Apply gamma correction to a pixel value and scale it to 4-bit (0-15).
    """
    corrected = int(math.pow(pixel_value / 255.0, 2.7) * 15.0 + 0.5)
    return max(0, min(15, corrected))

def process_image(image_data: bytes, rotation: int, target_size: Tuple[int, int] = (12, 8)) -> Optional[bytearray]:
    """
    Process a single image: load, grayscale, rotate, resize, and pack bits.
    
    Args:
        image_data: Raw bytes of the image file.
        rotation: Degrees to rotate the image (counter-clockwise).
        target_size: Tuple of (width, height) for the output image.
        
    Returns:
        bytearray of packed pixel data, or None if processing failed.
    """
    try:
        img = Image.open(io.BytesIO(image_data))
    except Exception as e:
        sys.stderr.write(f"Error opening image: {e}\n")
        return None
    
    # Convert to grayscale
    if img.mode != 'L':
        img = img.convert('L')
    
    # Rotate if needed
    if rotation != 0:
        img = img.rotate(rotation, expand=True)
        
    # Resize to target size (default 12x8)
    img = img.resize(target_size, Image.BICUBIC)
    
    pixels = img.load()
    width, height = img.size
    
    packed_bytes = bytearray()
    
    # Iterate over rows
    for y in range(height):
        # Iterate over columns in pairs
        for x in range(0, width, 2):
            # Get pixels and gamma correct
            p1 = gamma_correct(pixels[x, y])
            
            if x + 1 < width:
                p2 = gamma_correct(pixels[x+1, y])
            else:
                p2 = 0
            
            # Pack: High Nibble for Even pixel (p1), Low Nibble for Odd pixel (p2)
            byte_val = (p1 << 4) | (p2 & 0x0F)
            packed_bytes.append(byte_val)
            
    return packed_bytes

def process_zip(zip_path: str, rotation: int) -> List[bytearray]:
    """
    Process images inside a zip file.
    
    Returns:
        A list of frame data (bytearrays).
    """
    frames = []
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as myzip:
            file_list = sorted(myzip.namelist())
            for fname in file_list:
                if fname.endswith('/'):
                    continue
                
                # Ignore macOS metadata files
                if '__MACOSX' in fname or os.path.basename(fname).startswith('._'):
                    continue
                
                # Process image files
                if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                        with myzip.open(fname) as myfile:
                            data = myfile.read()
                            res = process_image(data, rotation)
                            if res:
                                frames.append(res)
    except Exception as e:
        sys.stderr.write(f"Error reading zip file {zip_path}: {e}\n")
        
    return frames

def process_file(file_path: str, rotation: int) -> Optional[bytearray]:
    """
    Process a single image file on disk.
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            return process_image(data, rotation)
    except Exception as e:
        # Ignore non-image errors gracefully (like unrelated files passed in)
        if not file_path.endswith('.py'):
            sys.stderr.write(f"Error reading file {file_path}: {e}\n")
    return None

def generate_output(frames: List[bytearray]):
    """
    Print the generated Python code to stdout.
    """
    print("# Auto-generated frame data")
    print("")
    print("frames = [")
    for frame in frames:
        hex_content = "".join(f"\\x{b:02x}" for b in frame)
        print(f"    b'{hex_content}',")
    print("]")

def main():
    parser = argparse.ArgumentParser(description='Convert images to Modulino MPY frames (Python list of byte arrays).')
    parser.add_argument('input_files', nargs='+', help='Image files or zip file')
    parser.add_argument('--rotate', type=int, default=0, help='Rotation angle in degrees (positive = counter-clockwise). Useful for adjusting portrait/landscape orientation.')
    
    args = parser.parse_args()
    
    all_frames = []
    
    for input_file in args.input_files:
        if input_file.lower().endswith('.zip'):
            frames = process_zip(input_file, args.rotate)
            all_frames.extend(frames)
        else:
            res = process_file(input_file, args.rotate)
            if res:
                all_frames.append(res)

    generate_output(all_frames)

if __name__ == '__main__':
    main()

