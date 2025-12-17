from modulino import Modulino

class ModulinoLEDMatrix(Modulino):
  """
  Class to control the LED Matrix module of the Modulino.
  """

  default_addresses = [0x72]

  def __init__(self, i2c_bus=None, address=None):
    """
    Initializes the Modulino LED Matrix.

    Parameters:
        i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
        address (int): The I2C address of the module. If not provided, the default address will be used.
    """
    super().__init__(i2c_bus, address, "LED Matrix")
    self._buffer = bytearray(12) # 96 bits = 96 LEDs (8 rows x 12 columns)

  def set_pixel(self, x, y, value):
    """
    Sets the state of a specific pixel in the LED matrix.

    Parameters:
        x (int): The x-coordinate of the pixel (0-11).
        y (int): The y-coordinate of the pixel (0-7).
        value (bool): True to turn the pixel on, False to turn it off.
    """
    if not (0 <= x < 12 and 0 <= y < 8):
        raise ValueError("Pixel coordinates out of bounds")
    
    index = y * 12 + x
    byte_index = index // 8
    bit_index = index % 8

    if value:
        self._buffer[byte_index] |= (1 << bit_index)
    else:
        self._buffer[byte_index] &= ~(1 << bit_index)
    
    return self

  def clear(self):
    """
    Clears the LED matrix by turning off all pixels.
    """
    self._buffer = bytearray(12)
    return self

  def show(self):
    """
    Sends the current buffer to the LED matrix to update the display.
    """
    self.write(self._buffer)

if __name__ == "__main__":
    from time import sleep_ms
    led_matrix = ModulinoLEDMatrix()
    led_matrix.clear().show()

    for y in range(8):
        for x in range(12):
            led_matrix.set_pixel(x, y, True)  # Checkerboard pattern
            led_matrix.show()
            sleep_ms(100)
