# Summary

* [buttons](#modulino.buttons)
  * [ModulinoButtons](#modulino.buttons.ModulinoButtons)
    * [default\_long\_press\_duration](#modulino.buttons.ModulinoButtons.default_long_press_duration)
    * [update](#modulino.buttons.ModulinoButtons.update)
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
* [pixels](#modulino.pixels)
  * [ModulinoColor](#modulino.pixels.ModulinoColor)
    * [\_\_int\_\_](#modulino.pixels.ModulinoColor.__int__)
* [thermo](#modulino.thermo)
  * [ModulinoThermo](#modulino.thermo.ModulinoThermo)
    * [measurements](#modulino.thermo.ModulinoThermo.measurements)
    * [relative\_humidity](#modulino.thermo.ModulinoThermo.relative_humidity)
    * [temperature](#modulino.thermo.ModulinoThermo.temperature)

<a id="modulino.buttons.ModulinoButtons"></a>

## class `ModulinoButtons`

```python
class ModulinoButtons(Modulino)
```

<a id="modulino.buttons.ModulinoButtons.default_long_press_duration"></a>

### `default_long_press_duration`

1 second

<a id="modulino.buttons.ModulinoButtons.update"></a>

### `update`

```python
def update()
```

Update the button status and call the corresponding callbacks.
Returns True if any of the buttons has changed its state.

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

