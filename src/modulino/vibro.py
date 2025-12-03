from .modulino import Modulino
from time import sleep_ms

class PowerLevel:
  STOP = 0
  GENTLE = 25
  MODERATE = 35
  MEDIUM = 45
  INTENSE = 55
  POWERFUL = 65
  MAXIMUM = 75

class ModulinoVibro(Modulino):
  """
  Class to operate the vibration motor of the Modulino Vibro.
  """

  default_addresses = [0x70]

  def __init__(self, i2c_bus=None, address=None):
    """
    Initializes the Modulino Vibro.

    Parameters:
        i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
        address (int): The I2C address of the module. If not provided, the default address will be used.
    """
    super().__init__(i2c_bus, address, "Vibro")
    self.data = bytearray(12)
    self.frequency = 1000  # Default frequency in Hz
    self.off()

  def on(self, lenght_ms: int = 0xFFFF, power = PowerLevel.MEDIUM, blocking: bool = False) -> None:
    """
    Vibrates the motor for the specified duration and power level.

    Parameters:
        lenght_ms: The duration of the vibration in milliseconds. If omitted, it defaults to 65535 ms (maximum duration).
        blocking: If set to True, the function will wait until the vibration is finished.
    """    
    self.data[0:4] = self.frequency.to_bytes(4, 'little')
    self.data[4:8] = lenght_ms.to_bytes(4, 'little')
    self.data[8:12] = power.to_bytes(4, 'little')
    self.write(self.data)
    
    if blocking:
      # Subtract 5ms to accommodate for the time it takes to send the data
      sleep_ms(lenght_ms - 5)

  def off(self) -> None:
    """
    Stops the motor from vibrating.
    """
    self.data = bytearray(12)
    self.write(self.data)