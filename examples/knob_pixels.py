"""
Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoKnob, ModulinoPixels, ModulinoColor

class ConstrainedIndex:
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.value = min

    def increment(self):
        self.value = min(self.value + 1, self.max)
        return self.value

    def decrement(self):
        self.value = max(self.value - 1, self.min)
        return self.value

knob = ModulinoKnob()
pixels = ModulinoPixels()

# 8 pixels, index is 0-based. -1 means all pixels are off.
pixel_index = ConstrainedIndex(-1, 7)

def update_pixels():
    pixels.clear_all()
    if pixel_index.value >= 0:
        pixels.set_range_color(0, pixel_index.value, ModulinoColor.GREEN)
    pixels.show()

def on_knob_rotate_clockwise(_):
    pixel_index.increment()
    update_pixels()

def on_knob_rotate_counter_clockwise(_):
    pixel_index.decrement()
    update_pixels()

knob.on_rotate_clockwise = on_knob_rotate_clockwise
knob.on_rotate_counter_clockwise = on_knob_rotate_counter_clockwise

while True:
    if(knob.update()):
        print(f"New level: {pixel_index.value}")