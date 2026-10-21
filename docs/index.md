---
hide:
  - navigation
---

![Modulino for MicroPython](assets/library-banner.svg){ .banner }

# Modulino for MicroPython

This package lets you connect to Arduino Modulinos from MicroPython, read their data and control them.

## Installation

The easiest way to install the library is the
[Arduino MicroPython Package Installer](https://labs.arduino.cc/en/labs/micropython-package-installer).
Connect your board, search for **Modulino** and click *Install*.

Alternatively, install it from the command line with `mpremote`:

```bash
mpremote mip install github:arduino/modulino-mpy
```

## Quick start

### 1. Connect the Modulino

Plug the Modulino into your board's Qwiic connector. Boards without a Qwiic connector
need a Qwiic to Dupont cable; see [Using 3rd party boards](getting-started.md#using-3rd-party-boards).

### 2. Install the library

Install the package as described in [Installation](#installation) above.

### 3. Write your first script

Every Modulino works the same way: import its class, create an object, then read from it
or control it. This script makes a Modulino Pixels blink green:

```python
from modulino import ModulinoPixels, ModulinoColor  # (1) Import the class
from time import sleep

pixels = ModulinoPixels()  # (2) Create the object. It finds the Modulino on the I2C bus.

while True:  # (3) Control it
    pixels.set_all_color(ModulinoColor.GREEN).show()
    sleep(0.5)
    pixels.clear_all().show()
    sleep(0.5)
```

Run the script on your board using the tool or IDE of your choice, e.g.
[Arduino Lab for MicroPython](https://labs.arduino.cc/en/labs/micropython) or `mpremote`.

### 4. Next steps

Pick your Modulino below to see all its functions and more examples.
For more details, e.g. on using several Modulinos of the same type, see [Getting started](getting-started.md).

## Modulinos

<div class="grid cards" markdown>

-   [![Buttons](assets/modulinos/buttons.svg){ .card-illustration }](modulinos/buttons.md)

    **[Buttons](modulinos/buttons.md)**

    ---

    Three buttons with LEDs.

-   [![Buzzer](assets/modulinos/buzzer.svg){ .card-illustration }](modulinos/buzzer.md)

    **[Buzzer](modulinos/buzzer.md)**

    ---

    A piezo speaker.

-   [![Pixels](assets/modulinos/pixels.svg){ .card-illustration }](modulinos/pixels.md)

    **[Pixels](modulinos/pixels.md)**

    ---

    8 RGB LEDs.

-   [![Distance](assets/modulinos/distance.svg){ .card-illustration }](modulinos/distance.md)

    **[Distance](modulinos/distance.md)**

    ---

    Time-of-Flight distance sensor.

-   [![Movement](assets/modulinos/movement.svg){ .card-illustration }](modulinos/movement.md)

    **[Movement](modulinos/movement.md)**

    ---

    Acceleration, rotation and steps.

-   [![Knob](assets/modulinos/knob.svg){ .card-illustration }](modulinos/knob.md)

    **[Knob](modulinos/knob.md)**

    ---

    Rotary encoder with a button.

-   [![Thermo](assets/modulinos/thermo.svg){ .card-illustration }](modulinos/thermo.md)

    **[Thermo](modulinos/thermo.md)**

    ---

    Temperature and humidity.

-   [![Latch Relay](assets/modulinos/latch-relay.svg){ .card-illustration }](modulinos/latch-relay.md)

    **[Latch Relay](modulinos/latch-relay.md)**

    ---

    Switch devices on and off.

-   [![Joystick](assets/modulinos/joystick.svg){ .card-illustration }](modulinos/joystick.md)

    **[Joystick](modulinos/joystick.md)**

    ---

    X/Y axis and a button.

-   [![Vibro](assets/modulinos/vibro.svg){ .card-illustration }](modulinos/vibro.md)

    **[Vibro](modulinos/vibro.md)**

    ---

    A vibration motor.

-   [![LED Matrix](assets/modulinos/led-matrix.svg){ .card-illustration }](modulinos/led-matrix.md)

    **[LED Matrix](modulinos/led-matrix.md)**

    ---

    A 12×8 LED matrix.

-   [![Light](assets/modulinos/light.svg){ .card-illustration }](modulinos/light.md)

    **[Light](modulinos/light.md)**

    ---

    Lux, color and infrared light.

-   [![Motors](assets/modulinos/motors.svg){ .card-illustration }](modulinos/motors.md)

    **[Motors](modulinos/motors.md)**

    ---

    DC and stepper motors.

-   [![Hub](assets/modulinos/hub.svg){ .card-illustration }](modulinos/hub.md)

    **[Hub](modulinos/hub.md)**

    ---

    Several Modulinos of the same type.

</div>

## Supported boards

Any board that has I2C and can run a modern version of MicroPython is supported.
On Arduino boards the correct I2C interface is detected automatically. On other boards
you have to pass the I2C interface, e.g. `ModulinoPixels(I2C(0))`.
Boards without a Qwiic connector need a Qwiic to Dupont cable.
