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

# TODO make them accessible
# RED = ModulinoColor(255, 0, 0)
# BLUE = ModulinoColor(0, 0, 255)
# GREEN = ModulinoColor(0, 255, 0)
# VIOLET = ModulinoColor(255, 0, 255)
# WHITE = ModulinoColor(255, 255, 255)

class ModulinoPixels(Modulino):
  NUM_LEDS = const(8)
  default_addresses = [0x6C]

  def __init__(self, i2c_bus = None, address=None):
    super().__init__(i2c_bus, address, "LEDS")
    self.clear_all()

  def map(self, x, in_min, in_max, out_min, out_max) -> int | float:
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  
  def mapi(self, x, in_min, in_max, out_min, out_max) -> int:
    return int(self.map(x, in_min, in_max, out_min, out_max)) 
  
  def set_all(self, r, g, b, brightness=25):
    for i in range(0, self.NUM_LEDS):
      self.set(i, ModulinoColor(r, g, b), brightness)

  def set(self, idx, rgb, brightness=25):
    
    if idx < 0 or idx >= self.NUM_LEDS:
      raise ValueError(f"LED index out of range (0..{self.NUM_LEDS - 1})")

    byte_index = idx * 4
    _brightness = self.mapi(brightness, 0, 100, 0, 0x1f)
    color_data_bytes =  int(rgb) | _brightness | 0xE0
    self.data[byte_index: byte_index+4] = color_data_bytes.to_bytes(4, 'little')

  def set_rgb(self, idx, r, g, b, brightness=5):
    global clr
    
    clr = ModulinoColor(r, g, b)
    self.set(idx, ModulinoColor(r, g, b), brightness)

  def clear(self, idx):
    self.set(idx, ModulinoColor(0, 0, 0), 0)

  def clear_all(self):
    self.data = bytearray([0xE0] * self.NUM_LEDS * 4)

  def show(self):
    self.i2c_bus.writeto(self.address, bytes(self.data))
