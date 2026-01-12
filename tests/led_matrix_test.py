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

#fill_rows(led_matrix)
#led_matrix.clear()
#fill_columns(led_matrix)

led_matrix.clear().text(2,0,"A").show()