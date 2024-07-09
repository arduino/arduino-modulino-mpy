from modulino import ModulinoButtons
from sys import exit

buttons = ModulinoButtons()

if not buttons.connected:
    print("🤷 No button modulino found")    
    exit()

buttons.on_button_a_press = lambda : print("Button A pressed")
buttons.on_button_a_long_press = lambda : print("Button A long press")
buttons.on_button_a_release = lambda : print("Button A released")

buttons.on_button_b_press = lambda : print("Button B pressed")
buttons.on_button_b_long_press = lambda : print("Button B long press")
buttons.on_button_b_release = lambda : print("Button B released")

buttons.on_button_c_press = lambda : print("Button C pressed")
buttons.on_button_c_long_press = lambda : print("Button C long press")
buttons.on_button_c_release = lambda : print("Button C released")


while True:
    buttons_state_changed = buttons.update()
    
    if(buttons_state_changed):    
      led_a_status = buttons.is_pressed(0)
      led_b_status = buttons.is_pressed(1)
      led_c_status = buttons.is_pressed(2)
      buttons.set_led_status(led_a_status, led_b_status, led_c_status)