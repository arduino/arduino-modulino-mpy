from .modulino import Modulino

class ModulinoKnob(Modulino):
  
  # This module can have one of two default addresses
  # This is for a use case where two encoders are bundled together in a package
  default_addresses = [0x74, 0x76]
  
  def __init__(self, i2c_bus=None, address=None):
    super().__init__(i2c_bus, address, "ENCODER")
    self._pressed = None
    self._encoder_value = None
    self._value_range = None

    # Encoder callbacks
    self._on_rotate_clockwise = None
    self._on_rotate_counter_clockwise = None
    self._on_press = None
    self._on_release = None

    # Detect bug in the set command that would make
    # the encoder value become negative after setting it to x with x != 0 
    self._set_bug_detected = False
    self._read_data()
    original_value = self._encoder_value
    self.value = 100
    self._read_data()    
    
    # If the value is not 100, then the set command has a bug
    if (self._encoder_value != 100):
      self._set_bug_detected = True
    
    self.value = original_value

    # Reset state to make sure the first update doesn't trigger the callbacks
    self._encoder_value = None
    self._pressed_status = None

  def _has_rotated_clockwise(self, previous_value, current_value):
    # Calculate difference considering wraparound
    diff = (current_value- previous_value + 65536) % 65536
    # Clockwise rotation is indicated by a positive difference less than half the range
    return 0 < diff < 32768

  def _has_rotated_counter_clockwise(self, previous_value, current_value):
      # Calculate difference considering wraparound
      diff = (previous_value - current_value+ 65536) % 65536
      # Counter-clockwise rotation is indicated by a positive difference less than half the range
      return 0 < diff < 32768

  def _get_steps(self, previous_value, current_value):
    # Calculate difference considering wraparound
    diff = (current_value - previous_value + 65536) % 65536
    # Clockwise rotation is indicated by a positive difference less than half the range
    if 0 < diff < 32768:
      return diff
    # Counter-clockwise rotation is indicated by a negative difference less than half the range
    elif 32768 < diff < 65536:
      return diff - 65536
    else:
      return 0

  def _read_data(self):
    data = self.read(3)
    self._pressed = data[2] != 0
    self._encoder_value = int.from_bytes(data[0:2], 'little', True)

    # Convert to signed int (16 bits), range -32768 to 32767
    if self._encoder_value >= 32768:
      self._encoder_value = self._encoder_value - 65536

    if(self._value_range != None):
      # Constrain the value to the range self._value_range[0] to self._value_range[1]
      constrained_value = max(self._value_range[0], min(self._value_range[1], self._encoder_value))
      
      if(constrained_value != self._encoder_value):
        self.value = constrained_value

  def reset(self):
    self.value = 0

  def update(self):
    previous_value = self._encoder_value
    previous_pressed_status = self._pressed

    self._read_data()

    # No need to execut the callbacks after the first update
    if(previous_value == None or previous_pressed_status == None):
      return False

    has_rotated_clockwise = self._has_rotated_clockwise(previous_value, self._encoder_value)
    has_rotated_counter_clockwise = self._has_rotated_counter_clockwise(previous_value, self._encoder_value)

    # Figure out how many steps the encoder has moved since the last update
    steps = self._get_steps(previous_value, self._encoder_value)

    if(self._on_rotate_clockwise and has_rotated_clockwise):
      self._on_rotate_clockwise(steps, self._encoder_value)

    if(self._on_rotate_counter_clockwise and has_rotated_counter_clockwise):
      self._on_rotate_counter_clockwise(steps, self._encoder_value)

    if(self._on_press and self._pressed and not previous_pressed_status):
      self._on_press()

    if(self._on_release and not self._pressed and previous_pressed_status):
      self._on_release()

    return (self._encoder_value != previous_value) or (self._pressed != previous_pressed_status)

  @property
  def range(self):
    return self._value_range
  
  @range.setter
  def range(self, value):
    if(value[0] < -32768 or value[1] > 32767):
      raise ValueError("Range must be between -32768 and 32767")

    self._value_range = value

    if(self.value == None):
      return

    # Adjust existing value to the new range
    if(self.value < self._value_range[0]):
      self.value = self._value_range[0]
    elif(self.value > self._value_range[1]):
      self.value = self._value_range[1]

  @property
  def on_rotate_clockwise(self):
    return self._on_rotate_clockwise
  
  @on_rotate_clockwise.setter
  def on_rotate_clockwise(self, value):
    self._on_rotate_clockwise = value

  @property
  def on_rotate_counter_clockwise(self):
    return self._on_rotate_counter_clockwise
  
  @on_rotate_counter_clockwise.setter
  def on_rotate_counter_clockwise(self, value):
    self._on_rotate_counter_clockwise = value

  @property
  def on_press(self):
    return self._on_press
  
  @on_press.setter
  def on_press(self, value):
    self._on_press = value

  @property
  def on_release(self):
    return self._on_release
  
  @on_release.setter
  def on_release(self, value):
    self._on_release = value

  @property
  def value(self):
    return self._encoder_value

  @value.setter
  def value(self, new_value):
    if(self._value_range != None): 
      if(new_value < self._value_range[0]) or (new_value > self._value_range[1]):
        raise ValueError(f"Value {new_value} is out of range ({self._value_range[0]} to {self._value_range[1]})")

    if (self._set_bug_detected):
      target_value = -new_value
    else:
      target_value = new_value

    buf = bytearray(4)
    buf[0:2] = target_value.to_bytes(2, 'little')

    if(self.write(buf)):
      self._encoder_value = new_value

  @property
  def pressed(self):
    return self._pressed