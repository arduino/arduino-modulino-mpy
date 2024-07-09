from .modulino import Modulino

class ModulinoKnob(Modulino):
  
  default_addresses = [0x74, 0x76]
  
  def __init__(self, i2c_bus=None, address=None):
    super().__init__(i2c_bus, address, "ENCODER")
    self.data = bytearray(3)
    self._pressed = False
    self.value = 0
    self.bug_on_set = True

  def begin(self):
    val = self.get()
    self.set(100)
    if (self.get() != 100):
      self.bug_on_set = True
      self.set(-val)
    else:
      self.set(val)
    
  def get(self):
    self.data = self.read(3)
    self._pressed = self.data[2] != 0
    self.value = int.from_bytes(self.data[0:2], 'little', True)
    
    if self.value >= 32768:
      self.value = self.value - 65536
    return self.value

  def set(self, value):
    if (self.bug_on_set):
      value = -value
    buf = bytearray(4)
    buf[0:2] = value.to_bytes(2, 'little')
    self.write(buf)

  @property
  def pressed(self):
    return self._pressed