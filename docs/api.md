# Summary

* [buzzer](#modulino.buzzer)
  * [ModulinoBuzzer](#modulino.buzzer.ModulinoBuzzer)
    * [tone](#modulino.buzzer.ModulinoBuzzer.tone)
    * [no\_tone](#modulino.buzzer.ModulinoBuzzer.no_tone)
* [buttons](#modulino.buttons)
  * [ModulinoButtons](#modulino.buttons.ModulinoButtons)
    * [default\_long\_press\_duration](#modulino.buttons.ModulinoButtons.default_long_press_duration)
    * [set\_led\_status](#modulino.buttons.ModulinoButtons.set_led_status)
    * [update](#modulino.buttons.ModulinoButtons.update)
    * [is\_pressed](#modulino.buttons.ModulinoButtons.is_pressed)
* [modulino](#modulino.modulino)
  * [I2CHelper](#modulino.modulino.I2CHelper)
    * [frequency](#modulino.modulino.I2CHelper.frequency)
    * [reset\_bus](#modulino.modulino.I2CHelper.reset_bus)
    * [find\_interface](#modulino.modulino.I2CHelper.find_interface)
  * [Modulino](#modulino.modulino.Modulino)
    * [discover](#modulino.modulino.Modulino.discover)
    * [\_\_bool\_\_](#modulino.modulino.Modulino.__bool__)
    * [connected](#modulino.modulino.Modulino.connected)
    * [pin\_strap\_address](#modulino.modulino.Modulino.pin_strap_address)
    * [device\_type](#modulino.modulino.Modulino.device_type)
    * [change\_address](#modulino.modulino.Modulino.change_address)
    * [read](#modulino.modulino.Modulino.read)
    * [write](#modulino.modulino.Modulino.write)
    * [has\_default\_address](#modulino.modulino.Modulino.has_default_address)
    * [available\_devices](#modulino.modulino.Modulino.available_devices)
    * [reset\_bus](#modulino.modulino.Modulino.reset_bus)
* [knob](#modulino.knob)
  * [ModulinoKnob](#modulino.knob.ModulinoKnob)
    * [reset](#modulino.knob.ModulinoKnob.reset)
    * [update](#modulino.knob.ModulinoKnob.update)
    * [range](#modulino.knob.ModulinoKnob.range)
    * [on\_rotate\_clockwise](#modulino.knob.ModulinoKnob.on_rotate_clockwise)
    * [on\_rotate\_counter\_clockwise](#modulino.knob.ModulinoKnob.on_rotate_counter_clockwise)
    * [on\_press](#modulino.knob.ModulinoKnob.on_press)
    * [on\_release](#modulino.knob.ModulinoKnob.on_release)
    * [value](#modulino.knob.ModulinoKnob.value)
    * [value](#modulino.knob.ModulinoKnob.value)
    * [pressed](#modulino.knob.ModulinoKnob.pressed)
* [pixels](#modulino.pixels)
  * [ModulinoColor](#modulino.pixels.ModulinoColor)
    * [\_\_int\_\_](#modulino.pixels.ModulinoColor.__int__)
  * [ModulinoPixels](#modulino.pixels.ModulinoPixels)
    * [set\_range\_rgb](#modulino.pixels.ModulinoPixels.set_range_rgb)
    * [set\_range\_color](#modulino.pixels.ModulinoPixels.set_range_color)
    * [set\_all\_rgb](#modulino.pixels.ModulinoPixels.set_all_rgb)
    * [set\_all\_color](#modulino.pixels.ModulinoPixels.set_all_color)
    * [set\_color](#modulino.pixels.ModulinoPixels.set_color)
    * [set\_rgb](#modulino.pixels.ModulinoPixels.set_rgb)
    * [clear](#modulino.pixels.ModulinoPixels.clear)
    * [clear\_all](#modulino.pixels.ModulinoPixels.clear_all)
    * [show](#modulino.pixels.ModulinoPixels.show)
* [thermo](#modulino.thermo)
  * [ModulinoThermo](#modulino.thermo.ModulinoThermo)
    * [measurements](#modulino.thermo.ModulinoThermo.measurements)
    * [relative\_humidity](#modulino.thermo.ModulinoThermo.relative_humidity)
    * [temperature](#modulino.thermo.ModulinoThermo.temperature)

<a id="modulino.buzzer.ModulinoBuzzer"></a>

## class `ModulinoBuzzer`

```python
class ModulinoBuzzer(Modulino)
```

<a id="modulino.buzzer.ModulinoBuzzer.tone"></a>

### `tone`

```python
def tone(frequency, lenght_ms=0xFFFF, blocking=False)
```

Plays a tone with the given frequency and duration.
If blocking is set to True, the function will wait until the tone is finished.

Parameters:
    frequency: The frequency of the tone in Hz
    lenght_ms: The duration of the tone in milliseconds
    blocking: If set to True, the function will wait until the tone is finished

<a id="modulino.buzzer.ModulinoBuzzer.no_tone"></a>

### `no_tone`

```python
def no_tone()
```

Stops the current tone from playing.

<a id="modulino.buttons.ModulinoButtons"></a>

## class `ModulinoButtons`

```python
class ModulinoButtons(Modulino)
```

<a id="modulino.buttons.ModulinoButtons.default_long_press_duration"></a>

### `default_long_press_duration`

1 second

<a id="modulino.buttons.ModulinoButtons.set_led_status"></a>

### `set_led_status`

```python
def set_led_status(a, b, c)
```

Turn on or off the button LEDs according to the given status.

Parameters:
    a (bool): The status of the LED A.
  b (bool): The status of the LED B.
  c (bool): The status of the LED C.

<a id="modulino.buttons.ModulinoButtons.update"></a>

### `update`

```python
def update()
```

Update the button status and call the corresponding callbacks.
Returns True if any of the buttons has changed its state.

Returns:
  bool: True if any of the buttons has changed its state.

<a id="modulino.buttons.ModulinoButtons.is_pressed"></a>

### `is_pressed`

```python
def is_pressed(index)
```

Returns True if the button at the given index is currently pressed.

Parameters:
    index (int): The index of the button. A = 0, B = 1, C = 2.

<a id="modulino.modulino.I2CHelper"></a>

## class `I2CHelper`

```python
class I2CHelper()
```

A helper class for interacting with I2C devices on supported boards.

<a id="modulino.modulino.I2CHelper.frequency"></a>

### `frequency`

Modulinos operate at 100kHz

<a id="modulino.modulino.I2CHelper.reset_bus"></a>

### `reset_bus`

```python
@staticmethod
def reset_bus(i2c_bus)
```

Resets the I2C bus in case it got stuck. To unblock the bus the SDA line is kept high for 20 clock cycles
Which causes the triggering of a NAK message.

<a id="modulino.modulino.I2CHelper.find_interface"></a>

### `find_interface`

```python
@staticmethod
def find_interface() -> I2C
```

Returns an instance of the I2C interface for the current board.

Raises:
    RuntimeError: If the current board is not supported.

Returns:
    I2C: An instance of the I2C interface.

<a id="modulino.modulino.Modulino"></a>

## class `Modulino`

```python
class Modulino()
```

<a id="modulino.modulino.Modulino.discover"></a>

### `discover`

```python
def discover(default_addresses)
```

Tries to find the given modulino device in the device chain
based on the pre-defined default addresses.
If the address has been changed to a custom one it won't be found with this function.

<a id="modulino.modulino.Modulino.__bool__"></a>

### `__bool__`

```python
def __bool__()
```

Boolean cast operator to determine if the given i2c device has a correct address
and if the bus is defined.
In case of auto discovery this also means that the device was found on the bus
because otherwise the address would be None.

<a id="modulino.modulino.Modulino.connected"></a>

### `connected`

```python
@property
def connected()
```

Determines if the given modulino is connected to the i2c bus.

<a id="modulino.modulino.Modulino.pin_strap_address"></a>

### `pin_strap_address`

```python
@property
def pin_strap_address()
```

Returns the pin strap i2c address of the modulino.
This address is set via resistors on the modulino board.
Since all modulinos generally use the same firmware, the pinstrap address
is needed to determine the type of the modulino at boot time, so it know what to do.
At boot it checks the internal flash in case its address has been overridden by the user
which would take precedence.

<a id="modulino.modulino.Modulino.device_type"></a>

### `device_type`

```python
@property
def device_type()
```

Returns the type of the modulino based on the pinstrap address.

<a id="modulino.modulino.Modulino.change_address"></a>

### `change_address`

```python
def change_address(new_address)
```

Sets the address of the i2c device to the given value.

<a id="modulino.modulino.Modulino.read"></a>

### `read`

```python
def read(amount_of_bytes)
```

Reads the given amount of bytes from the i2c device and returns the data.
It skips the first byte which is the pinstrap address.

<a id="modulino.modulino.Modulino.write"></a>

### `write`

```python
def write(data_buffer)
```

Writes the given buffer to the i2c device.

<a id="modulino.modulino.Modulino.has_default_address"></a>

### `has_default_address`

```python
@property
def has_default_address()
```

Determines if the given modulino has a default address
or if a custom one was set.

<a id="modulino.modulino.Modulino.available_devices"></a>

### `available_devices`

```python
@staticmethod
def available_devices()
```

Finds all devices on the i2c bus and returns them as a list of Modulino objects.

Returns:
    list: A list of Modulino objects.

<a id="modulino.modulino.Modulino.reset_bus"></a>

### `reset_bus`

```python
@staticmethod
def reset_bus(i2c_bus)
```

Resets the i2c bus. This is useful when the bus is in an unknown state. 
The modulinos that are equipped with a micro controller use DMA operations. 
If the host board does a reset during such operation it can make the bus get stuck. 

Returns:
    I2C: A new i2c bus object after resetting the bus.

<a id="modulino.knob.ModulinoKnob"></a>

## class `ModulinoKnob`

```python
class ModulinoKnob(Modulino)
```

<a id="modulino.knob.ModulinoKnob.reset"></a>

### `reset`

```python
def reset()
```

Resets the encoder value to 0.

<a id="modulino.knob.ModulinoKnob.update"></a>

### `update`

```python
def update()
```

Reads new data from the Modulino and calls the corresponding callbacks 
if the encoder value or pressed status has changed.

<a id="modulino.knob.ModulinoKnob.range"></a>

### `range`

```python
@range.setter
def range(value)
```

Sets the range of the encoder value.

Parameters:
    value (tuple): A tuple with two integers representing the minimum and maximum values of the range.

<a id="modulino.knob.ModulinoKnob.on_rotate_clockwise"></a>

### `on_rotate_clockwise`

```python
@on_rotate_clockwise.setter
def on_rotate_clockwise(value)
```

Sets the callback for the rotate clockwise event.

Parameters:
    value (function): The function to be called when the encoder is rotated clockwise.

<a id="modulino.knob.ModulinoKnob.on_rotate_counter_clockwise"></a>

### `on_rotate_counter_clockwise`

```python
@on_rotate_counter_clockwise.setter
def on_rotate_counter_clockwise(value)
```

Sets the callback for the rotate counter clockwise event.

Parameters:
    value (function): The function to be called when the encoder is rotated counter clockwise.

<a id="modulino.knob.ModulinoKnob.on_press"></a>

### `on_press`

```python
@on_press.setter
def on_press(value)
```

Sets the callback for the press event.

Parameters:
    value (function): The function to be called when the encoder is pressed.

<a id="modulino.knob.ModulinoKnob.on_release"></a>

### `on_release`

```python
@on_release.setter
def on_release(value)
```

Sets the callback for the release event.

Parameters:
    value (function): The function to be called when the encoder is released.

<a id="modulino.knob.ModulinoKnob.value"></a>

### `value`

```python
@property
def value()
```

Returns the current value of the encoder.

<a id="modulino.knob.ModulinoKnob.value"></a>

### `value`

```python
@value.setter
def value(new_value)
```

Sets the value of the encoder. This overrides the previous value.

Parameters:
    new_value (int): The new value of the encoder.

<a id="modulino.knob.ModulinoKnob.pressed"></a>

### `pressed`

```python
@property
def pressed()
```

Returns the pressed status of the encoder.

<a id="modulino.pixels.ModulinoColor"></a>

## class `ModulinoColor`

```python
class ModulinoColor()
```

<a id="modulino.pixels.ModulinoColor.__int__"></a>

### `__int__`

```python
def __int__()
```

Return the 32-bit integer representation of the color.

<a id="modulino.pixels.ModulinoPixels"></a>

## class `ModulinoPixels`

```python
class ModulinoPixels(Modulino)
```

<a id="modulino.pixels.ModulinoPixels.set_range_rgb"></a>

### `set_range_rgb`

```python
def set_range_rgb(index_from, index_to, r, g, b, brightness=100)
```

Sets the color of the LEDs in the given range to the given RGB values.

Parameters:
    index_from (int): The starting index of the range.
    index_to (int): The ending index (inclusive) of the range.
    r (int): The red value of the color.
    g (int): The green value of the color.
    b (int): The blue value of the color.
    brightness (int): The brightness of the LED. It should be a value between 0 and 100.

<a id="modulino.pixels.ModulinoPixels.set_range_color"></a>

### `set_range_color`

```python
def set_range_color(index_from, index_to, color, brightness=100)
```

Sets the color of the LEDs in the given range to the given color.

Parameters:
    index_from (int): The starting index of the range.
    index_to (int): The ending index (inclusive) of the range.
    color (ModulinoColor): The color of the LEDs.
    brightness (int): The brightness of the LED. It should be a value between 0 and 100.

<a id="modulino.pixels.ModulinoPixels.set_all_rgb"></a>

### `set_all_rgb`

```python
def set_all_rgb(r, g, b, brightness=100)
```

Sets the color of all the LEDs to the given RGB values.

Parameters:
    r (int): The red value of the color.
    g (int): The green value of the color.
    b (int): The blue value of the color.
    brightness (int): The brightness of the LED. It should be a value between 0 and 100.

<a id="modulino.pixels.ModulinoPixels.set_all_color"></a>

### `set_all_color`

```python
def set_all_color(color, brightness=100)
```

Sets the color of all the LEDs to the given color.

Parameters:
    color (ModulinoColor): The color of the LEDs.
    brightness (int): The brightness of the LED. It should be a value between 0 and 100.

<a id="modulino.pixels.ModulinoPixels.set_color"></a>

### `set_color`

```python
def set_color(idx, rgb: ModulinoColor, brightness=100)
```

Sets the color of the given LED index to the given color.

Parameters:
    idx (int): The index of the LED.
    rgb (ModulinoColor): The color of the LED.
    brightness (int): The brightness of the LED. It should be a value between 0 and 100.

<a id="modulino.pixels.ModulinoPixels.set_rgb"></a>

### `set_rgb`

```python
def set_rgb(idx, r, g, b, brightness=100)
```

Set the color of the given LED index to the given RGB values.

Parameters:
    idx (int): The index of the LED.
    r (int): The red value of the color.
    g (int): The green value of the color.
    b (int): The blue value of the color.
    brightness (int): The brightness of the LED. It should be a value between 0 and 100.

<a id="modulino.pixels.ModulinoPixels.clear"></a>

### `clear`

```python
def clear(idx)
```

Turns off the LED at the given index.

Parameters:
    idx (int): The index of the LED.

<a id="modulino.pixels.ModulinoPixels.clear_all"></a>

### `clear_all`

```python
def clear_all()
```

Turns all the LEDs off.

Parameters:
    idx (int): The index of the LED

<a id="modulino.pixels.ModulinoPixels.show"></a>

### `show`

```python
def show()
```

Applies the changes to the LEDs. This function needs to be called after any changes to the LEDs.
Otherwise, the changes will not be visible.

<a id="modulino.thermo.ModulinoThermo"></a>

## class `ModulinoThermo`

```python
class ModulinoThermo(Modulino)
```

<a id="modulino.thermo.ModulinoThermo.measurements"></a>

### `measurements`

```python
@property
def measurements() -> Measurement
```

Return Temperature and Relative Humidity or None if the data is stalled

<a id="modulino.thermo.ModulinoThermo.relative_humidity"></a>

### `relative_humidity`

```python
@property
def relative_humidity() -> float
```

The current relative humidity in % rH

<a id="modulino.thermo.ModulinoThermo.temperature"></a>

### `temperature`

```python
@property
def temperature() -> float
```

The current temperature in Celsius

