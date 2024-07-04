from modulino import ModulinoPixels
from machine import SoftI2C, I2C, Pin
from time import sleep
#Module.reset_bus()

pixels = ModulinoPixels()
pixels.begin()

for index in range(0, 8):
    color_wheel_colors = [
        (255, 0, 0),
        (255, 85, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 255, 255),
        (0, 0, 255),
        (255, 0, 255),
        (255, 0, 0)
    ]
    pixels.set_rgb(index, *color_wheel_colors[index], 100)
pixels.show()
sleep(2)

pixels.set_all(255, 0, 0, 100)
pixels.show()
sleep(2)

pixels.set_all(0, 255, 0, 100)
pixels.show()
sleep(2)

pixels.set_all(0, 0, 255, 100)
pixels.show()
sleep(2)

pixels.clear_all()    
pixels.show()