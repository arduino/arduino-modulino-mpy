"""
This example demonstrates how to use the Modulino LED Matrix module.
It shows how to set and unset individual pixels, draw shapes, display text, frames,
and run a simple Matrix-style rain animation.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoLEDMatrix
from time import sleep_ms

led_matrix = ModulinoLEDMatrix()
led_matrix.clear().show()

def fill_pixels(matrix: ModulinoLEDMatrix):
    # Set all pixels one by one
    for y in range(8):
        for x in range(12):
            matrix.set_pixel(x, y)
            matrix.show()
            sleep_ms(10)

def unfill_pixels(matrix: ModulinoLEDMatrix):
    # Unset all pixels in reverse order
    for y in range(7, -1, -1):
        for x in range(11, -1, -1):
            matrix.set_pixel(x, y, False)
            matrix.show()
            sleep_ms(10)

def draw_spiral(matrix: ModulinoLEDMatrix):
    # Spiral pattern
    for layer in range(6):
        for x in range(layer, 12 - layer):
            matrix.set_pixel(x, layer)
            matrix.show()
            sleep_ms(10)
        for y in range(layer + 1, 8 - layer):
            matrix.set_pixel(11 - layer, y)
            matrix.show()
            sleep_ms(10)
        for x in range(11 - layer - 1, layer - 1, -1):
            matrix.set_pixel(x, 7 - layer)
            matrix.show()
            sleep_ms(10)
        for y in range(7 - layer - 1, layer, -1):
            matrix.set_pixel(layer, y)
            matrix.show()
            sleep_ms(10)

def draw_squares(matrix: ModulinoLEDMatrix):
    # Draw small squares and circles
    for i in range(4):
        matrix.rect(i, i, 12 - 2 * i, 8 - 2 * i).show()
        sleep_ms(500)
        matrix.clear()

def draw_circles(matrix: ModulinoLEDMatrix):
    for i in range(4):
        matrix.ellipse(6, 3, 3 - i, 3 - i).show()
        sleep_ms(500)
        matrix.clear()

def display_text_animation(matrix: ModulinoLEDMatrix):
    """Display a simple text animation."""
    for c in "ARDUINO IS":
        matrix.clear()
        matrix.text(2, 0, c).show()
        sleep_ms(250)

def display_ascii_frame(matrix: ModulinoLEDMatrix):
    """Display a simple ASCII art frame."""
    heart_frame = """
    ............
    ..##....##..
    .##########.
    .##########.
    ..########..
    ...######...
    ....####....
    .....##.....
    """
    matrix.clear()
    matrix.set_frame_from_ascii(heart_frame).show()

def raining_code(matrix: ModulinoLEDMatrix, steps: int = 300, spawn_chance: int = 35, delay_ms: int = 70):
    """Play a brief Matrix-style rain animation."""
    from random import getrandbits

    def _randint(n: int) -> int:
        """Small helper to avoid importing full random."""
        return getrandbits(16) % n

    drops = []  # each drop: (x, head_y, length)

    for _ in range(steps):
        # Maybe spawn a new drop at the top
        if _randint(100) < spawn_chance:
            x = _randint(12)
            length = 2 + _randint(4)  # 2..5 pixels long
            drops.append([x, -1, length])

        matrix.clear()

        active = []
        for x, head_y, length in drops:
            head_y += 1
            tail_y = head_y - length

            # Draw the drop from head down to tail within bounds
            for y in range(max(0, tail_y), min(matrix._height, head_y + 1)):
                matrix.set_pixel(x, y, True)

            # Keep drop if it still intersects the display
            if tail_y < matrix._height:
                active.append([x, head_y, length])

        drops = active
        matrix.show()
        sleep_ms(delay_ms)

def draw_checkerboard(matrix: ModulinoLEDMatrix):
    """Draw a checkerboard pattern using hline and vline."""
    for y in range(8):
        if y % 2 == 0:
            matrix.hline(0, y, 12, True)
    for x in range(12):
        if x % 2 == 0:
            matrix.vline(x, 0, 8, True)
                
    matrix.show()
def draw_diamond(matrix: ModulinoLEDMatrix):
    """Draw a diamond shape using poly()."""
    points = [6, 0, 11, 3, 6, 7, 1, 3]
    matrix.poly(0,0,points).show()
    

# Run the animations sequentially
fill_pixels(led_matrix)
sleep_ms(500)
unfill_pixels(led_matrix)
sleep_ms(500)
draw_spiral(led_matrix)
sleep_ms(500)
draw_squares(led_matrix)
sleep_ms(500)
draw_circles(led_matrix)
sleep_ms(500)
draw_checkerboard(led_matrix)
sleep_ms(500)
display_text_animation(led_matrix)
sleep_ms(500)
display_ascii_frame(led_matrix)
sleep_ms(500)
raining_code(led_matrix)
led_matrix.clear().show()