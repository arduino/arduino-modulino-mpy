from .modulino import Modulino
from time import ticks_ms
from micropython import const

class ModulinoButtonsLED():
  """
  Class to interact with the LEDs of the Modulino Buttons.
  """

  def __init__(self, buttons):
    self._value = 0
    self._buttons = buttons

  def on(self):
    """ Turns the LED on. """
    self.value = 1

  def off(self):
    """ Turns the LED off. """
    self.value = 0

  @property
  def value(self):
    """ Returns the value of the LED (1 for on, 0 for off). """
    return self._value
  
  @value.setter
  def value(self, value):
    """
    Sets the value of the LED (1 for on, 0 for off).
    Calling this method will update the physical status of the LED immediately.
    """
    self._value = value
    self._buttons._update_leds()

class ModulinoButtons(Modulino):
  """
  Class to interact with the buttons of the Modulino Buttons.
  """

  default_addresses = [0x7C]
  default_long_press_duration = const(1000)

  def __init__(self, i2c_bus = None, address = None):
    """
    Initializes the Modulino Buttons.

    Parameters:
        i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
        address (int): The I2C address of the module. If not provided, the default address will be used.
    """

    super().__init__(i2c_bus, address, "Buttons")
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

    # LEDs
    self._led_a = ModulinoButtonsLED(self)
    self._led_b = ModulinoButtonsLED(self)
    self._led_c = ModulinoButtonsLED(self)
  
  @property
  def led_a(self) -> ModulinoButtonsLED:
    """ Returns the LED A object of the module. """
    return self._led_a
  
  @property
  def led_b(self) -> ModulinoButtonsLED:
    """ Returns the LED B object of the module. """
    return self._led_b
  
  @property
  def led_c(self) -> ModulinoButtonsLED:
    """ Returns the LED C object of the module. """
    return self._led_c

  def _update_leds(self):
    """
    Update the physical status of the button LEDs by writing the current values to the module.
    """
    data = bytearray(3)
    data[0] = self._led_a.value
    data[1] = self._led_b.value
    data[2] = self._led_c.value
    self.write(data)

  def set_led_status(self, a: bool, b: bool, c: bool) -> None:
    """
    Turn on or off the button LEDs according to the given status.

    Parameters:
        a (bool): The status of the LED A.
        b (bool): The status of the LED B.
        c (bool): The status of the LED C.
    """
    self._led_a._value = 1 if a else 0
    self._led_b._value = 1 if b else 0
    self._led_c._value = 1 if c else 0
    self._update_leds()

  @property
  def long_press_duration(self) -> int:
    """    
    Returns the duration in milliseconds that the button must 
    be pressed to trigger the long press event
    """
    return self._long_press_duration
  
  @long_press_duration.setter
  def long_press_duration(self, value: int) -> None:
    """
    Sets the duration in milliseconds that the button must 
    be pressed to trigger the long press event
    """
    self._long_press_duration = value

  @property
  def on_button_a_press(self):
    """
    Returns the callback for the press event of button A.    
    """
    return self._on_button_a_press
  
  @on_button_a_press.setter
  def on_button_a_press(self, value) -> None:
    """
    Sets the callback for the press event of button A.
    """
    self._on_button_a_press = value

  @property
  def on_button_a_release(self):
    """
    Returns the callback for the release event of button A.
    """
    return self._on_button_a_release
  
  @on_button_a_release.setter
  def on_button_a_release(self, value) -> None:
    """
    Sets the callback for the release event of button A.
    """
    self._on_button_a_release = value

  @property
  def on_button_a_long_press(self):
    """
    Returns the callback for the long press event of button A.
    """
    return self._on_button_a_long_press
  
  @on_button_a_long_press.setter
  def on_button_a_long_press(self, value) -> None:
    """
    Sets the callback for the long press event of button A.
    """
    self._on_button_a_long_press = value

  @property
  def on_button_b_press(self):
    """
    Returns the callback for the press event of button B.
    """
    return self._on_button_b_press
  
  @on_button_b_press.setter
  def on_button_b_press(self, value) -> None:
    """
    Sets the callback for the press event of button B.
    """
    self._on_button_b_press = value

  @property
  def on_button_b_release(self):
    """
    Returns the callback for the release event of button B.
    """
    return self._on_button_b_release
  
  @on_button_b_release.setter
  def on_button_b_release(self, value) -> None:
    """
    Sets the callback for the release event of button B.
    """
    self._on_button_b_release = value

  @property
  def on_button_b_long_press(self):
    """
    Returns the callback for the long press event of button B.
    """
    return self._on_button_b_long_press
  
  @on_button_b_long_press.setter
  def on_button_b_long_press(self, value) -> None:
    """
    Sets the callback for the long press event of button B.
    """
    self._on_button_b_long_press = value

  @property
  def on_button_c_press(self):
    """
    Returns the callback for the press event of button C.
    """
    return self._on_button_c_press
  
  @on_button_c_press.setter
  def on_button_c_press(self, value) -> None:
    """
    Sets the callback for the press event of button C.
    """
    self._on_button_c_press = value

  @property
  def on_button_c_release(self):
    """
    Returns the callback for the release event of button C.
    """
    return self._on_button_c_release
  
  @on_button_c_release.setter
  def on_button_c_release(self, value) -> None:
    """
    Sets the callback for the release event of button C.
    """
    self._on_button_c_release = value

  @property
  def on_button_c_long_press(self):
    """
    Returns the callback for the long press event of button C.
    """
    return self._on_button_c_long_press
  
  @on_button_c_long_press.setter
  def on_button_c_long_press(self, value) -> None:
    """
    Sets the callback for the long press event of button C.
    """
    self._on_button_c_long_press = value

  def update(self) -> bool:
    """
    Update the button status and call the corresponding callbacks.
    Returns True if any of the buttons has changed its state.

    Returns:
      bool: True if any of the buttons has changed its state.
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

      if(new_status[0] == 1 and previous_status[0] == 0):
        self._last_press_timestamps[0] = ticks_ms()
        if(self._on_button_a_press):
          self._on_button_a_press()
      elif(new_status[0] == 0 and previous_status[0] == 1 and self._on_button_a_release):
        self._on_button_a_release()
      
      if(new_status[1] == 1 and previous_status[1] == 0):
        self._last_press_timestamps[1] = ticks_ms()        
        if(self._on_button_b_press):
          self._on_button_b_press()
      elif(new_status[1] == 0 and previous_status[1] == 1 and self._on_button_b_release):
        self._on_button_b_release()
      
      if(new_status[2] == 1 and previous_status[2] == 0):
        self._last_press_timestamps[2] = ticks_ms()
        if(self._on_button_c_press):
          self._on_button_c_press()
      elif(new_status[2] == 0 and previous_status[2] == 1 and self._on_button_c_release):
        self._on_button_c_release()

    return button_states_changed

  def is_pressed(self, index: int) -> bool:
    """
    Returns True if the button at the given index is currently pressed.

    Parameters:
        index (int): The index of the button. A = 0, B = 1, C = 2.
    """
    return self._current_buttons_status[index]
  
  @property
  def button_a_pressed(self) -> bool:
    """
    Returns True if button A is currently pressed.
    """
    return self.is_pressed(0)
  
  @property
  def button_b_pressed(self) -> bool:
    """
    Returns True if button B is currently pressed.
    """
    return self.is_pressed(1)
  
  @property
  def button_c_pressed(self) -> bool:
    """
    Returns True if button C is currently pressed.
    """
    return self.is_pressed(2)