from .modulino import Modulino

class ModulinoKnob(Modulino):
  """
  Class to interact with the rotary encoder of the Modulinio Knob.
  """
  
  # This module can have one of two default addresses
  # This is for a use case where two encoders are bundled together in a package
  default_addresses = [0x74, 0x76]
  
  def __init__(self, i2c_bus = None, address = None):
    """
    Initializes the Modulino Knob.

    Parameters:
        i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
        address (int): The I2C address of the module. If not provided, the default address will be used.
    """

    super().__init__(i2c_bus, address, "Knob")
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
    
    # If the value is not 100, then the set command has a bug
    if (self._encoder_value != 100):
      self._set_bug_detected = True
    
    self.value = original_value

    # Reset state to make sure the first update doesn't trigger the callbacks
    self._encoder_value = None
    self._pressed_status: bool = None

  def _has_rotated_clockwise(self, previous_value: int, current_value: int) -> bool:
    """
    Determines if the encoder has rotated clockwise.

    Parameters:
        previous_value (int): The previous value of the encoder.
        current_value (int): The current value of the encoder.

    Returns:
        bool: True if the encoder has rotated clockwise.
    """
    # Calculate difference considering wraparound
    diff: int = (current_value - previous_value + 65536) % 65536
    # Clockwise rotation is indicated by a positive difference less than half the range
    return 0 < diff < 32768

  def _has_rotated_counter_clockwise(self, previous_value: int, current_value: int) -> bool:
      """
      Determines if the encoder has rotated counter clockwise.

      Parameters:
          previous_value (int): The previous value of the encoder.
          current_value (int): The current value of the encoder.

      Returns:
          bool: True if the encoder has rotated counter clockwise.
      """
      # Calculate difference considering wraparound
      diff: int = (previous_value - current_value + 65536) % 65536
      # Counter-clockwise rotation is indicated by a positive difference less than half the range
      return 0 < diff < 32768

  def _get_steps(self, previous_value: int, current_value: int) -> int:
    """
    Calculates the number of steps the encoder has moved since the last update.
    """
    # Calculate difference considering wraparound
    diff: int = (current_value - previous_value + 65536) % 65536
    # Clockwise rotation is indicated by a positive difference less than half the range
    if 0 < diff < 32768:
      return diff
    # Counter-clockwise rotation is indicated by a negative difference less than half the range
    elif 32768 < diff < 65536:
      return diff - 65536
    else:
      return 0

  def _read_data(self) -> None:
    """
    Reads the encoder value and pressed status from the Modulino.
    Adjusts the value to the range if it is set.
    Converts the encoder value to a signed 16-bit integer.
    """
    data: bytes = self.read(3)
    self._pressed = data[2] != 0
    self._encoder_value = int.from_bytes(data[0:2], 'little', True)

    # Convert to signed int (16 bits), range -32768 to 32767
    if self._encoder_value >= 32768:
      self._encoder_value = self._encoder_value - 65536

    if self._value_range is not None:
      # Constrain the value to the range self._value_range[0] to self._value_range[1]
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

    # No need to execut the callbacks after the first update
    if previous_value is None or previous_pressed_status is None:
      return False

    has_rotated_clockwise: bool = self._has_rotated_clockwise(previous_value, self._encoder_value)
    has_rotated_counter_clockwise: bool = self._has_rotated_counter_clockwise(previous_value, self._encoder_value)

    # Figure out how many steps the encoder has moved since the last update
    steps: int = self._get_steps(previous_value, self._encoder_value)

    if self._on_rotate_clockwise and has_rotated_clockwise:
      self._on_rotate_clockwise(steps, self._encoder_value)

    if self._on_rotate_counter_clockwise and has_rotated_counter_clockwise:
      self._on_rotate_counter_clockwise(steps, self._encoder_value)

    if self._on_press and self._pressed and not previous_pressed_status:
      self._on_press()

    if self._on_release and not self._pressed and previous_pressed_status:
      self._on_release()

    return (self._encoder_value != previous_value) or (self._pressed != previous_pressed_status)

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

    self._value_range = value

    if self.value is None:
      return

    # Adjust existing value to the new range
    if self.value < self._value_range[0]:
      self.value = self._value_range[0]
    elif self.value > self._value_range[1]:
      self.value = self._value_range[1]

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

    buf: bytearray = bytearray(4)
    buf[0:2] = target_value.to_bytes(2, 'little')

    if self.write(buf):
      self._encoder_value = new_value

  @property
  def pressed(self) -> bool:
    """
    Returns the pressed status of the encoder.
    """
    return self._pressed