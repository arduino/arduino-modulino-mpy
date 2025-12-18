from modulino import ModulinoLEDMatrix
from time import sleep_ms

led_matrix = ModulinoLEDMatrix()
led_matrix.clear().show()

for y in range(8):
    for x in range(12):
        led_matrix.set_pixel(x, y)
        led_matrix.show()
        sleep_ms(10)

# Unset all pixels in reverse order
for y in range(7, -1, -1):
    for x in range(11, -1, -1):
        led_matrix.set_pixel(x, y, False)
        led_matrix.show()
        sleep_ms(10)

heart_frame = """
............
.##....##....
##########....
##########....
.########....
..######.....
...####......
....##........
"""
for c in "ARDUINO IS":
    led_matrix.clear()
    led_matrix.text(0, 0, c).show()
    sleep_ms(500)

sleep_ms(1000)
led_matrix.clear()
led_matrix.set_frame_from_ascii(heart_frame).show()