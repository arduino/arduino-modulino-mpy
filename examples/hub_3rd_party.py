"""
This example shows how to use the Modulino Hub with a 3rd party I2C module.
When using a 3rd party module, a Port object needs to be retrieved and any
operation that does I2C needs to be surrounded with a "with" statement.
This ensures the Hub multiplexer routes the I2C signals to the correct port.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

import time
import ssd1306
from modulino import ModulinoHub

print("Initializing Modulino Hub...")
hub = ModulinoHub()

# The Modulino instance exposes the underlying I2C bus as `i2c_bus`
i2c = hub.i2c_bus

print("Initializing SSD1306 on Port 3...")
# Retrieve the Port object for the port where the 3rd party module is connected.
port = hub.get_port(3)

# Any I2C initialization needs to be surrounded by a "with" statement using the Port object.
with port:
    # Initialize the SSD1306 OLED display (128x64 resolution is common)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    
    # We can perform the first operations inside the context
    display.fill(0)
    display.text("Hello Modulino!", 0, 0)
    display.show()

counter = 0

while True:
    try:
        # Buffer operations (like fill, text) don't require I2C communication,
        # so they can safely run outside the with block.
        display.fill(0)
        display.text(f"Count: {counter}", 0, 20)
        
        # We need to use the `with` statement whenever actual I2C transmission happens,
        # which is exactly what display.show() does when pushing the buffer.
        with port:
            display.show()
            
        counter += 1
    except OSError as e:
        print(f"I2C Communication error: {e}")
        
    time.sleep(1)
