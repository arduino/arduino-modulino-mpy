# 📖 Documentation

## 💻 Usage

To use this library you can import the `modulino` module along with the desired classes which give you access to the different modulinos. For example:

```python
from modulino import ModulinoPixels

pixels = ModulinoPixels()
```
Once the desired object is obtained you can call functions and query properties on these objects such as `pixels.set_all_rgb(255, 0, 0)`.

## ℹ️ Using 3rd Party Boards

When using this library on a non-Arduino board, the I2C bus must be initialized manually.
Usually the available I2C buses are predefined and can be accessed by their number, e.g. I2C(0).
If not, the pins for SDA and SCL must be specified. An example on how to do this can be found [here](../examples/third_party_board.py).

## 🕹️🕹️ Using multiple Modulinos of the same type

When using multiple Modulinos of the same type, you can create separate instances for each one by specifying different I2C addresses. For that to work, make sure to change their I2C address to a unique one by running the `change_address.py` script in the examples folder. This only works for Modulino models that support changing the I2C address (e.g., ModulinoButtons, ModulinoBuzzer, ModulinoKnob, ModulinoPixels).

```python
from modulino import ModulinoButtons

buttons1 = ModulinoButtons(address=0x10)
buttons2 = ModulinoButtons(address=0x11)

print("Button A on Modulino 1 is pressed:", buttons1.button_a_pressed)
print("Button A on Modulino 2 is pressed:", buttons2.button_a_pressed)
```

## 👀 Examples

The following scripts are examples of how to use the Modulinos with Python:

- [buttons.py](../examples/buttons.py): This example shows how to use the ModulinoButtons class to interact with the buttons of the Modulino.
- [buzzer.py](../examples/buzzer.py): This example shows how to use the ModulinoBuzzer class to play a melody using the buzzer of the Modulino.
- [distance.py](../examples/distance.py): This example shows how to use the ModulinoDistance class to read the distance from the Time of Flight sensor of the Modulino.
- [knob.py](../examples/knob.py): This example shows how to use the ModulinoKnob class to read the value of a rotary encoder knob.
- [knob_buzzer.py](../examples/knob_buzzer.py): This example demonstrates how to use the ModulinoKnob and ModulinoBuzzer classes to play different notes using a buzzer.
- [knob_pixels.py](../examples/knob_pixels.py): This example shows how to use the ModulinoKnob and ModulinoPixels classes to control a set of pixels with a knob.
- [movement.py](../examples/movement.py): This example shows how to use the ModulinoMovement class to read the accelerometer 
and gyroscope values from the Modulino.
- [pixels.py](../examples/pixels.py): This example shows how to use the ModulinoPixels class to control a set of pixels.
- [pixels_thermo.py](../examples/pixels_thermo.py): This example shows how to use the ModulinoPixels and ModulinoThermo classes to display the temperature on a pixel strip.
temperature and altitude from the Modulino.
- [thermo.py](../examples/thermo.py): This example shows how to use the ModulinoThermo class to read the temperature and humidity from the Modulino.