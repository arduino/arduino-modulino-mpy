from .modulino import Modulino

class ModulinoButtons(Modulino):
  def __init__(self, i2c_bus, address=0xFF):
    self.i2c_bus = i2c_bus
    self.address = 0x3E #address
    self.name = "BUTTONS"
    self.data = bytearray(3)
    self.data_butt = bytearray(3)
    self.last_status = bytearray(3)
    self.match = [0x3E]
    
  def set_leds(self, a, b, c):
    self.data[0] = a
    self.data[1] = b
    self.data[2] = c
    self.write(self.data)

  def update(self):
    self.read(self.data_butt, 3)
    #print(self.data_butt[0], self.data_butt[1], self.data_butt[2])
    res = self.data_butt and (self.data_butt[0] != self.last_status[0] or self.data_butt[1] != self.last_status[1] or self.data_butt[2] != self.last_status[2])
    self.last_status = self.data_butt
    return res

  def is_pressed(self, index):
    return self.last_status[index]