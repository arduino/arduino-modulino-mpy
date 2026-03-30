from .modulino import Modulino
from micropython import const

class ModulinoMotors(Modulino):
  """
  Class to operate the motors of the Modulino.
  """
  default_addresses = [0x48]
  MAX_SPEED = const(32767)  # Max speed value for 16-bit signed integer

  def __init__(self, i2c_bus=None, address=None, check_connection: bool = True):
    """
    Initializes the Modulino Motors.
    
    Parameters:
        i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
        address (int): The I2C address of the module. If not provided, the default address will be used.
        check_connection (bool): Whether to check the connection to the module.
    """
    super().__init__(i2c_bus, address, "Motors", check_connection=check_connection)
    self._send_buffer = bytearray(7)  # Buffer for sending commands
    self._receive_buffer = bytearray(6)  # Buffer for receiving sense data
    self._speed_a = 0
    self._invert_a = False
    self._speed_b = 0
    self._invert_b = False
    self._frequency = 1000

  def _send_command(self, msg):
    # Padding to 7 bytes to match firmware expectation
    length = len(msg)
    if length < 7:
        msg += b'\x00' * (7 - length)
    elif length > 7:
        raise ValueError(f"Message length {length} exceeds maximum of 7 bytes")
    self.write(msg)

  def _update_speed(self):
    val_a = int(self._speed_a * self.MAX_SPEED / 100) * (-1 if self._invert_a else 1)
    val_b = int(self._speed_b * self.MAX_SPEED / 100) * (-1 if self._invert_b else 1)
    
    # Command: 'S' + int16 (A) + int16 (B)
    self._send_buffer[:] = b'\x00' * len(self._send_buffer)  # Clear buffer
    self._send_buffer[0] = ord('S')
    self._send_buffer[1:3] = val_a.to_bytes(2, 'little', True)
    self._send_buffer[3:5] = val_b.to_bytes(2, 'little', True)
    self._send_command(self._send_buffer)

  @property
  def speed_a(self) -> int:
    """
    Gets or sets the speed of motor A in percentage (0-100).
    """
    return self._speed_a

  @speed_a.setter
  def speed_a(self, value: int):
    if not 0 <= value <= 100:
      raise ValueError("Speed must be between 0 and 100")
    self._speed_a = value
    self._update_speed()

  @property
  def invert_a(self) -> bool:
    """
    Gets or sets if the direction of motor A is inverted.
    """
    return self._invert_a

  @invert_a.setter
  def invert_a(self, value: bool):
    self._invert_a = value
    self._update_speed()

  @property
  def speed_b(self) -> int:
    """
    Gets or sets the speed of motor B in percentage (0-100).
    """
    return self._speed_b

  @speed_b.setter
  def speed_b(self, value: int):
    if not 0 <= value <= 100:
      raise ValueError("Speed must be between 0 and 100")
    self._speed_b = value
    self._update_speed()

  @property
  def invert_b(self) -> bool:
    """
    Gets or sets if the direction of motor B is inverted.
    """
    return self._invert_b

  @invert_b.setter
  def invert_b(self, value: bool):
    self._invert_b = value
    self._update_speed()

  def set_decay(self, decay_mode: int) -> None:
    """
    Sets the decay mode of the motors.

    Parameters:
      decay_mode (int): The decay mode to set.
    """
    self._send_command(bytes([ord('T'), decay_mode]))

  @property
  def frequency(self) -> int:
    """
    Gets or sets the frequency of the motors.
    """
    return self._frequency

  @frequency.setter
  def frequency(self, value: int):
    """Set DC Motor PWM Frequency in Hz (200 - 60000)"""
    self._frequency = value
    # Command: 'F' + uint16
    self._send_buffer[:] = b'\x00' * len(self._send_buffer)  # Clear buffer
    self._send_buffer[0] = ord('F')
    self._send_buffer[1:3] = value.to_bytes(2, 'little')
    self._send_command(self._send_buffer)

  @property
  def sense_a(self) -> int:
    """
    Gets the current sense value of motor A.

    Returns:
      int: The sense value of motor A.
    """
    return self.sense[0]

  @property
  def sense_b(self) -> int:
    """
    Gets the current sense value of motor B.

    Returns:
      int: The sense value of motor B.
    """
    return self.sense[1]

  @property
  def sense(self) -> tuple[int, int]:
    """
    Gets the current sense values of both motors.

    Returns:
      tuple[int, int]: The sense values of motor A and motor B.
    """
    self._receive_buffer[:] = b'\x00' * len(self._receive_buffer)  # Clear buffer
    self.read(self._receive_buffer)
    sense_a = int.from_bytes(self._receive_buffer[1:3], 'little')
    sense_b = int.from_bytes(self._receive_buffer[3:5], 'little')
    return sense_a, sense_b

  @property
  def send_buffer_size(self) -> int:
    return len(self._send_buffer)