from .modulino import Modulino
from .helpers import map_value_int

from micropython import const

class ModulinoColor:
  """
  Class to represent an RGB color.
  It comes with predefined colors:
  - RED
  - GREEN
  - BLUE
  - YELLOW
  - CYAN
  - MAGENTA
  - WHITE

  They can be accessed e.g. as ModulinoColor.RED
  """
  
  def __init__(self, r: int, g: int, b: int):
    """
    Initializes the color with the given RGB values.

    Parameters:
        r (int): The red value of the color.
        g (int): The green value of the color.
        b (int): The blue value of the color.
    """

    if r < 0 or r > 255:
      raise ValueError(f"Red value {r} should be between 0 and 255")
    if g < 0 or g > 255:
      raise ValueError(f"Green value {g} should be between 0 and 255")
    if b < 0 or b > 255:
      raise ValueError(f"Blue value {b} should be between 0 and 255")
    self.r = r
    self.g = g
    self.b = b
  
  def __int__(self) -> int:
    """
    Return the 32-bit integer representation of the color.
    Used bits: 8 to 15 for blue, 16 to 23 for green, 24 to 31 for red.
    """
    return (self.b << 8 | self.g << 16 | self.r << 24)

ModulinoColor.RED = ModulinoColor(255, 0, 0)
ModulinoColor.GREEN = ModulinoColor(0, 255, 0)
ModulinoColor.BLUE = ModulinoColor(0, 0, 255)
ModulinoColor.YELLOW = ModulinoColor(255, 255, 0)
ModulinoColor.CYAN = ModulinoColor(0, 255, 255)
ModulinoColor.MAGENTA = ModulinoColor(255, 0, 255)
ModulinoColor.WHITE = ModulinoColor(255, 255, 255)

NUM_LEDS = const(8)

