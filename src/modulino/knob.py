from .modulino import Modulino

class ModulinoKnob(Modulino):
  
  default_addresses = [0x74, 0x76]
  
  def __init__(self, i2c_bus=None, address=None):
    super().__init__(i2c_bus, address, "ENCODER")
    self._pressed = None
    self._encoder_value = None

    # Encoder callbacks
    self._on_rotate_clockwise = None
    self._on_rotate_counter_clockwise = None
    self._on_press = None
    self._on_release = None

    # Detect bug in the set command that would make
    # the encoder value become negative after setting it to x with x != 0 
    self._set_bug_detected = False
    self.update()
    original_value = self.value
    self.value = 100    
    
    # If the value is not 100, then the set command has a bug
    if (self.value != 100):
      self._set_bug_detected = True
      self.value = -original_value
    else:
      self.value = original_value

  def update(self):
    previous_value = self._encoder_value
    previous_pressed_status = self._pressed

    data = self.read(3)
    self._pressed = data[2] != 0
    self._encoder_value = int.from_bytes(data[0:2], 'little', True)

    # Convert to signed int (16 bits), range -32768 to 32767
    if self._encoder_value >= 32768:
      self._encoder_value = self._encoder_value - 65536

    # No need to execut the callbacks after the first update
    if(previous_value == None or previous_pressed_status == None):
      return False

    has_rotated_clockwise = self._encoder_value > previous_value or (self._encoder_value == -32768 and previous_value == 32767)
    has_rotated_counter_clockwise = self._encoder_value < previous_value or (self._encoder_value == 32767 and previous_value == -32768)

    if(self._on_rotate_clockwise and has_rotated_clockwise):
      self._on_rotate_clockwise(self._encoder_value)

    if(self._on_rotate_counter_clockwise and has_rotated_counter_clockwise):
      self._on_rotate_counter_clockwise(self._encoder_value)

    if(self._on_press and self._pressed and not previous_pressed_status):
      self._on_press()

    if(self._on_release and not self._pressed and previous_pressed_status):
      self._on_release()

    return (self._encoder_value != previous_value) or (self._pressed != previous_pressed_status)

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
    if (self._set_bug_detected):
      new_value = -new_value
    buf = bytearray(4)
    buf[0:2] = new_value.to_bytes(2, 'little')
    self.write(buf)

  @property
  def pressed(self):
    return self._pressed