"""
This example demonstrates using the Modulino LED Matrix in grayscale mode.
It includes functions to create a fade pattern and a Matrix-style rain animation.
In this mode, each pixel can have 16 levels of brightness (0-15).

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoLEDMatrix
from time import sleep_ms

led_matrix = ModulinoLEDMatrix(use_grayscale=True)
led_matrix.clear().show()

def fade_pattern(matrix: ModulinoLEDMatrix):
    # Set each row of 12 pixels to increasing brightness
    for row in range(8):
        for col in range(12):
            brightness = col  # Brightness increases from 0 to 11
            matrix.set_pixel(col, row, brightness)
    matrix.show()

def raining_code(matrix: ModulinoLEDMatrix, steps: int = 300, spawn_chance: int = 35, delay_ms: int = 70):
    """Play a brief Matrix-style rain animation with a grayscale trail."""
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

            # Draw the drop from head down to tail within bounds, brighter toward the head
            for y in range(max(0, tail_y), min(matrix._height, head_y + 1)):
                distance_from_head = head_y - y  # 0 at head, increases upward
                brightness = 15 - (distance_from_head * 14) // max(1, length - 1)
                brightness = 0 if brightness < 0 else brightness  # clamp to avoid wrapping negatives
                matrix.set_pixel(x, y, brightness)

            # Keep drop if it still intersects the display
            if tail_y < matrix._height:
                active.append([x, head_y, length])

        drops = active
        matrix.show()
        sleep_ms(delay_ms)


fade_pattern(led_matrix)
sleep_ms(2000)
led_matrix.clear()

raining_code(led_matrix)