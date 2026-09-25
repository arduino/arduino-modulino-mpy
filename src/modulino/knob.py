from .modulino import Modulino
import struct

class ModulinoKnob(Modulino):
  """
  Class to interact with the rotary encoder of the Modulino Knob.
  """
  
  # This module can have one of two default addresses
  # This is for a use case where two encoders are bundled together in a package
  default_addresses = [0x74, 0x76]
  
  def __init__(self, i2c_bus = None, address = None, hub_port=None, check_connection: bool = True):
    """
    Initializes the Modulino Knob.

    Parameters:
        i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
        address (int): The I2C address of the module. If not provided, the default address will be used.
        hub_port (ModulinoHubPort): The Modulino Hub port to which the device is connected.
        check_connection (bool): Whether to check the connection to the module.
    """

    super().__init__(i2c_bus, address, "Knob", check_connection=check_connection, hub_port=hub_port)
    self._read_buffer = bytearray(4) # 1 byte for pinstrap address + 2 bytes for encoder value + 1 byte for pressed status
    self._write_buffer = bytearray(4) # 2 bytes for encoder value, remaining bytes stay zero
    self._pressed: bool = None
    self._encoder_value: int = None
    self._value_range: tuple[int, int] = None

    # Encoder callbacks
    self._on_rotate_clockwise = None
    self._on_rotate_counter_clockwise = None
    self._on_press = None
    self._on_release = None

    # Detect bug in the set command that would make
    # the encoder value become negative after setting it to x with x != 0 
    self._set_bug_detected: bool = False
    self._read_data()
    original_value: int = self._encoder_value
    self.value = 100
    self._read_data()
    
    # If the value became negative, then the set command has the bug.
    # Checking for the sign rather than != 100 tolerates the knob being turned meanwhile.
    self._set_bug_detected = self._encoder_value < 0
    self.value = original_value

  @property
  def send_buffer_size(self) -> int:
    return 4

  @staticmethod
  def _get_steps(previous_value: int, current_value: int) -> int:
    """
    Calculates the number of steps the encoder has moved since the last update.
    Positive values indicate clockwise rotation, negative values counter clockwise rotation.
    Takes into account the wraparound of the signed 16-bit counter.
    """
    return ((current_value - previous_value + 32768) & 0xFFFF) - 32768

  def _read_data(self) -> None:
    """
    Reads the encoder value and pressed status from the Modulino.
    Adjusts the value to the range if it is set.
    """
    self.read(self._read_buffer)
    # Skip pinstrap address, then read a signed 16-bit value and the pressed status
    self._encoder_value, pressed = struct.unpack_from('<hB', self._read_buffer, 1)
    self._pressed = pressed != 0
    self._constrain_value()

  def _constrain_value(self) -> None:
    """
    Constrains the encoder value to the range if it is set
    and writes the constrained value back to the Modulino.
    """
    if self._value_range is None:
      return

    constrained_value: int = max(self._value_range[0], min(self._value_range[1], self._encoder_value))
    if constrained_value != self._encoder_value:
      self.value = constrained_value

  def reset(self) -> None:
    """
    Resets the encoder value to 0.
    """
    self.value = 0

  def update(self) -> bool:
    """
    Reads new data from the Modulino and calls the corresponding callbacks 
    if the encoder value or pressed status has changed.

    Returns:
        bool: True if the encoder value or pressed status has changed.
    """
    previous_value: int = self._encoder_value
    previous_pressed_status: bool = self._pressed

    self._read_data()

    # Figure out how many steps the encoder has moved since the last update
    steps: int = self._get_steps(previous_value, self._encoder_value)

    if steps > 0 and self._on_rotate_clockwise:
      self._on_rotate_clockwise(steps, self._encoder_value)
    elif steps < 0 and self._on_rotate_counter_clockwise:
      self._on_rotate_counter_clockwise(-steps, self._encoder_value)

    if self._on_press and self._pressed and not previous_pressed_status:
      self._on_press()

    if self._on_release and not self._pressed and previous_pressed_status:
      self._on_release()

    return steps != 0 or self._pressed != previous_pressed_status

  @property
  def range(self) -> tuple[int, int]:
    """
    Returns the range of the encoder value.
    """    
    return self._value_range
  
  @range.setter
  def range(self, value: tuple[int, int]) -> None:
    """
    Sets the range of the encoder value.

    Parameters:
        value (tuple): A tuple with two integers representing the minimum and maximum values of the range.
    """
    if value[0] < -32768 or value[1] > 32767:
      raise ValueError("Range must be between -32768 and 32767")

    if value[0] > value[1]:
      raise ValueError(f"Range minimum {value[0]} must not be greater than maximum {value[1]}")

    self._value_range = value
    # Adjust existing value to the new range
    self._constrain_value()

  @property
  def on_rotate_clockwise(self):
    """
    Returns the callback for the rotate clockwise event.
    """
    return self._on_rotate_clockwise
  
  @on_rotate_clockwise.setter
  def on_rotate_clockwise(self, value) -> None:
    """
    Sets the callback for the rotate clockwise event.

    Parameters:
        value (function): The function to be called when the encoder is rotated clockwise.
            It receives the number of steps and the new value as arguments.
    """
    self._on_rotate_clockwise = value

  @property
  def on_rotate_counter_clockwise(self):
    """
    Returns the callback for the rotate counter clockwise event.
    """
    return self._on_rotate_counter_clockwise
  
  @on_rotate_counter_clockwise.setter
  def on_rotate_counter_clockwise(self, value) -> None:
    """
    Sets the callback for the rotate counter clockwise event.

    Parameters:
        value (function): The function to be called when the encoder is rotated counter clockwise.
            It receives the number of steps and the new value as arguments.
    """
    self._on_rotate_counter_clockwise = value

  @property
  def on_press(self):
    """
    Returns the callback for the press event.
    """
    return self._on_press
  
  @on_press.setter
  def on_press(self, value) -> None:
    """
    Sets the callback for the press event.

    Parameters:
        value (function): The function to be called when the encoder is pressed.
    """
    self._on_press = value

  @property
  def on_release(self):
    """
    Returns the callback for the release event.
    """
    return self._on_release
  
  @on_release.setter
  def on_release(self, value) -> None:
    """
    Sets the callback for the release event.

    Parameters:
        value (function): The function to be called when the encoder is released.
    """
    self._on_release = value

  @property
  def value(self) -> int:
    """
    Returns the current value of the encoder.
    """
    return self._encoder_value

  @value.setter
  def value(self, new_value: int) -> None:
    """
    Sets the value of the encoder. This overrides the previous value.

    Parameters:
        new_value (int): The new value of the encoder.
    """
    if self._value_range is not None: 
      if new_value < self._value_range[0] or new_value > self._value_range[1]:
        raise ValueError(f"Value {new_value} is out of range ({self._value_range[0]} to {self._value_range[1]})")

    if self._set_bug_detected:
      target_value: int = -new_value
    else:
      target_value: int = new_value

    # Avoid int.to_bytes() because its signature
    # differs between MicroPython versions.
    struct.pack_into('<h', self._write_buffer, 0, target_value)

    if self.write(self._write_buffer):
      self._encoder_value = new_value

  @property
  def pressed(self) -> bool:
    """
    Returns the pressed status of the encoder.
    """
    return self._pressed