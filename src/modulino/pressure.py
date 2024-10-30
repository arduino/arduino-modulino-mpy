from .modulino import Modulino
from lps22h import LPS22H

class ModulinoPressure(Modulino):
    """
    Class to interact with the pressure sensor of the Modulino Pressure.
    """

    # Module can have one of two default addresses
    # based on the solder jumper configuration on the board
    default_addresses = [0x5C, 0x5D]
    convert_default_addresses = False

    def __init__(self, i2c_bus=None, address: int | None = None) -> None:
        super().__init__(i2c_bus, address, "PRESSURE")
        self.sensor = LPS22H(self.i2c_bus, self.address)

    @property
    def pressure(self) -> float:
        """
        Returns:
            float: The pressure in hectopascals.
        """
        return self.sensor.pressure()
    
    @property
    def temperature(self) -> float:
        """
        Returns:
            float: The temperature in degrees Celsius.
        """
        return self.sensor.temperature()
    
    @property
    def altitude(self) -> float:
        """
        Returns:
            float: The altitude in meters.
        """
        return self.sensor.altitude()