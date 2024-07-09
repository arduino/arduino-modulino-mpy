from modulino import ModulinoPixels, ModulinoColor
from time import sleep

pixels = ModulinoPixels()

if not pixels.connected:
    print("🤷 No pixel modulino found")    
    exit()

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

pixels.set_all_rgb(255, 0, 0, 100)
pixels.show()
sleep(2)

pixels.set_all_color(ModulinoColor.GREEN, 100)
pixels.show()
sleep(2)

pixels.set_all_color(ModulinoColor.BLUE, 100)
pixels.show()
sleep(2)

pixels.clear_all()    
pixels.show()