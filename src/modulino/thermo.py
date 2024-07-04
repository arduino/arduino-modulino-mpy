from time import sleep
from micropython import const
from collections import namedtuple

# Driver from github.com/jposada202020/MicroPython_HS3003
from micropython_hs3003 import hs3003

Measurement = namedtuple('Measurement', ['temperature', 'relative_humidity'])

class ModulinoThermo():
    DEFAULT_ADDRESS = const(0x44)

    def __init__(self, i2c_bus, address: int = DEFAULT_ADDRESS) -> None:
        self._i2c_bus = i2c_bus
        self._address = address
        self._sensor = hs3003.HS3003(i2c_bus)

    @property
    def measurements(self) -> Measurement:
        """
        Return Temperature and Relative Humidity or None if the data is stalled
        """
        (temperature, humidity) = self._sensor.measurements
        
        if self._sensor._status_bit == 1:
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