# Getting started

## Installation

### Arduino MicroPython Package Installer (recommended)

The easiest way to install the library is the
[Arduino MicroPython Package Installer](https://labs.arduino.cc/en/labs/micropython-package-installer),
available for macOS, Windows and Linux.

1. [Download the installer](https://github.com/arduino/lab-micropython-package-installer/releases/latest) for your operating system and launch it.
2. Connect your board and select it in the installer.
3. Search for **Modulino** and click *Install*.

### mpremote

You can also install the package from the command line with [mpremote and mip](https://docs.micropython.org/en/latest/reference/packages.html#packages):

```bash
mpremote mip install github:arduino/modulino-mpy
```

### Development setup

For development, clone the repository, mount the `src` folder on the board and run an example:

```bash
mpremote connect mount src run ./examples/pixels.py
```

If your board isn't detected automatically, pass its serial number, which you can find with `mpremote connect list`:

```bash
mpremote connect id:387784598440 mount src run ./examples/pixels.py
```

To pick an example interactively, run `python run_examples.py`.

## Usage

Import the `modulino` module along with the classes for the Modulinos you want to use:

```python
from modulino import ModulinoPixels

pixels = ModulinoPixels()
pixels.set_all_rgb(255, 0, 0).show()
```

Once you have an object you can call its methods and query its properties.
Each Modulino has its own page with the full API and examples. See the navigation on the left.

## Using 3rd party boards

On non-Arduino boards the I2C bus must be initialized manually.
Usually the available I2C buses are predefined and can be accessed by their number:

```python
from machine import I2C
from modulino import ModulinoPixels

pixels = ModulinoPixels(I2C(0))
```

If not, the pins for SDA and SCL must be specified:

??? example "third_party_board.py"

    ```python
    --8<-- "examples/third_party_board.py"
    ```

## Using multiple Modulinos of the same type

### Changing the I2C address

You can create separate instances for each Modulino by giving them unique I2C addresses.
Change the address with the `change_address.py` script below. This only works for Modulinos
that have a microcontroller (e.g. Buttons, Buzzer, Knob, Pixels).

```python
from modulino import ModulinoButtons

buttons1 = ModulinoButtons(address=0x10)
buttons2 = ModulinoButtons(address=0x11)

print("Button A on Modulino 1 is pressed:", buttons1.button_a_pressed)
print("Button A on Modulino 2 is pressed:", buttons2.button_a_pressed)
```

??? example "change_address.py"

    ```python
    --8<-- "examples/change_address.py"
    ```

### Using a Modulino Hub

Alternatively, a [Modulino Hub](modulinos/hub.md) connects multiple Modulinos of the same type
without changing their addresses. Pass the port to the constructor with `hub_port`:

```python
from modulino import ModulinoHub, ModulinoButtons

hub = ModulinoHub()
buttons_a = ModulinoButtons(hub_port=hub.get_port(0))
buttons_b = ModulinoButtons(hub_port=hub.get_port(1))
```

## Updating the firmware

Modulinos with a microcontroller can be updated over I2C using their built-in bootloader.

??? example "firmware_update.py"

    ```python
    --8<-- "examples/firmware_update.py"
    ```
