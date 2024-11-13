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

def set_glowing_led(index, r, g, b, brightness):
    """
    Set the color of the LED at the given index with its 
    neighboring LEDs slightly dimmed to create a glowing effect.
    """
    pixels.clear_all()
    pixels.set_rgb(index, r, g, b, brightness)

    if index > 0:
        pixels.set_rgb(index - 1, r, g, b, brightness // 8) # LED to the left
    if index < 7:
        pixels.set_rgb(index + 1, r, g, b, brightness // 8) # LED to the right
    
    pixels.show()

for j in range(0, 3):
    for i in range(0, 8):
        set_glowing_led(i, 255, 0, 0, 100)
        sleep(0.05)

    for i in range(7, -1, -1):
        set_glowing_led(i, 255, 0, 0, 100)
        sleep(0.05)

# Turn off all LEDs
# Daisy chain the show() method to send the data to the LEDs
# This works for all the methods that modify the LEDs' appearance.
pixels.clear_all().show()