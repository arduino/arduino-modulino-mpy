"""
Convert a video file into a ZIP archive of grayscale PNG frames with optional contrast adjustment, resizing, and cropping.
Note that the cropping happens before resizing.

Requires OpenCV. Install via:
  pip install opencv-python

Example usage:
  python convert_video.py input_video.mp4 output_frames.zip --contrast 1.5 --resize 12 --crop "100,50,640,480"

Arguments:
  input_video: Path to the input video file. Supported formats depend on your OpenCV installation (commonly .mp4, .avi, etc.).
  output_zip: Path to the output ZIP file that will contain the extracted frames as PNG images.
  --contrast: (Optional) Contrast adjustment factor. 1.0 means no change, >1.0 increases contrast, <1.0 decreases contrast.
  --resize: (Optional) Resize the frames so that their maximum dimension (width or height) matches this value, while preserving aspect ratio.
  --crop: (Optional) Crop region specified as "x,y,w,h".
          - x: The x-coordinate of the top-left corner of the crop rectangle.
          - y: The y-coordinate of the top-left corner of the crop rectangle.
          - w: The width of the crop rectangle.
          - h: The height of the crop rectangle.
          The crop will be applied before resizing. If the specified crop region exceeds the image bounds, it will be automatically clamped to fit within the image.
Output:
  A ZIP file containing the extracted frames as grayscale PNG images, named sequentially as frame_00000.png, frame_00001.png, etc.
"""

import argparse
import zipfile
import os
import sys
from typing import Optional, Tuple

# Try importing OpenCV
try:
    import cv2
except ImportError:
    print("Error: 'opencv-python' is not installed. Please install it using:")
    print("  pip install opencv-python")
    sys.exit(1)

def apply_crop(image, crop):
    """
    Crop the image based on the provided (x, y, w, h) tuple.
    Clamps the crop region to ensure it stays within image bounds.
    """
    x, y, w, h = crop
    img_h, img_w = image.shape
    
    # Clamp crop region to image bounds
    x = max(0, min(x, img_w - 1))
    y = max(0, min(y, img_h - 1))
    w = max(1, min(w, img_w - x))
    h = max(1, min(h, img_h - y))
    
    return image[y:y+h, x:x+w]

def apply_contrast(image, contrast):
    """
    Apply centered contrast adjustment (around 127).
    """
    beta = 127 * (1.0 - contrast)
    return cv2.convertScaleAbs(image, alpha=contrast, beta=beta)

def apply_resize(image, resize_dim):
    """
    Resize the image so its maximum dimension matches resize_dim,
    preserving aspect ratio.
    """
    h, w = image.shape[:2]
    
    if w >= h: # Landscape or Square
        new_w = resize_dim
        new_h = int(h * (resize_dim / w))
    else: # Portrait
        new_h = resize_dim
        new_w = int(w * (resize_dim / h))
    
    # Ensure dimensions are at least 1x1
    new_w = max(1, new_w)
    new_h = max(1, new_h)
    
    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

def video_to_zip(video_path: str, zip_path: str, contrast: float = 1.0, resize_dim: Optional[int] = None, crop: Optional[Tuple[int, int, int, int]] = None):
    """
    Reads a video file, extracts all frames, converts them to grayscale,
    applies contrast adjustment, resize, optional crop, and saves them as PNGs into a ZIP archive.
    
    crop is a tuple of (x, y, width, height)
    """
    if not os.path.isfile(video_path):
        print(f"Error: Input video '{video_path}' does not exist.")
        return

    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'")
        return

    # Create directory for zip file if it doesn't exist
    zip_dir = os.path.dirname(os.path.abspath(zip_path))
    if zip_dir and not os.path.exists(zip_dir):
        os.makedirs(zip_dir)

    frame_count = 0
    print(f"Processing {video_path} -> {zip_path}...")
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as myzip:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Crop if requested
                if crop:
                    gray = apply_crop(gray, crop)

                # Apply contrast
                if contrast != 1.0:
                    gray = apply_contrast(gray, contrast)
                
                # Resize keeping aspect ratio
                if resize_dim:
                    gray = apply_resize(gray, resize_dim)

                # Encode frame to PNG in memory
                success, buffer = cv2.imencode(".png", gray)
                if not success:
                   print(f"Warning: Failed to encode frame {frame_count}")
                   continue
                
                # Write to zip
                file_name = f"frame_{frame_count:05d}.png"
                myzip.writestr(file_name, buffer.tobytes())
                
                frame_count += 1
                if frame_count % 30 == 0:
                    print(f"Extracted {frame_count} frames", end='\r')

        print(f"\nDone! Extracted {frame_count} frames to '{zip_path}'.")
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        cap.release()

def parse_crop_arg(crop_str: str) -> Optional[Tuple[int, int, int, int]]:
    """Parse 'x,y,w,h' string into a tuple of integers."""
    if not crop_str:
        return None
    try:
        parts = [int(p.strip()) for p in crop_str.split(',')]
        if len(parts) != 4:
            raise ValueError
        return tuple(parts)
    except:
        print("Error: Crop argument must be in format 'x,y,w,h' (e.g., '100,50,640,480')")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Extract video frames to grayscale PNGs and save as a ZIP file.')
    parser.add_argument('input_video', help='Input video file path')
    parser.add_argument('output_zip', help='Output ZIP file path')
    parser.add_argument('--contrast', type=float, default=1.0, help='Contrast factor (1.0 = original, >1.0 = increased contrast)')
    parser.add_argument('--resize', type=int, help='Resize max dimension to this value (keeping aspect ratio). If not provided, original size is kept.')
    parser.add_argument('--crop', type=str, help='Crop region in format "x,y,w,h". Applied before resizing.')

    args = parser.parse_args()
    
    crop_tuple = parse_crop_arg(args.crop)
    video_to_zip(args.input_video, args.output_zip, args.contrast, args.resize, crop_tuple)

if __name__ == '__main__':
    main()
