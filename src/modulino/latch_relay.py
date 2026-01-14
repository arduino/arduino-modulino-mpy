from .modulino import Modulino

class ModulinoLatchRelay(Modulino):
  """
  Class to control the relay module of the Modulino.
  """

  name = "Latch Relay"
  default_addresses = [0x4]
  receive_buffer_size: int = 3

  def __init__(self, i2c_bus=None, address=None):
    """
    Initializes the Modulino Buzzer.

    Parameters:
        i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
        address (int): The I2C address of the module. If not provided, the default address will be used.
    """
    super().__init__(i2c_bus, address, "Latch Relay")
    self._read_buffer = bytearray(3)
    self._write_buffer = bytearray(3)

  def on(self) -> None:
    """
    Turns on the relay.
    """
    self._write_buffer[0] = 1
    self.write(self._write_buffer)
    
  def off(self) -> None:
    """
    Turns off the relay.
    """
    self._write_buffer[0] = 0
    self.write(self._write_buffer)

  @property
  def is_on(self) -> bool:
    """
    Checks if the relay is currently on.
    """
    self.read(self._read_buffer)
    status = self._read_buffer[1:] # Skip pinstrap address
    if status[0] == 0 and status[1] == 0:
      return None # last status before poweroff is maintained
    
    if status[0] == 1:
        return False
    
    return True
    