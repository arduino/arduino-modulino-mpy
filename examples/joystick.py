"""
This example demonstrates how to use the ModulinoJoystick class to read 
joystick coordinates and handle button events.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoJoystick

joystick = ModulinoJoystick()
joystick.on_button_press = lambda: print("Button pressed")
joystick.on_button_release = lambda: print("Button released")
joystick.on_button_long_press = lambda: print("Button long pressed")

while True:
    state_changed = joystick.update()
    if state_changed:
        print(f"Joystick position: x={joystick.x}, y={joystick.y}")
        # print("Button pressed:", joystick.button_pressed)