from .modulino import Modulino
from lsm6dsox import LSM6DSOX
from collections import namedtuple

MovementValues = namedtuple('MovementValues', ['x', 'y', 'z'])
"""A named tuple to store the x, y, and z values of the movement sensors."""

class ModulinoMovement(Modulino):
    """
    Class to interact with the movement sensor (IMU) of the Modulino Movement.
    """

    # Module can have one of two default addresses
    # based on the solder jumper configuration on the board
    default_addresses = [0x6A, 0x6B]
    convert_default_addresses = False

    def __init__(self, i2c_bus = None, address: int | None = None) -> None:
        """
        Initializes the Modulino Movement.

        Parameters:
            i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
            address (int): The I2C address of the module. If not provided, the default address will be used.
        """
        super().__init__(i2c_bus, address, "Movement")
        self.sensor = LSM6DSOX(self.i2c_bus, address=self.address)

    @property
    def accelerometer(self) -> MovementValues:
        """
        Returns:
            MovementValues: The acceleration values in the x, y, and z axes.
                            These values can be accessed as .x, .y, and .z properties
                            or by using the index operator for tuple unpacking.
        """
        sensor_values = self.sensor.accel()
        return MovementValues(sensor_values[0], sensor_values[1], sensor_values[2])
    
    @property
    def gyro(self) -> MovementValues:
        """
        Returns:
            MovementValues: The gyroscope values in the x, y, and z axes.
                            These values can be accessed as .x, .y, and .z properties
                            or by using the index operator for tuple unpacking.
        """
        sensor_values = self.sensor.gyro()
        return MovementValues(sensor_values[0], sensor_values[1], sensor_values[2])