from .modulino import Modulino
from lsm6dsox import LSM6DSOX

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
        super().__init__(i2c_bus, address, "MOVEMENT")
        self.sensor = LSM6DSOX(self.i2c_bus, address=self.address)

    @property
    def accelerometer(self) -> tuple[float, float, float]:
        """
        Returns:
            tuple[float, float, float]: The acceleration values in the x, y, and z axes.        
        """
        return self.sensor.accel()
    
    @property
    def gyro(self) -> tuple[float, float, float]:
        """
        Returns:
            tuple[float, float, float]: The angular velocity values in the x, y, and z axes.
        """
        return self.sensor.gyro()