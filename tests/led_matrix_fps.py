"""
This test measures the frames per second (FPS) achievable by the Modulino LED matrix
when rapidly switching between two frames.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoLEDMatrix
from time import ticks_ms

use_grayscale = False
multiplier = 48 if use_grayscale else 12
led_matrix = ModulinoLEDMatrix(use_grayscale=use_grayscale)
led_matrix.clear().show()

frame1 = b'\x77' * multiplier
frame2 = b'\xFF' * multiplier

frames = [frame1, frame2]

# Calculate FPS by switching between two frames rapidly for 10 seconds
duration_ms = 10000
end_time = ticks_ms() + duration_ms
frame_count = 0

i = 0
while ticks_ms() < end_time:
    led_matrix.set_frame(frames[i % 2]).show()
    i += 1
    frame_count += 1  # One frame per loop

fps = frame_count / (duration_ms / 1000)
print("Achieved FPS: {:.2f}".format(fps))