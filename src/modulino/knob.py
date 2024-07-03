from .modulino import Modulino

class ModulinoKnob(Modulino):
  
  def __init__(self, i2c_bus=None, address=0xFF):
    super().__init__(i2c_bus, 0x3A, "ENCODER")
    # self.i2c_bus = i2c_bus
    # self.address = 0x3A #address or 3E
    # self.name = "ENCODER"
    self.data = bytearray(3)
    self.match = [0x3A]
    self.pressed = False
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
    self.read(self.data, 3)
    self.pressed = self.data[2]
    self.value = (int)(self.data[0] | (self.data[1] << 8))
    if self.value >= 32768:
      self.value = self.value - 65536
    return self.value

  def set(self, value):
    if (self.bug_on_set):
      value = -value
    buf = bytearray(4)
    buf[0:2] = value.to_bytes(2, 'little')
    self.write(buf)

  def is_pressed(self):
    return self.pressed