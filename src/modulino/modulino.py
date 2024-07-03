from machine import Pin

class Modulino:
  i2c_bus = None
  
  def __init__(self, i2c_bus, address=0xFF, name=""):
    self.i2c_bus = i2c_bus
    self.address = address
    self.name = name
    self.pinstrap_address = None

  def begin(self):
    if self.address == 0xFF:
      self.address = self.discover() >> 1

  def discover(self):
    return 0xFF

  def __bool__(self):
    return self.address != 0xFF

  def read(self, buf, howmany):
    if self.address == 0xFF:
      return False
    self.i2c_bus.writeto(self.address, bytes(1), False)
    self.i2c_bus.readfrom_into(self.address, buf, False)
    return True

  def write(self, buf):
    # print(buf)
    if self.address == 0xFF:
      return False
    self.i2c_bus.writeto(self.address, buf)
    return True

  def non_default_address(self):
    return self.pinstrap_address != self.address

  def scan(self, addr):
    try:
      addr = addr >> 1
      self.i2c_bus.writeto(addr, bytes(0))
      return True
    except OSError:
      return False

  @staticmethod
  def reset_bus():
    sda_dummy = Pin(43, Pin.OUT)
    scl_dummy = Pin(44, Pin.OUT)
    sda_dummy.value(1)
    for clk in range(0, 20):
      scl_dummy.value(1)
      scl_dummy.value(0)
    