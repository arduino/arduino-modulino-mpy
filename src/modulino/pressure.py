from .modulino import Modulino
from lps22h import LPS22H

class ModulinoPressure(Modulino):
    # Module can have one of two default addresses
    # based on the solder jumper configuration on the board
    default_addresses = [0x5C, 0x5D]
    convert_default_addresses = False

    def __init__(self, i2c_bus=None, address: int | None = None) -> None:
        super().__init__(i2c_bus, address, "PRESSURE")
        self.sensor = LPS22H(self.i2c_bus, self.address)

    @property
    def pressure(self):
        return self.sensor.pressure()
    
    @property
    def temperature(self):
        return self.sensor.temperature()
    
    @property
    def altitude(self):
        return self.sensor.altitude()