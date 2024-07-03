from .modulino import Modulino
from time import sleep_ms

class ModulinoBuzzer(Modulino):
  def __init__(self, i2c_bus, address=0xFF):
    self.i2c_bus = i2c_bus
    self.address = 0x1E #address
    self.name = "BUZZER"
    self.data = bytearray(8)
    self.match = [0x1E]

  def tone(self, frequency, lenght_ms):
    self.data[0:4]=frequency.to_bytes(4,'little') #index, index+len
    self.data[4:8]=lenght_ms.to_bytes(4,'little')
    self.write(self.data)

  def no_tone(self):
    self.data = bytearray(8)
    self.write(self.data)