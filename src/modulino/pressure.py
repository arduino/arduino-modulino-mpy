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

    def __init__(self, i2c_bus: I2C = None, address: int = None) -> None:
        """
        Initializes the Modulino Pressure.

        Parameters:
            i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
            address (int): The I2C address of the module. If not provided, the default address will be used.
        """
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