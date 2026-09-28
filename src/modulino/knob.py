from .modulino import Modulino
import struct
from math import ceil

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
    self._pressed: bool = None
    self._raw_value: int = None # Hardware counter, only used to compute the steps between reads
    self._value_range: tuple[int, int] = None
    self._increment: int | float = 1

    # Encoder callbacks
    self._on_rotate_clockwise = None
    self._on_rotate_counter_clockwise = None
    self._on_press = None
    self._on_release = None

    # The value is tracked here rather than on the Modulino. This way it never needs to be
    # written to the device, which avoids glitches caused by the firmware's set command.
    self._encoder_value: int = 0
    self._read_data()

  @property
  def send_buffer_size(self) -> int:
    return 4

  @staticmethod
  def _get_steps(previous_raw_value: int, current_raw_value: int) -> int:
    """
    Calculates the number of steps between two readings of the hardware counter.
    Positive values indicate clockwise rotation, negative values counter clockwise rotation.
    Takes into account the wraparound of the signed 16-bit counter.
    """
    return ((current_raw_value - previous_raw_value + 32768) & 0xFFFF) - 32768

  def _read_data(self) -> int:
    """
    Reads the encoder counter and pressed status from the Modulino.

    Returns:
        int: The number of steps the encoder has moved since the last read.
    """
    self.read(self._read_buffer)
    # Skip pinstrap address, then read a signed 16-bit counter and the pressed status
    raw_value, pressed = struct.unpack_from('<hB', self._read_buffer, 1)
    self._pressed = pressed != 0

    steps: int = 0 if self._raw_value is None else self._get_steps(self._raw_value, raw_value)
    self._raw_value = raw_value
    return steps

  def _constrain(self, value: int) -> int:
    """
    Constrains the given value to the range if it is set.
    """
    if self._value_range is None:
      return value
    return max(self._value_range[0], min(self._value_range[1], value))

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
    previous_value: int | float = self._encoder_value
    previous_pressed_status: bool = self._pressed

    steps: int = self._read_data()
    unconstrained_value: int | float = previous_value + steps * self._increment
    self._encoder_value = self._constrain(unconstrained_value)
    change: int | float = self._encoder_value - previous_value

    if self._encoder_value == unconstrained_value:
      steps = abs(steps)
    else:
      # Only count the steps that fit into the range, so that turning past a limit doesn't trigger
      # the callbacks. Rounded up, so that a step that only partially fits still counts as one.
      # Rounding to 6 decimals first avoids float inaccuracies, e.g. 0.3 / 0.1 = 2.9999999999999996
      steps = ceil(round(abs(change) / self._increment, 6))

    if change > 0 and self._on_rotate_clockwise:
      self._on_rotate_clockwise(steps, self._encoder_value)
    elif change < 0 and self._on_rotate_counter_clockwise:
      self._on_rotate_counter_clockwise(steps, self._encoder_value)

    if self._on_press and self._pressed and not previous_pressed_status:
      self._on_press()

    if self._on_release and not self._pressed and previous_pressed_status:
      self._on_release()

    return change != 0 or self._pressed != previous_pressed_status

  @property
  def increment(self) -> int | float:
    """
    Returns the amount by which the value changes per step of the encoder.
    """
    return self._increment

  @increment.setter
  def increment(self, value: int | float) -> None:
    """
    Sets the amount by which the value changes per step of the encoder.
    If a range is set, the value still stops exactly at its limits.
    Fractional increments make the value a float, which can accumulate small
    inaccuracies for increments that floats can't represent exactly, such as 0.1.

    Parameters:
        value (int | float): A positive number. Defaults to 1.
    """
    if value <= 0:
      raise ValueError(f"Increment must be greater than 0, got {value}")

    self._increment = value

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
    if value[0] > value[1]:
      raise ValueError(f"Range minimum {value[0]} must not be greater than maximum {value[1]}")

    self._value_range = value
    # Adjust existing value to the new range
    self._encoder_value = self._constrain(self._encoder_value)

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
            It receives the number of steps turned (regardless of the increment) and the new value as arguments.
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
            It receives the number of steps turned (regardless of the increment) and the new value as arguments.
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
    The value is only stored in this object, not on the Modulino.

    Parameters:
        new_value (int): The new value of the encoder.
    """
    if self._value_range is not None: 
      if new_value < self._value_range[0] or new_value > self._value_range[1]:
        raise ValueError(f"Value {new_value} is out of range ({self._value_range[0]} to {self._value_range[1]})")

    self._encoder_value = new_value

  @property
  def pressed(self) -> bool:
    """
    Returns the pressed status of the encoder.
    """
    return self._pressed