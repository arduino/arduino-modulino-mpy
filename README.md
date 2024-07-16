# 📦 Modulino MicroPython Package

This package contains an API to connect to Arduino Modulinos, read their data and control them.

## ✨ Features

Supports the following Modulinos:

- 🔘 **Modulino Buttons**: A three-button Modulino.
- 🎵 **Modulino Buzzer**: A piezo speaker.
- 🌈 **Modulino Pixels**: Control RGB LEDs on the Modulino Pixels.
- 📏 **Modulino Distance**: Measure distance to an object.
- 🏃‍♂️ **Modulino Movement**: Measure acceleration and positioning.
- 🎛️ **Modulino Knob**: A rotating knob with a button.
- 🌡️ **Modulino Thermo**: Read surrounding temperature and humidity.

## 📖 Documentation
For more information on the features of this library and how to use them please read the documentation [here](./docs/).

## ✅ Supported Boards

Any board that has I2C and can run a modern version of MicroPython is supported. On non-Arduino boards you will have to specify the I2C interface to be used. e.g. `pixels = ModulinoPixels(I2C(0))`. On Arduino boards the correct I2C interface will be detected automatically.
On boards that don't have a Qwiic connector you will need to buy a Qwiic to Dupont cable or make your own.

## ⚙️ Installation

The easiest way is to use [mpremote and mip](https://docs.micropython.org/en/latest/reference/packages.html#packages): `mpremote mip install github:arduino/arduino-modulino-mpy`

## 🧑‍💻 Developer Installation

The easiest way is to clone the repository and then run any example using `mpremote`.
The recommended way is to mount the root directory remotely on the board and then running an example script. e.g.

```
 mpremote connect mount src run ./examples/pixels.py
```

If your board cannot be detected automatically you can try to explicitely specify the board's serial number. For example:

```
mpremote connect id:387784598440 mount src run ./examples/board_control.py
```

The specified serial number passed to the `id` attribute can be retrieved using `mpremote connect list`.
The serial number is the value in the second column.

## 🐛 Reporting Issues

If you encounter any issue, please open a bug report [here](https://github.com/arduino/arduino-modulino-mpy/issues). 

## 📕 Further Reading

- Take a look at the documentation of the [Arduino Plug and Make Kit](https://docs.arduino.cc/hardware/plug-and-make-kit/) which includes 7 selected Modulinos.

## 💪 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 🤙 Contact

For questions, comments, or feedback on this package, please create an issue on this repository.