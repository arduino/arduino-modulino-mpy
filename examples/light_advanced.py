"""
This example shows how to fine-tune the light sensor for more advanced use cases.

The ModulinoLight class covers the most common readings, but the sensor it uses
(an LTR-381RGB-01) can do more. You can reach it directly through the `sensor`
attribute to change settings like the gain (how much weak light is amplified)
and the integration time (how long the sensor collects light for each reading).

Higher gain and longer integration time help in dim conditions, while lower
values work better in bright environments.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoLight
from ltr381rgb import Gain, IntegrationTime
from time import sleep_ms

light = ModulinoLight()

# Access the underlying sensor for advanced configuration.
# Here we increase the gain and the integration time to read better in low light.
light.sensor.gain = Gain.X9
light.sensor.integration_time = IntegrationTime.MS200

print("🎚️ Sensor reconfigured for low-light readings")
print(f"⏱️ Integration time: {light.sensor.integration_time_ms} ms")
print("")

while True:
    print(f"💡 Brightness: {light.lux:.1f} lux")
    print(f"🎨 Color (R, G, B): {light.rgb}")
    print("")
    sleep_ms(500)
