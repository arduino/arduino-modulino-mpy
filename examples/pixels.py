"""
This example shows how to use the ModulinoPixels class to control a set of pixels.

The pixels are set to different colors and animations.
You can use the ModulinoColor class to set predefined colors:
- RED, GREEN, BLUE, YELLOW, CYAN, VIOLET, WHITE

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoPixels, ModulinoColor
from time import sleep

pixels = ModulinoPixels()

if not pixels.connected:
    print("🤷 No pixel modulino found")    
    exit()

for index in range(0, 8):
    color_wheel_colors = [
        (255, 0, 0),
        (255, 85, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 255, 255),
        (0, 0, 255),
        (255, 0, 255),
        (255, 0, 0)
    ]
    pixels.set_rgb(index, *color_wheel_colors[index], 100)
pixels.show()
sleep(1)

pixels.set_all_rgb(255, 0, 0, 100)
pixels.show()
sleep(1)

pixels.set_all_color(ModulinoColor.GREEN, 100)
pixels.show()
sleep(1)

pixels.set_all_color(ModulinoColor.BLUE, 100)
pixels.show()
sleep(1)


# Night Rider animation

for j in range(0, 3):
    for i in range(0, 8):
        pixels.clear_all()
        pixels.set_rgb(i, 255, 0, 0, 100)
        pixels.show()
        sleep(0.05)

    for i in range(7, -1, -1):
        pixels.clear_all()
        pixels.set_rgb(i, 255, 0, 0, 100)
        pixels.show()
        sleep(0.05)

# Turn off all LEDs
pixels.clear_all()    
pixels.show()