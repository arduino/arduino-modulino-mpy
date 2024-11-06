# Summary

* [buzzer](#modulino.buzzer)
  * [ModulinoBuzzer](#modulino.buzzer.ModulinoBuzzer)
    * [NOTES](#modulino.buzzer.ModulinoBuzzer.NOTES)
    * [\_\_init\_\_](#modulino.buzzer.ModulinoBuzzer.__init__)
    * [tone](#modulino.buzzer.ModulinoBuzzer.tone)
    * [no\_tone](#modulino.buzzer.ModulinoBuzzer.no_tone)
* [buttons](#modulino.buttons)
  * [ModulinoButtons](#modulino.buttons.ModulinoButtons)
    * [\_\_init\_\_](#modulino.buttons.ModulinoButtons.__init__)
    * [set\_led\_status](#modulino.buttons.ModulinoButtons.set_led_status)
    * [long\_press\_duration](#modulino.buttons.ModulinoButtons.long_press_duration)
    * [long\_press\_duration](#modulino.buttons.ModulinoButtons.long_press_duration)
    * [on\_button\_a\_press](#modulino.buttons.ModulinoButtons.on_button_a_press)
    * [on\_button\_a\_press](#modulino.buttons.ModulinoButtons.on_button_a_press)
    * [on\_button\_a\_release](#modulino.buttons.ModulinoButtons.on_button_a_release)
    * [on\_button\_a\_release](#modulino.buttons.ModulinoButtons.on_button_a_release)
    * [on\_button\_a\_long\_press](#modulino.buttons.ModulinoButtons.on_button_a_long_press)
    * [on\_button\_a\_long\_press](#modulino.buttons.ModulinoButtons.on_button_a_long_press)
    * [on\_button\_b\_press](#modulino.buttons.ModulinoButtons.on_button_b_press)
    * [on\_button\_b\_press](#modulino.buttons.ModulinoButtons.on_button_b_press)
    * [on\_button\_b\_release](#modulino.buttons.ModulinoButtons.on_button_b_release)
    * [on\_button\_b\_release](#modulino.buttons.ModulinoButtons.on_button_b_release)
    * [on\_button\_b\_long\_press](#modulino.buttons.ModulinoButtons.on_button_b_long_press)
    * [on\_button\_b\_long\_press](#modulino.buttons.ModulinoButtons.on_button_b_long_press)
    * [on\_button\_c\_press](#modulino.buttons.ModulinoButtons.on_button_c_press)
    * [on\_button\_c\_press](#modulino.buttons.ModulinoButtons.on_button_c_press)
    * [on\_button\_c\_release](#modulino.buttons.ModulinoButtons.on_button_c_release)
    * [on\_button\_c\_release](#modulino.buttons.ModulinoButtons.on_button_c_release)
    * [on\_button\_c\_long\_press](#modulino.buttons.ModulinoButtons.on_button_c_long_press)
    * [on\_button\_c\_long\_press](#modulino.buttons.ModulinoButtons.on_button_c_long_press)
    * [update](#modulino.buttons.ModulinoButtons.update)
    * [is\_pressed](#modulino.buttons.ModulinoButtons.is_pressed)
    * [button\_a\_pressed](#modulino.buttons.ModulinoButtons.button_a_pressed)
    * [button\_b\_pressed](#modulino.buttons.ModulinoButtons.button_b_pressed)
    * [button\_c\_pressed](#modulino.buttons.ModulinoButtons.button_c_pressed)
* [pressure](#modulino.pressure)
  * [ModulinoPressure](#modulino.pressure.ModulinoPressure)
    * [\_\_init\_\_](#modulino.pressure.ModulinoPressure.__init__)
    * [pressure](#modulino.pressure.ModulinoPressure.pressure)
    * [temperature](#modulino.pressure.ModulinoPressure.temperature)
    * [altitude](#modulino.pressure.ModulinoPressure.altitude)
* [modulino](#modulino.modulino)
  * [Modulino](#modulino.modulino.Modulino)
    * [default\_addresses](#modulino.modulino.Modulino.default_addresses)
    * [convert\_default\_addresses](#modulino.modulino.Modulino.convert_default_addresses)
    * [\_\_init\_\_](#modulino.modulino.Modulino.__init__)
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
* [distance](#modulino.distance)
  * [ModulinoDistance](#modulino.distance.ModulinoDistance)
    * [\_\_init\_\_](#modulino.distance.ModulinoDistance.__init__)
    * [distance](#modulino.distance.ModulinoDistance.distance)
* [knob](#modulino.knob)
  * [ModulinoKnob](#modulino.knob.ModulinoKnob)
    * [\_\_init\_\_](#modulino.knob.ModulinoKnob.__init__)
    * [reset](#modulino.knob.ModulinoKnob.reset)
    * [update](#modulino.knob.ModulinoKnob.update)
    * [range](#modulino.knob.ModulinoKnob.range)
    * [range](#modulino.knob.ModulinoKnob.range)
    * [on\_rotate\_clockwise](#modulino.knob.ModulinoKnob.on_rotate_clockwise)
    * [on\_rotate\_clockwise](#modulino.knob.ModulinoKnob.on_rotate_clockwise)
    * [on\_rotate\_counter\_clockwise](#modulino.knob.ModulinoKnob.on_rotate_counter_clockwise)
    * [on\_rotate\_counter\_clockwise](#modulino.knob.ModulinoKnob.on_rotate_counter_clockwise)
    * [on\_press](#modulino.knob.ModulinoKnob.on_press)
    * [on\_press](#modulino.knob.ModulinoKnob.on_press)
    * [on\_release](#modulino.knob.ModulinoKnob.on_release)
    * [on\_release](#modulino.knob.ModulinoKnob.on_release)
    * [value](#modulino.knob.ModulinoKnob.value)
    * [value](#modulino.knob.ModulinoKnob.value)
    * [pressed](#modulino.knob.ModulinoKnob.pressed)
* [pixels](#modulino.pixels)
  * [ModulinoColor](#modulino.pixels.ModulinoColor)
    * [\_\_init\_\_](#modulino.pixels.ModulinoColor.__init__)
    * [\_\_int\_\_](#modulino.pixels.ModulinoColor.__int__)
  * [ModulinoPixels](#modulino.pixels.ModulinoPixels)
    * [\_\_init\_\_](#modulino.pixels.ModulinoPixels.__init__)
    * [set\_range\_rgb](#modulino.pixels.ModulinoPixels.set_range_rgb)
    * [set\_range\_color](#modulino.pixels.ModulinoPixels.set_range_color)
    * [set\_all\_rgb](#modulino.pixels.ModulinoPixels.set_all_rgb)
    * [set\_all\_color](#modulino.pixels.ModulinoPixels.set_all_color)
    * [set\_color](#modulino.pixels.ModulinoPixels.set_color)
    * [set\_rgb](#modulino.pixels.ModulinoPixels.set_rgb)
    * [clear](#modulino.pixels.ModulinoPixels.clear)
    * [clear\_range](#modulino.pixels.ModulinoPixels.clear_range)
    * [clear\_all](#modulino.pixels.ModulinoPixels.clear_all)
    * [show](#modulino.pixels.ModulinoPixels.show)
* [movement](#modulino.movement)
  * [MovementValues](#modulino.movement.MovementValues)
  * [ModulinoMovement](#modulino.movement.ModulinoMovement)
    * [\_\_init\_\_](#modulino.movement.ModulinoMovement.__init__)
    * [accelerometer](#modulino.movement.ModulinoMovement.accelerometer)
    * [gyro](#modulino.movement.ModulinoMovement.gyro)
* [thermo](#modulino.thermo)
  * [Measurement](#modulino.thermo.Measurement)
  * [ModulinoThermo](#modulino.thermo.ModulinoThermo)
    * [\_\_init\_\_](#modulino.thermo.ModulinoThermo.__init__)
    * [measurements](#modulino.thermo.ModulinoThermo.measurements)
    * [relative\_humidity](#modulino.thermo.ModulinoThermo.relative_humidity)
    * [temperature](#modulino.thermo.ModulinoThermo.temperature)

<a id="modulino.buzzer.ModulinoBuzzer"></a>

## class `ModulinoBuzzer`

```python
class ModulinoBuzzer(Modulino)
```

Class to play tones on the piezo element of the Modulino Buzzer.
Predefined notes are available in the NOTES dictionary e.g. ModulinoBuzzer.NOTES["C4"]

<a id="modulino.buzzer.ModulinoBuzzer.NOTES"></a>

### `NOTES`

Dictionary with the notes and their corresponding frequencies.
The supported notes are defined as follows:
- B0
- C1, CS1, D1, DS1, E1, F1, FS1, G1, GS1, A1, AS1, B1
- C2, CS2, D2, DS2, E2, F2, FS2, G2, GS2, A2, AS2, B2
- C3, CS3, D3, DS3, E3, F3, FS3, G3, GS3, A3, AS3, B3
- C4, CS4, D4, DS4, E4, F4, FS4, G4, GS4, A4, AS4, B4
- C5, CS5, D5, DS5, E5, F5, FS5, G5, GS5, A5, AS5, B5
- C6, CS6, D6, DS6, E6, F6, FS6, G6, GS6, A6, AS6, B6
- C7, CS7, D7, DS7, E7, F7, FS7, G7, GS7, A7, AS7, B7
- C8, CS8, D8, DS8
- REST (Silence)

<a id="modulino.buzzer.ModulinoBuzzer.__init__"></a>

### `__init__`

```python
def __init__(i2c_bus=None, address=None)
```

Initializes the Modulino Buzzer.

**Arguments**:

- `i2c_bus` _I2C_ - The I2C bus to use. If not provided, the default I2C bus will be used.
- `address` _int_ - The I2C address of the module. If not provided, the default address will be used.

<a id="modulino.buzzer.ModulinoBuzzer.tone"></a>

### `tone`

```python
def tone(frequency: int,
         lenght_ms: int = 0xFFFF,
         blocking: bool = False) -> None
```

Plays a tone with the given frequency and duration.
If blocking is set to True, the function will wait until the tone is finished.

**Arguments**:

- `frequency` - The frequency of the tone in Hz
- `lenght_ms` - The duration of the tone in milliseconds. If omitted, the tone will play indefinitely
- `blocking` - If set to True, the function will wait until the tone is finished

<a id="modulino.buzzer.ModulinoBuzzer.no_tone"></a>

### `no_tone`

```python
def no_tone() -> None
```

Stops the current tone from playing.

<a id="modulino.buttons.ModulinoButtons"></a>

## class `ModulinoButtons`

```python
class ModulinoButtons(Modulino)
```

Class to interact with the buttons of the Modulino Buttons.

<a id="modulino.buttons.ModulinoButtons.__init__"></a>

### `__init__`

```python
def __init__(i2c_bus=None, address=None)
```

Initializes the Modulino Buttons.

**Arguments**:

- `i2c_bus` _I2C_ - The I2C bus to use. If not provided, the default I2C bus will be used.
- `address` _int_ - The I2C address of the module. If not provided, the default address will be used.

<a id="modulino.buttons.ModulinoButtons.set_led_status"></a>

### `set_led_status`

```python
def set_led_status(a: bool, b: bool, c: bool) -> None
```

Turn on or off the button LEDs according to the given status.

**Arguments**:

- `a` _bool_ - The status of the LED A.
- `b` _bool_ - The status of the LED B.
- `c` _bool_ - The status of the LED C.

<a id="modulino.buttons.ModulinoButtons.long_press_duration"></a>

### `long_press_duration`

```python
@property
def long_press_duration() -> int
```

Returns the duration in milliseconds that the button must
be pressed to trigger the long press event

<a id="modulino.buttons.ModulinoButtons.long_press_duration"></a>

### `long_press_duration`

```python
@long_press_duration.setter
def long_press_duration(value: int) -> None
```

Sets the duration in milliseconds that the button must
be pressed to trigger the long press event

<a id="modulino.buttons.ModulinoButtons.on_button_a_press"></a>

### `on_button_a_press`

```python
@property
def on_button_a_press()
```

Returns the callback for the press event of button A.

<a id="modulino.buttons.ModulinoButtons.on_button_a_press"></a>

### `on_button_a_press`

```python
@on_button_a_press.setter
def on_button_a_press(value) -> None
```

Sets the callback for the press event of button A.

<a id="modulino.buttons.ModulinoButtons.on_button_a_release"></a>

### `on_button_a_release`

```python
@property
def on_button_a_release()
```

Returns the callback for the release event of button A.

<a id="modulino.buttons.ModulinoButtons.on_button_a_release"></a>

### `on_button_a_release`

```python
@on_button_a_release.setter
def on_button_a_release(value) -> None
```

Sets the callback for the release event of button A.

<a id="modulino.buttons.ModulinoButtons.on_button_a_long_press"></a>

### `on_button_a_long_press`

```python
@property
def on_button_a_long_press()
```

Returns the callback for the long press event of button A.

<a id="modulino.buttons.ModulinoButtons.on_button_a_long_press"></a>

### `on_button_a_long_press`

```python
@on_button_a_long_press.setter
def on_button_a_long_press(value) -> None
```

Sets the callback for the long press event of button A.

<a id="modulino.buttons.ModulinoButtons.on_button_b_press"></a>

### `on_button_b_press`

```python
@property
def on_button_b_press()
```

Returns the callback for the press event of button B.

<a id="modulino.buttons.ModulinoButtons.on_button_b_press"></a>

### `on_button_b_press`

```python
@on_button_b_press.setter
def on_button_b_press(value) -> None
```

Sets the callback for the press event of button B.

<a id="modulino.buttons.ModulinoButtons.on_button_b_release"></a>

### `on_button_b_release`

```python
@property
def on_button_b_release()
```

Returns the callback for the release event of button B.

<a id="modulino.buttons.ModulinoButtons.on_button_b_release"></a>

### `on_button_b_release`

```python
@on_button_b_release.setter
def on_button_b_release(value) -> None
```

Sets the callback for the release event of button B.

<a id="modulino.buttons.ModulinoButtons.on_button_b_long_press"></a>

### `on_button_b_long_press`

```python
@property
def on_button_b_long_press()
```

Returns the callback for the long press event of button B.

<a id="modulino.buttons.ModulinoButtons.on_button_b_long_press"></a>

### `on_button_b_long_press`

```python
@on_button_b_long_press.setter
def on_button_b_long_press(value) -> None
```

Sets the callback for the long press event of button B.

<a id="modulino.buttons.ModulinoButtons.on_button_c_press"></a>

### `on_button_c_press`

```python
@property
def on_button_c_press()
```

Returns the callback for the press event of button C.

<a id="modulino.buttons.ModulinoButtons.on_button_c_press"></a>

### `on_button_c_press`

```python
@on_button_c_press.setter
def on_button_c_press(value) -> None
```

Sets the callback for the press event of button C.

<a id="modulino.buttons.ModulinoButtons.on_button_c_release"></a>

### `on_button_c_release`

```python
@property
def on_button_c_release()
```

Returns the callback for the release event of button C.

<a id="modulino.buttons.ModulinoButtons.on_button_c_release"></a>

### `on_button_c_release`

```python
@on_button_c_release.setter
def on_button_c_release(value) -> None
```

Sets the callback for the release event of button C.

<a id="modulino.buttons.ModulinoButtons.on_button_c_long_press"></a>

### `on_button_c_long_press`

```python
@property
def on_button_c_long_press()
```

Returns the callback for the long press event of button C.

<a id="modulino.buttons.ModulinoButtons.on_button_c_long_press"></a>

### `on_button_c_long_press`

```python
@on_button_c_long_press.setter
def on_button_c_long_press(value) -> None
```

Sets the callback for the long press event of button C.

<a id="modulino.buttons.ModulinoButtons.update"></a>

### `update`

```python
def update() -> bool
```

Update the button status and call the corresponding callbacks.
Returns True if any of the buttons has changed its state.

**Returns**:

- `bool` - True if any of the buttons has changed its state.

<a id="modulino.buttons.ModulinoButtons.is_pressed"></a>

### `is_pressed`

```python
def is_pressed(index: int) -> bool
```

Returns True if the button at the given index is currently pressed.

**Arguments**:

- `index` _int_ - The index of the button. A = 0, B = 1, C = 2.

<a id="modulino.buttons.ModulinoButtons.button_a_pressed"></a>

### `button_a_pressed`

```python
@property
def button_a_pressed() -> bool
```

Returns True if button A is currently pressed.

<a id="modulino.buttons.ModulinoButtons.button_b_pressed"></a>

### `button_b_pressed`

```python
@property
def button_b_pressed() -> bool
```

Returns True if button B is currently pressed.

<a id="modulino.buttons.ModulinoButtons.button_c_pressed"></a>

### `button_c_pressed`

```python
@property
def button_c_pressed() -> bool
```

Returns True if button C is currently pressed.

<a id="modulino.pressure.ModulinoPressure"></a>

## class `ModulinoPressure`

```python
class ModulinoPressure(Modulino)
```

Class to interact with the pressure sensor of the Modulino Pressure.

<a id="modulino.pressure.ModulinoPressure.__init__"></a>

### `__init__`

```python
def __init__(i2c_bus: I2C = None, address: int = None) -> None
```

Initializes the Modulino Pressure.

**Arguments**:

- `i2c_bus` _I2C_ - The I2C bus to use. If not provided, the default I2C bus will be used.
- `address` _int_ - The I2C address of the module. If not provided, the default address will be used.

<a id="modulino.pressure.ModulinoPressure.pressure"></a>

### `pressure`

```python
@property
def pressure() -> float
```

**Returns**:

- `float` - The pressure in hectopascals.

<a id="modulino.pressure.ModulinoPressure.temperature"></a>

### `temperature`

```python
@property
def temperature() -> float
```

**Returns**:

- `float` - The temperature in degrees Celsius.

<a id="modulino.pressure.ModulinoPressure.altitude"></a>

### `altitude`

```python
@property
def altitude() -> float
```

**Returns**:

- `float` - The altitude in meters.

<a id="modulino.modulino.Modulino"></a>

## class `Modulino`

```python
class Modulino()
```

Base class for all Modulino devices.

<a id="modulino.modulino.Modulino.default_addresses"></a>

### `default_addresses`

A list of default addresses that the modulino can have.
This list needs to be overridden derived classes.

<a id="modulino.modulino.Modulino.convert_default_addresses"></a>

### `convert_default_addresses`

Determines if the default addresses need to be converted from 8-bit to 7-bit.
Addresses of modulinos without native I2C modules need to be converted.
This class variable needs to be overridden in derived classes.

<a id="modulino.modulino.Modulino.__init__"></a>

### `__init__`

```python
def __init__(i2c_bus: I2C = None, address: int = None, name: str = None)
```

Initializes the Modulino object with the given i2c bus and address.
If the address is not provided, the device will try to auto discover it.
If the address is provided, the device will check if it is connected to the bus.
If the address is 8-bit, it will be converted to 7-bit.
If no bus is provided, the default bus will be used if available.

**Arguments**:

- `i2c_bus` _I2C_ - The I2C bus to use. If not provided, the default I2C bus will be used.
- `address` _int_ - The address of the device. If not provided, the device will try to auto discover it.
- `name` _str_ - The name of the device.

<a id="modulino.modulino.Modulino.discover"></a>

### `discover`

```python
def discover(default_addresses: list[int]) -> int | None
```

Tries to find the given modulino device in the device chain
based on the pre-defined default addresses. The first address found will be returned.
If the address has been changed to a custom one it won't be found with this function.

**Returns**:

  int | None: The address of the device if found, None otherwise.

<a id="modulino.modulino.Modulino.__bool__"></a>

### `__bool__`

```python
def __bool__() -> bool
```

Boolean cast operator to determine if the given i2c device has a correct address
and if the bus is defined.
In case of auto discovery this also means that the device was found on the bus
because otherwise the address would be None.

<a id="modulino.modulino.Modulino.connected"></a>

### `connected`

```python
@property
def connected() -> bool
```

Determines if the given modulino is connected to the i2c bus.

<a id="modulino.modulino.Modulino.pin_strap_address"></a>

### `pin_strap_address`

```python
@property
def pin_strap_address() -> int | None
```

Returns the pin strap i2c address of the modulino.
This address is set via resistors on the modulino board.
Since all modulinos generally use the same firmware, the pinstrap address
is needed to determine the type of the modulino at boot time, so it know what to do.
At boot it checks the internal flash in case its address has been overridden by the user
which would take precedence.

**Returns**:

  int | None: The pin strap address of the modulino.

<a id="modulino.modulino.Modulino.device_type"></a>

### `device_type`

```python
@property
def device_type() -> str | None
```

Returns the type of the modulino based on the pinstrap address as a string.

<a id="modulino.modulino.Modulino.change_address"></a>

### `change_address`

```python
def change_address(new_address: int)
```

Sets the address of the i2c device to the given value.
This is only supported on Modulinos that have a microcontroller.

<a id="modulino.modulino.Modulino.read"></a>

### `read`

```python
def read(amount_of_bytes: int) -> bytes | None
```

Reads the given amount of bytes from the i2c device and returns the data.
It skips the first byte which is the pinstrap address.

**Returns**:

  bytes | None: The data read from the device.

<a id="modulino.modulino.Modulino.write"></a>

### `write`

```python
def write(data_buffer: bytearray) -> bool
```

Writes the given buffer to the i2c device.

**Arguments**:

- `data_buffer` _bytearray_ - The data to be written to the device.
  

**Returns**:

- `bool` - True if the data was written successfully, False otherwise.

<a id="modulino.modulino.Modulino.has_default_address"></a>

### `has_default_address`

```python
@property
def has_default_address() -> bool
```

Determines if the given modulino has a default address
or if a custom one was set.

<a id="modulino.modulino.Modulino.available_devices"></a>

### `available_devices`

```python
@staticmethod
def available_devices() -> list[Modulino]
```

Finds all devices on the i2c bus and returns them as a list of Modulino objects.

**Returns**:

- `list` - A list of Modulino objects.

<a id="modulino.modulino.Modulino.reset_bus"></a>

### `reset_bus`

```python
@staticmethod
def reset_bus(i2c_bus: I2C) -> I2C
```

Resets the i2c bus. This is useful when the bus is in an unknown state.
The modulinos that are equipped with a micro controller use DMA operations.
If the host board does a reset during such operation it can make the bus get stuck.

**Returns**:

- `I2C` - A new i2c bus object after resetting the bus.

<a id="modulino.distance.ModulinoDistance"></a>

## class `ModulinoDistance`

```python
class ModulinoDistance(Modulino)
```

Class to interact with the distance sensor of the Modulino Distance.

<a id="modulino.distance.ModulinoDistance.__init__"></a>

### `__init__`

```python
def __init__(i2c_bus=None, address: int | None = None) -> None
```

Initializes the Modulino Distance.

**Arguments**:

- `i2c_bus` _I2C_ - The I2C bus to use. If not provided, the default I2C bus will be used.
- `address` _int_ - The I2C address of the module. If not provided, the default address will be used.

<a id="modulino.distance.ModulinoDistance.distance"></a>

### `distance`

```python
@property
def distance() -> int
```

**Returns**:

- `int` - The distance in centimeters.

<a id="modulino.knob.ModulinoKnob"></a>

## class `ModulinoKnob`

```python
class ModulinoKnob(Modulino)
```

Class to interact with the rotary encoder of the Modulinio Knob.

<a id="modulino.knob.ModulinoKnob.__init__"></a>

### `__init__`

```python
def __init__(i2c_bus=None, address=None)
```

Initializes the Modulino Knob.

**Arguments**:

- `i2c_bus` _I2C_ - The I2C bus to use. If not provided, the default I2C bus will be used.
- `address` _int_ - The I2C address of the module. If not provided, the default address will be used.

<a id="modulino.knob.ModulinoKnob.reset"></a>

### `reset`

```python
def reset() -> None
```

Resets the encoder value to 0.

<a id="modulino.knob.ModulinoKnob.update"></a>

### `update`

```python
def update() -> bool
```

Reads new data from the Modulino and calls the corresponding callbacks
if the encoder value or pressed status has changed.

**Returns**:

- `bool` - True if the encoder value or pressed status has changed.

<a id="modulino.knob.ModulinoKnob.range"></a>

### `range`

```python
@property
def range() -> tuple[int, int]
```

Returns the range of the encoder value.

<a id="modulino.knob.ModulinoKnob.range"></a>

### `range`

```python
@range.setter
def range(value: tuple[int, int]) -> None
```

Sets the range of the encoder value.

**Arguments**:

- `value` _tuple_ - A tuple with two integers representing the minimum and maximum values of the range.

<a id="modulino.knob.ModulinoKnob.on_rotate_clockwise"></a>

### `on_rotate_clockwise`

```python
@property
def on_rotate_clockwise()
```

Returns the callback for the rotate clockwise event.

<a id="modulino.knob.ModulinoKnob.on_rotate_clockwise"></a>

### `on_rotate_clockwise`

```python
@on_rotate_clockwise.setter
def on_rotate_clockwise(value) -> None
```

Sets the callback for the rotate clockwise event.

**Arguments**:

- `value` _function_ - The function to be called when the encoder is rotated clockwise.

<a id="modulino.knob.ModulinoKnob.on_rotate_counter_clockwise"></a>

### `on_rotate_counter_clockwise`

```python
@property
def on_rotate_counter_clockwise()
```

Returns the callback for the rotate counter clockwise event.

<a id="modulino.knob.ModulinoKnob.on_rotate_counter_clockwise"></a>

### `on_rotate_counter_clockwise`

```python
@on_rotate_counter_clockwise.setter
def on_rotate_counter_clockwise(value) -> None
```

Sets the callback for the rotate counter clockwise event.

**Arguments**:

- `value` _function_ - The function to be called when the encoder is rotated counter clockwise.

<a id="modulino.knob.ModulinoKnob.on_press"></a>

### `on_press`

```python
@property
def on_press()
```

Returns the callback for the press event.

<a id="modulino.knob.ModulinoKnob.on_press"></a>

### `on_press`

```python
@on_press.setter
def on_press(value) -> None
```

Sets the callback for the press event.

**Arguments**:

- `value` _function_ - The function to be called when the encoder is pressed.

<a id="modulino.knob.ModulinoKnob.on_release"></a>

### `on_release`

```python
@property
def on_release()
```

Returns the callback for the release event.

<a id="modulino.knob.ModulinoKnob.on_release"></a>

### `on_release`

```python
@on_release.setter
def on_release(value) -> None
```

Sets the callback for the release event.

**Arguments**:

- `value` _function_ - The function to be called when the encoder is released.

<a id="modulino.knob.ModulinoKnob.value"></a>

### `value`

```python
@property
def value() -> int
```

Returns the current value of the encoder.

<a id="modulino.knob.ModulinoKnob.value"></a>

### `value`

```python
@value.setter
def value(new_value: int) -> None
```

Sets the value of the encoder. This overrides the previous value.

**Arguments**:

- `new_value` _int_ - The new value of the encoder.

<a id="modulino.knob.ModulinoKnob.pressed"></a>

### `pressed`

```python
@property
def pressed() -> bool
```

Returns the pressed status of the encoder.

<a id="modulino.pixels.ModulinoColor"></a>

## class `ModulinoColor`

```python
class ModulinoColor()
```

Class to represent an RGB color.
It comes with predefined colors:
- RED
- GREEN
- BLUE
- YELLOW
- CYAN
- VIOLET
- WHITE

They can be accessed e.g. as ModulinoColor.RED

<a id="modulino.pixels.ModulinoColor.__init__"></a>

### `__init__`

```python
def __init__(r: int, g: int, b: int)
```

Initializes the color with the given RGB values.

**Arguments**:

- `r` _int_ - The red value of the color.
- `g` _int_ - The green value of the color.
- `b` _int_ - The blue value of the color.

<a id="modulino.pixels.ModulinoColor.__int__"></a>

### `__int__`

```python
def __int__() -> int
```

Return the 32-bit integer representation of the color.

<a id="modulino.pixels.ModulinoPixels"></a>

## class `ModulinoPixels`

```python
class ModulinoPixels(Modulino)
```

Class to interact with the LEDs of the Modulino Pixels.

<a id="modulino.pixels.ModulinoPixels.__init__"></a>

### `__init__`

```python
def __init__(i2c_bus=None, address=None)
```

Initializes the Modulino Pixels.

**Arguments**:

- `i2c_bus` _I2C_ - The I2C bus to use. If not provided, the default I2C bus will be used.
- `address` _int_ - The I2C address of the module. If not provided, the default address will be used.

<a id="modulino.pixels.ModulinoPixels.set_range_rgb"></a>

### `set_range_rgb`

```python
def set_range_rgb(index_from: int,
                  index_to: int,
                  r: int,
                  g: int,
                  b: int,
                  brightness: int = 100) -> None
```

Sets the color of the LEDs in the given range to the given RGB values.

**Arguments**:

- `index_from` _int_ - The starting index of the range.
- `index_to` _int_ - The ending index (inclusive) of the range.
- `r` _int_ - The red value of the color.
- `g` _int_ - The green value of the color.
- `b` _int_ - The blue value of the color.
- `brightness` _int_ - The brightness of the LED. It should be a value between 0 and 100.

<a id="modulino.pixels.ModulinoPixels.set_range_color"></a>

### `set_range_color`

```python
def set_range_color(index_from: int,
                    index_to: int,
                    color: ModulinoColor,
                    brightness: int = 100) -> None
```

Sets the color of the LEDs in the given range to the given color.

**Arguments**:

- `index_from` _int_ - The starting index of the range.
- `index_to` _int_ - The ending index (inclusive) of the range.
- `color` _ModulinoColor_ - The color of the LEDs.
- `brightness` _int_ - The brightness of the LED. It should be a value between 0 and 100.

<a id="modulino.pixels.ModulinoPixels.set_all_rgb"></a>

### `set_all_rgb`

```python
def set_all_rgb(r: int, g: int, b: int, brightness: int = 100) -> None
```

Sets the color of all the LEDs to the given RGB values.

**Arguments**:

- `r` _int_ - The red value of the color.
- `g` _int_ - The green value of the color.
- `b` _int_ - The blue value of the color.
- `brightness` _int_ - The brightness of the LED. It should be a value between 0 and 100.

<a id="modulino.pixels.ModulinoPixels.set_all_color"></a>

### `set_all_color`

```python
def set_all_color(color: ModulinoColor, brightness: int = 100) -> None
```

Sets the color of all the LEDs to the given color.

**Arguments**:

- `color` _ModulinoColor_ - The color of the LEDs.
- `brightness` _int_ - The brightness of the LED. It should be a value between 0 and 100.

<a id="modulino.pixels.ModulinoPixels.set_color"></a>

### `set_color`

```python
def set_color(idx: int, rgb: ModulinoColor, brightness: int = 100) -> None
```

Sets the color of the given LED index to the given color.

**Arguments**:

- `idx` _int_ - The index of the LED (0..7).
- `rgb` _ModulinoColor_ - The color of the LED.
- `brightness` _int_ - The brightness of the LED. It should be a value between 0 and 100.

<a id="modulino.pixels.ModulinoPixels.set_rgb"></a>

### `set_rgb`

```python
def set_rgb(idx: int, r: int, g: int, b: int, brightness: int = 100) -> None
```

Set the color of the given LED index to the given RGB values.

**Arguments**:

- `idx` _int_ - The index of the LED (0..7).
- `r` _int_ - The red value of the color.
- `g` _int_ - The green value of the color.
- `b` _int_ - The blue value of the color.
- `brightness` _int_ - The brightness of the LED. It should be a value between 0 and 100.

<a id="modulino.pixels.ModulinoPixels.clear"></a>

### `clear`

```python
def clear(idx: int) -> None
```

Turns off the LED at the given index.

**Arguments**:

- `idx` _int_ - The index of the LED (0..7).

<a id="modulino.pixels.ModulinoPixels.clear_range"></a>

### `clear_range`

```python
def clear_range(start: int, end: int) -> None
```

Turns off the LEDs in the given range.

**Arguments**:

- `start` _int_ - The starting index of the range.
- `end` _int_ - The ending index (inclusive) of the range.

<a id="modulino.pixels.ModulinoPixels.clear_all"></a>

### `clear_all`

```python
def clear_all() -> None
```

Turns all the LEDs off.

<a id="modulino.pixels.ModulinoPixels.show"></a>

### `show`

```python
def show() -> None
```

Applies the changes to the LEDs. This function needs to be called after any changes to the LEDs.
Otherwise, the changes will not be visible.

<a id="modulino.movement.MovementValues"></a>

### `MovementValues`

A named tuple to store the x, y, and z values of the movement sensors.

<a id="modulino.movement.ModulinoMovement"></a>

## class `ModulinoMovement`

```python
class ModulinoMovement(Modulino)
```

Class to interact with the movement sensor (IMU) of the Modulino Movement.

<a id="modulino.movement.ModulinoMovement.__init__"></a>

### `__init__`

```python
def __init__(i2c_bus=None, address: int | None = None) -> None
```

Initializes the Modulino Movement.

**Arguments**:

- `i2c_bus` _I2C_ - The I2C bus to use. If not provided, the default I2C bus will be used.
- `address` _int_ - The I2C address of the module. If not provided, the default address will be used.

<a id="modulino.movement.ModulinoMovement.accelerometer"></a>

### `accelerometer`

```python
@property
def accelerometer() -> MovementValues
```

**Returns**:

- `MovementValues` - The acceleration values in the x, y, and z axes.
  These values can be accessed as .x, .y, and .z properties
  or by using the index operator for tuple unpacking.

<a id="modulino.movement.ModulinoMovement.gyro"></a>

### `gyro`

```python
@property
def gyro() -> MovementValues
```

**Returns**:

- `MovementValues` - The gyroscope values in the x, y, and z axes.
  These values can be accessed as .x, .y, and .z properties
  or by using the index operator for tuple unpacking.

<a id="modulino.thermo.Measurement"></a>

### `Measurement`

A named tuple to store the temperature and relative humidity measurements.

<a id="modulino.thermo.ModulinoThermo"></a>

## class `ModulinoThermo`

```python
class ModulinoThermo(Modulino)
```

Class to interact with the temperature and humidity sensor of the Modulino Thermo.

<a id="modulino.thermo.ModulinoThermo.__init__"></a>

### `__init__`

```python
def __init__(i2c_bus: I2C = None, address: int = DEFAULT_ADDRESS) -> None
```

Initializes the Modulino Thermo.

**Arguments**:

- `i2c_bus` _I2C_ - The I2C bus to use. If not provided, the default I2C bus will be used.
- `address` _int_ - The I2C address of the module. If not provided, the default address will be used.

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

