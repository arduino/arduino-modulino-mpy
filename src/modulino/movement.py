from .modulino import Modulino
from lsm6dsox import LSM6DSOX

class ModulinoMovement(Modulino):
    # Module can have one of two default addresses
    # based on the solder jumper configuration on the board
    default_addresses = [0x6A, 0x6B]
    convert_default_addresses = False

    def __init__(self, i2c_bus=None, address: int | None = None) -> None:
        super().__init__(i2c_bus, address, "MOVEMENT")
        self.sensor = LSM6DSOX(self.i2c_bus, address=self.address)

    @property
    def accelerometer(self) -> tuple:
        return self.sensor.accel()
    
    @property
    def gyro(self) -> tuple:
        return self.sensor.gyro()