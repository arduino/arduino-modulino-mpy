from machine import Pin, I2C
import os

DEVICE_I2C_INTERFACES = {
    "Arduino Portenta H7" : { "type" : "hw", "interface" : 3 },
    "Arduino Portenta C33" : { "type" : "hw", "interface" : 0 },
    "Generic ESP32S3 module" : { "type" : "hw", "interface" : 0 },
    # "Other board" : { "type" : "sw", "scl" : "P408", "sda" : "P407" }
}

class I2CHelper:
    """
    A helper class for interacting with I2C devices on supported boards.
    """

    @staticmethod
    def get_interface() -> I2C:
        """
        Returns an instance of the I2C interface for the current board.

        Raises:
            RuntimeError: If the current board is not supported.

        Returns:
            I2C: An instance of the I2C interface.
        """
        board_name = os.uname().machine.split(' with ')[0]
        interface_info = DEVICE_I2C_INTERFACES.get(board_name, None)

        if interface_info is None:
            raise RuntimeError(f"I2C interface couldn't be determined automatically for '{board_name}'.")

        if interface_info["type"] == "hw":
            return I2C(interface_info["interface"])

        if interface_info["type"] == "sw":
            from machine import SoftI2C, Pin
            return SoftI2C(scl=Pin(interface_info["scl"]) , sda=Pin(interface_info["sda"]))            


class Modulino:
  i2c_bus = None
  
  def __init__(self, i2c_bus=None, address=0xFF, name=""):
    if i2c_bus is None:
        self.i2c_bus = I2CHelper.get_interface()
    else:
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
    