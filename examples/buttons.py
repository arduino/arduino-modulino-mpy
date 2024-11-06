"""
This example shows how to use the ModulinoButtons class to interact with the buttons of the Modulino.

The ModulinoButtons class allows you to read the state of the buttons, set the state of the LEDs, and define callbacks for the different button events.
It's necessary to call the `update()` method in each iteration of the loop to read the state of the buttons and execute the callbacks.
Use the `long_press_duration` property to set the duration in milliseconds that the button must be pressed to trigger the long press event.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoButtons
from time import sleep

buttons = ModulinoButtons()

buttons.on_button_a_press = lambda : print("Button A pressed")
buttons.on_button_a_long_press = lambda : print("Button A long press")
buttons.on_button_a_release = lambda : print("Button A released")

buttons.on_button_b_press = lambda : print("Button B pressed")
buttons.on_button_b_long_press = lambda : print("Button B long press")
buttons.on_button_b_release = lambda : print("Button B released")

buttons.on_button_c_press = lambda : print("Button C pressed")
buttons.on_button_c_long_press = lambda : print("Button C long press")
buttons.on_button_c_release = lambda : print("Button C released")

buttons.led_a.on()
sleep(0.5)
buttons.led_b.on()
sleep(0.5)
buttons.led_c.on()
sleep(0.5)
buttons.set_led_status(False, False, False) # Turn off all LEDs

while True:
    buttons_state_changed = buttons.update()
    
    if(buttons_state_changed):    
      led_a_status = buttons.is_pressed(0) # Turn LED A on if button A is pressed
      led_b_status = buttons.is_pressed(1) # Turn LED B on if button B is pressed
      led_c_status = buttons.is_pressed(2) # Turn LED C on if button C is pressed
      buttons.set_led_status(led_a_status, led_b_status, led_c_status)