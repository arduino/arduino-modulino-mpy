from .modulino import Modulino
from time import ticks_ms
from micropython import const

class ModulinoButtons(Modulino):

  default_addresses = [0x7C]
  default_long_press_duration = const(1000) # 1 second

  def __init__(self, i2c_bus=None, address=None):
    super().__init__(i2c_bus, address, "BUTTONS")
    self.long_press_duration = self.default_long_press_duration

    self._current_buttons_status = [None, None, None]
    self._last_press_timestamps = [None, None, None]

    # Button callbacks
    self._on_button_a_press = None
    self._on_button_a_release = None
    self._on_button_b_press = None
    self._on_button_b_release = None
    self._on_button_c_press = None
    self._on_button_c_release = None
    self._on_button_a_long_press = None
    self._on_button_b_long_press = None
    self._on_button_c_long_press = None
  
  def set_led_status(self, a, b, c):
    data = bytearray(3)
    data[0] = 1 if a else 0
    data[1] = 1 if b else 0
    data[2] = 1 if c else 0
    self.write(data)

  @property
  def long_press_duration(self):
    return self._long_press_duration
  
  @long_press_duration.setter
  def long_press_duration(self, value):
    self._long_press_duration = value

  @property
  def on_button_a_press(self):
    return self._on_button_a_press
  
  @on_button_a_press.setter
  def on_button_a_press(self, value):
    self._on_button_a_press = value

  @property
  def on_button_a_release(self):
    return self._on_button_a_release
  
  @on_button_a_release.setter
  def on_button_a_release(self, value):
    self._on_button_a_release = value

  @property
  def on_button_a_long_press(self):
    return self._on_button_a_long_press
  
  @on_button_a_long_press.setter
  def on_button_a_long_press(self, value):
    self._on_button_a_long_press = value

  @property
  def on_button_b_press(self):
    return self._on_button_b_press
  
  @on_button_b_press.setter
  def on_button_b_press(self, value):
    self._on_button_b_press = value

  @property
  def on_button_b_release(self):
    return self._on_button_b_release
  
  @on_button_b_release.setter
  def on_button_b_release(self, value):
    self._on_button_b_release = value

  @property
  def on_button_b_long_press(self):
    return self._on_button_b_long_press
  
  @on_button_b_long_press.setter
  def on_button_b_long_press(self, value):
    self._on_button_b_long_press = value

  @property
  def on_button_c_press(self):
    return self._on_button_c_press
  
  @on_button_c_press.setter
  def on_button_c_press(self, value):
    self._on_button_c_press = value

  @property
  def on_button_c_release(self):
    return self._on_button_c_release
  
  @on_button_c_release.setter
  def on_button_c_release(self, value):
    self._on_button_c_release = value

  @property
  def on_button_c_long_press(self):
    return self._on_button_c_long_press
  
  @on_button_c_long_press.setter
  def on_button_c_long_press(self, value):
    self._on_button_c_long_press = value

  def update(self):
    """
    Update the button status and call the corresponding callbacks.
    Returns True if any of the buttons has changed its state.
    """
    new_status = self.read(3)
    button_states_changed = new_status != self._current_buttons_status
    previous_status = self._current_buttons_status
    current_timestamp = ticks_ms()
    
    # Update status already in case it's accessed in one of the button callbacks
    self._current_buttons_status = new_status    

    # Check for long press
    if(new_status[0] == 1 and previous_status[0] == 1 and self._last_press_timestamps[0] and current_timestamp - self._last_press_timestamps[0] > self.long_press_duration):
      self._last_press_timestamps[0] = None
      if self._on_button_a_long_press:
        self._on_button_a_long_press()

    if(new_status[1] == 1 and previous_status[1] == 1 and self._last_press_timestamps[1] and current_timestamp - self._last_press_timestamps[1] > self.long_press_duration):
      self._last_press_timestamps[1] = None
      if self._on_button_b_long_press:
        self._on_button_b_long_press()

    if(new_status[2] == 1 and previous_status[2] == 1 and self._last_press_timestamps[2] and current_timestamp - self._last_press_timestamps[2] > self.long_press_duration):
      self._last_press_timestamps[2] = None
      if self._on_button_c_long_press:
        self._on_button_c_long_press()
      
    # Check for press and release
    if(button_states_changed):

      if(new_status[0] == 1 and previous_status[0] == 0 and self._on_button_a_press):
        self._last_press_timestamps[0] = ticks_ms()
        self._on_button_a_press()
      elif(new_status[0] == 0 and previous_status[0] == 1 and self._on_button_a_release):
        self._on_button_a_release()
      
      if(new_status[1] == 1 and previous_status[1] == 0 and self._on_button_b_press):
        self._last_press_timestamps[1] = ticks_ms()        
        self._on_button_b_press()
      elif(new_status[1] == 0 and previous_status[1] == 1 and self._on_button_b_release):
        self._on_button_b_release()
      
      if(new_status[2] == 1 and previous_status[2] == 0 and self._on_button_c_press):
        self._last_press_timestamps[2] = ticks_ms()
        self._on_button_c_press()
      elif(new_status[2] == 0 and previous_status[2] == 1 and self._on_button_c_release):
        self._on_button_c_release()

    return button_states_changed

  def is_pressed(self, index):
    return self._current_buttons_status[index]