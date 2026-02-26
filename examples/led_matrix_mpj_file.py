"""
This example demonstrates how to load an MPJ animation file onto the Modulino LED Matrix.
These files can be created using the online tool under https://ledmatrix-editor.arduino.cc/

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoLEDMatrix, MPJAnimation

led_matrix = ModulinoLEDMatrix(use_grayscale=False)
led_matrix.clear().show()

try:
    animation = MPJAnimation(led_matrix, '/animation.mpj')
    print(f"Playing animation with {animation.frame_count} frames.")
    print("Press Ctrl+C to stop.")
    animation.play(loop=True)

except KeyboardInterrupt:
    print("Animation stopped by user.")
    led_matrix.clear().show()