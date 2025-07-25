"""
This example shows how to use the ModulinoLight class to read the light around you.

It prints how bright the surroundings are (in lux), the color of the light as
red, green and blue values, a simple name for that color, the color temperature
in kelvin and the amount of invisible infrared light.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoLight
from time import sleep_ms

light = ModulinoLight()

while True:
    print(f"💡 Brightness: {light.lux:.1f} lux")
    print(f"🎨 Color (R, G, B): {light.rgb}")
    print(f"🌈 Color name: {light.color_name}")

    color_temperature = light.color_temperature
    if color_temperature is not None:
        print(f"🌡️ Color temperature: {color_temperature} K")

    print(f"🌌 Infrared: {light.infrared}")
    print("")
    sleep_ms(500)
