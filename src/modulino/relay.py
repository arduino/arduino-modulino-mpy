from .modulino import Modulino
from time import sleep_ms

class ModulinoRelay(Modulino):
  """
  Class to control the relay module of the Modulino.
  """

  default_addresses = [0x28]

  def __init__(self, i2c_bus=None, address=None):
    """
    Initializes the Modulino Buzzer.

    Parameters:
        i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
        address (int): The I2C address of the module. If not provided, the default address will be used.
    """
    super().__init__(i2c_bus, address, "Relay")
    self.data = bytearray(3)
    self.off()

  def on(self) -> None:
    """
    Turns on the relay.
    """
    self.data[0] = 1
    self.write(self.data)
    
  def off(self) -> None:
    """
    Turns off the relay.
    """
    self.data[0] = 0
    self.write(self.data)

  @property
  def is_on(self) -> bool:
    """
    Checks if the relay is currently on.
    """
    status = self.read(3)
    return status[0] == 1