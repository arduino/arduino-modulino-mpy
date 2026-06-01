import time
from modulino import ModulinoHub, ModulinoThermo

print("Initializing Modulino Hub...")
hub = ModulinoHub()

# Now we can initialize the Modulino Thermo which will communicate over port 1.
# Note: It is important to initialize the thermo after selecting the port,
# as it will attempt to verify its connection on initialization.
print("Initializing Modulino Thermo on Port 1...")
thermo_a = ModulinoThermo()

print("Initializing Modulino Thermo on Port 0...")
thermo_b = ModulinoThermo()

# Wait a moment for the sensor to be ready a fter being connected to the bus
time.sleep(0.1)

print("Starting continuous temperature and humidity readings...\n")

def print_sensor_data(thermo):
    temp = thermo.temperature
    hum = thermo.relative_humidity
    
    if temp is not None and hum is not None:
        print(f"Temperature: {temp:.2f} °C, Humidity: {hum:.2f} %")
    else:
        print("Failed to read data from the sensor.")

while True:
    try:
        hub.select_port(1)
        print_sensor_data(thermo_a)
        hub.select_port(0)
        print_sensor_data(thermo_b)    
    except OSError as e:
        print(f"I2C Communication error: {e}")
        
    time.sleep(1)
