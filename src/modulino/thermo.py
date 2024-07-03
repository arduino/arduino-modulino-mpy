from time import sleep
from micropython import const
from collections import namedtuple

# Driver adapted from github.com/jposada202020/MicroPython_HS3003

Measurement = namedtuple('Measurement', ['temperature', 'relative_humidity'])

class ModulinoThermo():
    DEFAULT_ADDRESS = const(0x44)

    def __init__(self, i2c_bus, address: int = DEFAULT_ADDRESS) -> None:
        self._i2c = i2c_bus
        self._address = address
        self._status_bit = None

    @property
    def measurements(self) -> Measurement:
        """
        Return Temperature and Relative Humidity or None if the data is stalled
        """
        self._i2c.writeto(self._address, bytes([0x00]))
        sleep(0.1)  # Time to wake up the sensor
        data = bytearray(4)
        self._i2c.readfrom_into(self._address, data)

        # The Status bit will have a value of 1 when the data is stalled
        self._status_bit = data[0] & 0x40

        if self._status_bit == 1:
            return (None, None)

        msb_humidity = data[0] & 0x3F
        lsb_humidity = data[1]
        raw_humidity = msb_humidity << 8 | lsb_humidity
        humidity = (raw_humidity / (2**14.0 - 1)) * 100

        msb_temperature = data[2]
        lsb_temperature = (data[3] & 0xFC) >> 2
        raw_temperature = msb_temperature << 6 | lsb_temperature
        temperature = (raw_temperature / (2**14.0 - 1)) * 165 - 40

        return Measurement(temperature, humidity)

    @property
    def relative_humidity(self) -> float:
        """The current relative humidity in % rH"""
        return self.measurements.relative_humidity

    @property
    def temperature(self) -> float:
        """The current temperature in Celsius"""
        return self.measurements.temperature