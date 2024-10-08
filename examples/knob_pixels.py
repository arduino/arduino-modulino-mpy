"""
This example shows how to use the ModulinoKnob and ModulinoPixels classes to control a set of pixels with a knob.

The knob is used to set the number of pixels to turn on.
The range property of the knob is used to map the knob values to the number of pixels to turn on.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoKnob, ModulinoPixels, ModulinoColor

knob = ModulinoKnob()
pixels = ModulinoPixels()

# 8 pixels, index is 0-based. -1 means all pixels are off.
knob.value = -1
knob.range = (-1, 7)

def update_pixels():
    pixels.clear_all()
    if knob.value >= 0:
        pixels.set_range_color(0, knob.value, ModulinoColor.GREEN)
    pixels.show()

while True:
    if(knob.update()):
        print(f"New level: {knob.value}")
        update_pixels()