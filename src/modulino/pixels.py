from .modulino import Modulino
from micropython import const

class ModulinoColor:
  def __init__(self, r, g, b):
    self.r = r
    self.g = g
    self.b = b
  
  def __int__(self):
    """Return the 32-bit integer representation of the color."""
    return (self.b << 8 | self.g << 16 | self.r << 24)

ModulinoColor.RED = ModulinoColor(255, 0, 0)
ModulinoColor.GREEN = ModulinoColor(0, 255, 0)
ModulinoColor.BLUE = ModulinoColor(0, 0, 255)
ModulinoColor.VIOLET = ModulinoColor(255, 0, 255)
ModulinoColor.WHITE = ModulinoColor(255, 255, 255)

NUM_LEDS = const(8)

class ModulinoPixels(Modulino):
  default_addresses = [0x6C]

  def __init__(self, i2c_bus = None, address=None):
    super().__init__(i2c_bus, address, "LEDS")
    self.clear_all()

  def map(self, x, in_min, in_max, out_min, out_max) -> int | float:
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  
  def mapi(self, x, in_min, in_max, out_min, out_max) -> int:
    return int(self.map(x, in_min, in_max, out_min, out_max)) 
  
  def set_all_rgb(self, r, g, b, brightness=100):
    for i in range(0, NUM_LEDS):
      self.set_color(i, ModulinoColor(r, g, b), brightness)

  def set_all_color(self, color, brightness=100):
    for i in range(0, NUM_LEDS):
      self.set_color(i, color, brightness)

  def set_color(self, idx, rgb, brightness=100):
    if idx < 0 or idx >= NUM_LEDS:
      raise ValueError(f"LED index out of range (0..{NUM_LEDS - 1})")

    byte_index = idx * 4
    mapped_brightness = self.mapi(brightness, 0, 100, 0, 0x1f)
    color_data_bytes =  int(rgb) | mapped_brightness | 0xE0
    self.data[byte_index: byte_index+4] = color_data_bytes.to_bytes(4, 'little')

  def set_rgb(self, idx, r, g, b, brightness=100):
    self.set_color(idx, ModulinoColor(r, g, b), brightness)

  def clear(self, idx):
    self.set_color(idx, ModulinoColor(0, 0, 0), 0)

  def clear_all(self):
    self.data = bytearray([0xE0] * NUM_LEDS * 4)

  def show(self):
    self.i2c_bus.writeto(self.address, self.data)
