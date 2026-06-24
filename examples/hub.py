"""
This example demonstrates how to use the Modulino Hub and Modulino Thermo 
classes to read temperature and humidity data from two sensors connected 
to different ports of the Modulino Hub.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

import time
from modulino import ModulinoHub, ModulinoThermo

print("Initializing Modulino Hub...")
hub = ModulinoHub()

# Now we can initialize the Modulino Thermo which will communicate over port 1.
# Note: It is important to initialize the thermo after selecting the port,
# as it will attempt to verify its connection on initialization.
thermo_a = ModulinoThermo(hub_port=hub.get_port(1))
thermo_b = ModulinoThermo(hub_port=hub.get_port(0))

# Wait a moment for the sensor to be ready a fter being connected to the bus
time.sleep(0.1)

print("Starting continuous temperature and humidity readings...\n")

def print_sensor_data(sensor, port):
    data = sensor.measurements
    temp = data.temperature
    hum = data.relative_humidity
    
    if temp is not None and hum is not None:
        print(f"Port {port}: Temperature: {temp:.2f} °C, Humidity: {hum:.2f} %")
    else:
        print(f"Port {port}: Failed to read data from the sensor.")

while True:
    try:
        print_sensor_data(thermo_a, 1)
        print_sensor_data(thermo_b, 0)    
    except OSError as e:
        print(f"I2C Communication error: {e}")
        
    time.sleep(1)
