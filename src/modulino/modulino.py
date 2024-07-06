from machine import Pin, I2C
from time import sleep
from micropython import const
import re
import os
from collections import namedtuple

I2CInterface = namedtuple('I2CInterface', ['type', 'bus_number', "scl", "sda"])

DEVICE_I2C_INTERFACES = {
    "Arduino Nano ESP32" : I2CInterface("hw", 0, None, None),
    "Arduino Portenta H7" : I2CInterface("hw", 3, None, None),
    "Arduino Portenta C33" : I2CInterface("hw", 0, None, None),
    "Generic ESP32S3 module" : I2CInterface("hw", 0, None, None),
}

class I2CHelper:
    """
    A helper class for interacting with I2C devices on supported boards.
    """
    i2c_bus = None
    frequency = const(100000) # Modulinos operate at 100kHz

    @staticmethod
    def extract_i2c_info(i2c_bus):
      bus_info = str(i2c_bus)
      # Use regex to find the values of the interface, scl, and sda
      interface_match = re.search(r'I2C\((\d+)', bus_info)
      scl_match = re.search(r'scl=(\d+)', bus_info)
      sda_match = re.search(r'sda=(\d+)', bus_info)
      
      # Extract the values if the matches are found
      interface = int(interface_match.group(1)) if interface_match else None
      scl = int(scl_match.group(1)) if scl_match else None
      sda = int(sda_match.group(1)) if sda_match else None
      
      return interface, scl, sda

    @staticmethod
    def reset_bus(i2c_bus):
      """
      Resets the I2C bus in case it got stuck. To unblock the bus the SDA line is kept high for 20 clock cycles
      Which causes the triggering of a NAK message.
      """

      # This is a workaround to get the SCL and SDA pins from a given bus object.
      # Unfortunately the I2C class does not expose those attributes directly.
      interface, scl_pin_number, sda_pin_number = I2CHelper.extract_i2c_info(i2c_bus)
      scl_pin = Pin(scl_pin_number, Pin.OUT)
      sda_pin = Pin(sda_pin_number, Pin.OUT)
      
      period = 1 / I2CHelper.frequency
      sda_pin.value(1)
      for _ in range(0, 20):
        scl_pin.value(1)
        sleep(period / 2)  # Add sleep to match the frequency
        scl_pin.value(0)
        sleep(period / 2)  # Add sleep to match the frequency
      
      # Need to re-initialize the bus after resetting it
      # otherwise it gets stuck.
      return I2C(interface, freq=I2CHelper.frequency)

    @staticmethod
    def get_interface() -> I2C:
      if(I2CHelper.i2c_bus is None):        
        I2CHelper.i2c_bus = I2CHelper.find_interface()
        I2CHelper.i2c_bus = I2CHelper.reset_bus(I2CHelper.i2c_bus)
      return I2CHelper.i2c_bus

    @staticmethod
    def find_interface() -> I2C:
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

        if interface_info.type == "hw":
            return I2C(interface_info.bus_number, freq=I2CHelper.frequency)

        if interface_info.type == "sw":
            from machine import SoftI2C, Pin
            return SoftI2C(scl=Pin(interface_info.scl) , sda=Pin(interface_info.sda), freq=I2CHelper.frequency)            

class Modulino:
  i2c_bus = None
  pinstrap_address = None # TODO what do we use this for?
  default_addresses = []
  
  def __init__(self, i2c_bus=None, address=None, name=None):
    if i2c_bus is None:
        self.i2c_bus = I2CHelper.get_interface()
    else:
        self.i2c_bus = i2c_bus

    self.address = address
    self.name = name

    if self.address == None:
      # Need to convert the 8-bit address to 7-bit
      actual_addresses = list(map(lambda addr: addr >> 1, self.default_addresses))
      self.address = self.discover(actual_addresses)

  def discover(self, default_addresses):
    """
    Tries to find the given modulino device in the device chain
    based on the pre-defined default addresses.
    If the address has been changed to a custom one it won't be found with this function.
    """
    if(len(default_addresses) == 0):
      return None
    
    devices_on_bus = self.i2c_bus.scan()
    for addr in default_addresses:
      if addr in devices_on_bus:
        return addr
      
    return None

  def __bool__(self):
    """
    Boolean cast operator to determine if the given i2c device has a correct address.
    In case of auto discovery this also means that the device was found on the bus.    
    """
    # Check if a valid i2c address is set
    return self.address <= 127 and self.address >= 0 

  def read(self, buf, howmany):
    if self.address == None:
      return False
    self.i2c_bus.writeto(self.address, bytes(1), False)
    self.i2c_bus.readfrom_into(self.address, buf, False)
    return True

  def write(self, data_buffer):
    """
    Writes the given buffer to the i2c device.
    """
    if self.address == None:
      return False
    self.i2c_bus.writeto(self.address, data_buffer)
    return True

  @property
  def has_default_address(self):
    """
    Determines if the given modulino has a default address
    or if a custom one was set.
    """
    return self.address in self.default_addresses

  @staticmethod
  def reset_bus(i2c_bus):
    """
    Resets the i2c bus. This is useful when the bus is in an unknown state. 
    The modulinos that are equipped with a micro controller use DMA operations. 
    If the host board does a reset during such operation it can make the bus get stuck. 
    
    Returns
        ----
        I2C: A new i2c bus object after resetting the bus.
    """
    return I2CHelper.reset_bus(i2c_bus)