class ModulinoPixels(Modulino):
  """
  Class to interact with the LEDs of the Modulino Pixels.
  """

  default_addresses = [0x6C]

  def __init__(self, i2c_bus = None, address=None):
    """
    Initializes the Modulino Pixels.

    Parameters:
        i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
        address (int): The I2C address of the module. If not provided, the default address will be used.
    """
    super().__init__(i2c_bus, address, "Pixels")
    self.clear_all()
  
  def set_range_rgb(self, index_from: int, index_to: int, r: int, g: int, b: int, brightness: int = 100) -> 'ModulinoPixels':
    """
    Sets the color of the LEDs in the given range to the given RGB values.

    Parameters:
        index_from (int): The starting index of the range.
        index_to (int): The ending index (inclusive) of the range.
        r (int): The red value of the color.
        g (int): The green value of the color.
        b (int): The blue value of the color.
        brightness (int): The brightness of the LED. It should be a value between 0 and 100.

    Returns:
        ModulinoPixels: The object itself. Allows for daisy chaining of methods.
    """
    self.set_range_color(index_from, index_to, ModulinoColor(r, g, b), brightness)
    return self

  def set_range_color(self, index_from: int, index_to: int, color: ModulinoColor, brightness: int = 100) -> 'ModulinoPixels':
    """
    Sets the color of the LEDs in the given range to the given color.

    Parameters:
        index_from (int): The starting index of the range.
        index_to (int): The ending index (inclusive) of the range.
        color (ModulinoColor): The color of the LEDs.
        brightness (int): The brightness of the LED. It should be a value between 0 and 100.

    Returns:
        ModulinoPixels: The object itself. Allows for daisy chaining of methods.
    """
    for i in range(index_from, index_to + 1):
      self.set_color(i, color, brightness)
    return self

  def set_all_rgb(self, r: int, g: int, b: int, brightness: int = 100) -> 'ModulinoPixels':
    """
    Sets the color of all the LEDs to the given RGB values.

    Parameters:
        r (int): The red value of the color.
        g (int): The green value of the color.
        b (int): The blue value of the color.
        brightness (int): The brightness of the LED. It should be a value between 0 and 100.

    Returns:
        ModulinoPixels: The object itself. Allows for daisy chaining of methods.
    """
    self.set_all_color(ModulinoColor(r, g, b), brightness)
    return self

  def set_all_color(self, color: ModulinoColor, brightness: int = 100) -> 'ModulinoPixels':
    """
    Sets the color of all the LEDs to the given color.

    Parameters:
        color (ModulinoColor): The color of the LEDs.
        brightness (int): The brightness of the LED. It should be a value between 0 and 100.

    Returns:
        ModulinoPixels: The object itself. Allows for daisy chaining of methods.
    """
    self.set_range_color(0, NUM_LEDS - 1, color, brightness)
    return self

  def set_color(self, idx: int, rgb: ModulinoColor, brightness: int = 100) -> 'ModulinoPixels':
    """
    Sets the color of the given LED index to the given color.

    Parameters:
        idx (int): The index of the LED (0..7).
        rgb (ModulinoColor): The color of the LED.
        brightness (int): The brightness of the LED. It should be a value between 0 and 100.

    Returns:
        ModulinoPixels: The object itself. Allows for daisy chaining of methods.
    """
    if idx < 0 or idx >= NUM_LEDS:
      raise ValueError(f"LED index out of range {idx} (Valid: 0..{NUM_LEDS - 1})")

    byte_index = idx * 4
    mapped_brightness = map_value_int(brightness, 0, 100, 0, 0x1f)
    color_data_bytes =  int(rgb) | mapped_brightness | 0xE0
    self.data[byte_index: byte_index+4] = color_data_bytes.to_bytes(4, 'little')
    return self

  def set_rgb(self, idx: int, r: int, g: int, b: int, brightness: int = 100) -> 'ModulinoPixels':
    """
    Set the color of the given LED index to the given RGB values.

    Parameters:
        idx (int): The index of the LED (0..7).
        r (int): The red value of the color.
        g (int): The green value of the color.
        b (int): The blue value of the color.
        brightness (int): The brightness of the LED. It should be a value between 0 and 100.

    Returns:
        ModulinoPixels: The object itself. Allows for daisy chaining of methods.
    """
    self.set_color(idx, ModulinoColor(r, g, b), brightness)
    return self

  def set_brightness(self, idx: int, brightness: int) -> 'ModulinoPixels':
    """
    Sets the brightness of the given LED index.

    Parameters:
        idx (int): The index of the LED (0..7).
        brightness (int): The brightness of the LED. It should be a value between 0 and 100.

    Returns:
        ModulinoPixels: The object itself. Allows for daisy chaining of methods.
    """
    if idx < 0 or idx >= NUM_LEDS:
      raise ValueError(f"LED index out of range {idx} (Valid: 0..{NUM_LEDS - 1})")
    
    if brightness < 0 or brightness > 100:
      raise ValueError(f"Brightness value {brightness} should be between 0 and 100")

    byte_index = (idx * 4) # The brightness is stored in the first byte of the 4-byte data (little-endian)
    mapped_brightness = map_value_int(brightness, 0, 100, 0, 0x1f) # Map to 0..31
    self.data[byte_index] = mapped_brightness | 0xE0 # Fill bits 5..7 with 1
    return self

  def set_all_brightness(self, brightness: int) -> 'ModulinoPixels':
    """
    Sets the brightness of all the LEDs.

    Parameters:
        brightness (int): The brightness of the LED. It should be a value between 0 and 100.

    Returns:
        ModulinoPixels: The object itself. Allows for daisy chaining of methods.
    """
    for i in range(NUM_LEDS):
      self.set_brightness(i, brightness)
    return self

  def clear(self, idx: int) -> 'ModulinoPixels':
    """
    Turns off the LED at the given index.

    Parameters:
        idx (int): The index of the LED (0..7).

    Returns:
        ModulinoPixels: The object itself. Allows for daisy chaining of methods.
    """
    self.set_color(idx, ModulinoColor(0, 0, 0), 0)
    return self

  def clear_range(self, start: int, end: int) -> 'ModulinoPixels':
    """
    Turns off the LEDs in the given range.

    Parameters:
        start (int): The starting index of the range.
        end (int): The ending index (inclusive) of the range.

    Returns:
        ModulinoPixels: The object itself. Allows for daisy chaining of methods.
    """
    for i in range(start, end):
        self.clear(i)
    return self
        
  def clear_all(self) -> 'ModulinoPixels':
    """
    Turns all the LEDs off.

    Returns:
        ModulinoPixels: The object itself. Allows for daisy chaining of methods.
    """
    self.data = bytearray([0xE0] * NUM_LEDS * 4)
    return self
  
  def __setitem__(self, idx: int, color: tuple | ModulinoColor) -> None:
    """
    Sets the color of the given LED index to the given color.
    This allows to use the object like an array, e.g. pixels[0] = (255, 0, 0, 50)

    Parameters:
        idx (int): The index of the LED (0..7).
        color (tuple | ModulinoColor): A tuple of three/four integers representing the RGB values (0-255) plus optional brightness (0-100). 
          Alternatively, a ModulinoColor object can be provided. 
          If None, the LED will be turned off.        
    """
    if color is None:
      self.clear(idx)
      return

    if isinstance(color, ModulinoColor):
      self.set_color(idx, color)
      return

    if not isinstance(color, tuple) or len(color) < 3:
      raise ValueError("Color must be a tuple of three or four integers representing the RGBA values.")
    brightness = 100 if len(color) == 3 else color[3]
    self.set_rgb(idx, color[0], color[1], color[2], brightness)    

  def show(self) -> None:
    """
    Applies the changes to the LEDs. This function needs to be called after any changes to the LEDs.
    Otherwise, the changes will not be visible.
    """
    self.write(self.data)
