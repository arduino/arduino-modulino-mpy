from .modulino import Modulino

class ModulinoKnob(Modulino):
  
  default_addresses = [0x74, 0x76]
  
  def __init__(self, i2c_bus=None, address=None):
    super().__init__(i2c_bus, address, "ENCODER")
    self._data = bytearray(3)
    self._pressed = False
    self._value = 0
    # Flag to detect bug in the set command that would make
    # the encoder value become negative after setting it to x with x != 0 
    self._set_bug_detected = False
    original_value = self.value
    self.value = 100    
    
    # If the value is not 100, then the set command has a bug
    if (self.value != 100):
      self._set_bug_detected = True
      self.value = -original_value
    else:
      self.value = original_value

  @property
  def value(self):
    self._data = self.read(3)
    self._pressed = self._data[2] != 0
    self._value = int.from_bytes(self._data[0:2], 'little', True)

    # Convert to signed int (16 bits)
    if self._value >= 32768:
      self._value = self._value - 65536
    return self._value

  @value.setter
  def value(self, new_value):
    if (self._set_bug_detected):
      new_value = -new_value
    buf = bytearray(4)
    buf[0:2] = new_value.to_bytes(2, 'little')
    self.write(buf)

  @property
  def pressed(self):
    return self._pressed