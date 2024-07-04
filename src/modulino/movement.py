from lsm6dsox import LSM6DSOX
from micropython import const

class ModulinoMovement():
    DEFAULT_ADDRESS = const(0x6A)

    def __init__(self, i2c_bus, address: int = DEFAULT_ADDRESS) -> None:
        self._i2c_bus = i2c_bus
        self._address = address
        self._sensor = LSM6DSOX(i2c_bus)

    @property
    def accelerometer(self) -> tuple:
        return self._sensor.accel()
    
    @property
    def gyro(self) -> tuple:
        return self._sensor.gyro()