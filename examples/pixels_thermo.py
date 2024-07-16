"""
Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoPixels, ModulinoThermo
from time import sleep

pixels = ModulinoPixels()
thermo_module = ModulinoThermo()

# Yellow to red scale with 8 steps in between
colors = [
    (255, 255, 0), 
    (255, 204, 0), 
    (255, 153, 0), 
    (255, 102, 0),
    (255, 51, 0), 
    (255, 0, 0), 
    (204, 0, 0), 
    (153, 0, 0)
]

# Define the range of temperatures (°C) to map to the pixel strip
temperature_range = (20, 30)

while True:
    temperature = thermo_module.temperature
    print(f"🌡️ Temperature: {temperature:.1f} °C")    

    # Constrain temperature to the given range
    if temperature < temperature_range[0]:
        temperature = temperature_range[0]
    elif temperature > temperature_range[1]:
        temperature = temperature_range[1]

    # Map temperature to the pixel strip
    # temperature_range[0]°C : 0 index -> first pixel
    # temperature_range[1]°C : 7 index -> last pixel
    temperature_index = int((temperature - temperature_range[0]) * 7 / (temperature_range[1] - temperature_range[0]))

    pixels.clear_all()

    for index in range(0, temperature_index + 1):        
        pixels.set_rgb(index, *colors[index], 100)
        
    pixels.show()
    sleep(1)