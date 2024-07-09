from .modulino import Modulino
from micropython import const
from collections import namedtuple

# Driver from github.com/jposada202020/MicroPython_HS3003
from micropython_hs3003 import hs3003

Measurement = namedtuple('Measurement', ['temperature', 'relative_humidity'])

class ModulinoThermo(Modulino):
    # The default I2C address of the HS3003 sensor cannot be changed by the user
    # so we can define it as a constant and avoid discovery overhead.
    DEFAULT_ADDRESS = const(0x44)

    def __init__(self, i2c_bus = None, address: int = DEFAULT_ADDRESS) -> None:
        super().__init__(i2c_bus, address, "THERMO")
        self.sensor = hs3003.HS3003(self.i2c_bus)

    @property
    def measurements(self) -> Measurement:
        """
        Return Temperature and Relative Humidity or None if the data is stalled
        """
        (temperature, humidity) = self.sensor.measurements
        
        if self.sensor._status_bit == 1:
            return Measurement(None, None)

        return Measurement(temperature, humidity)

    @property
    def relative_humidity(self) -> float:
        """The current relative humidity in % rH"""
        return self.measurements.relative_humidity

    @property
    def temperature(self) -> float:
        """The current temperature in Celsius"""
        return self.measurements.temperature