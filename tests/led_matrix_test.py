from modulino import ModulinoLEDMatrix
from time import sleep_ms

led_matrix = ModulinoLEDMatrix()
led_matrix.clear().show()

# Fill row by row
def fill_rows(matrix: ModulinoLEDMatrix):
    # Set all pixels one by one
    for y in range(8):
        for x in range(12):
            matrix.set_pixel(x, y)
            matrix.show()
            sleep_ms(100)

# Fill column by column
def fill_columns(matrix: ModulinoLEDMatrix):
    for x in range(12):
        for y in range(8):
            matrix.set_pixel(x, y)
            matrix.show()
            sleep_ms(100)

def fade_pattern(matrix: ModulinoLEDMatrix):
    # Set each row of 12 pixels to increasing brightness
    for row in range(8):
        for col in range(12):
            brightness = col  # Brightness increases from 0 to 11
            matrix.set_pixel(col, row, brightness)
    matrix.show()

led_matrix.fill().show()
sleep_ms(1000)
led_matrix.clear()

fill_rows(led_matrix)
led_matrix.clear()

fill_columns(led_matrix)
led_matrix.clear()

led_matrix.text(2,0,"A").show()
sleep_ms(2000)
led_matrix.clear()

led_matrix.use_grayscale = True
fade_pattern(led_matrix)