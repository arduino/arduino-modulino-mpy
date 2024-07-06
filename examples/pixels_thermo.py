from modulino import ModulinoPixels, ModulinoThermo
from time import sleep
#Module.reset_bus()

pixels = ModulinoPixels()
pixels.begin()
thermo_module = ModulinoThermo()
thermo_module.begin()

while True:
    # print(f"🌡️ Temperature: {thermo_module.temperature:.1f} °C")
    # print(f"💧 Humidity: {thermo_module.relative_humidity:.1f} %")    
    # print()
    sleep(2)

    # Map temperature from 25 to 30 degrees to 0 to 8 pixels
    temperature = thermo_module.temperature
    if temperature < 25:
        temperature = 25
    elif temperature > 30:
        temperature = 30
    temperature -= 25
    temperature_index = int(temperature * 8 / 5)
    print(f"Temperature: {temperature_index}")    

    for index in range(0, temperature_index):
        # Green to red scale
        colors = [
            (0, 255, 0),
            (85, 255, 0),
            (170, 255, 0),
            (255, 255, 0),
            (255, 170, 0),
            (255, 85, 0),
            (255, 0, 0),
            (255, 0, 0)
        ]
        pixels.set_rgb(index, *colors[index], 100)
    pixels.show()