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
    has_mcu = False

    def __init__(self, i2c_bus = None, address: int | None = None, hub_port=None, check_connection: bool = True) -> None:
        """
        Initializes the Modulino Movement.

        Parameters:
            i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
            address (int): The I2C address of the module. If not provided, the default address will be used.
            hub_port (ModulinoHubPort): The Modulino Hub port to which the device is connected.
            check_connection (bool): Whether to check the connection to the module.
        """
        super().__init__(i2c_bus, address, "Movement", check_connection=check_connection, hub_port=hub_port)
        with self._hub_port:
            self.sensor = LSM6DSOX(self.i2c_bus, address=self.address)
        # The pedometer state can't be read back through the driver,
        # so it's put into a known state that the properties can rely on.
        self._configure_pedometer(False, 10)

    @property
    def acceleration(self) -> MovementValues:
        """
        Returns:
            MovementValues: The acceleration values in the x, y, and z axes.
                            These values can be accessed as .x, .y, and .z properties
                            or by using the index operator for tuple unpacking.
        """
        with self._hub_port:
            sensor_values = self.sensor.accel()
        return MovementValues(sensor_values[0], sensor_values[1], sensor_values[2])
    
    @property
    def acceleration_magnitude(self) -> float:
        """
        Returns:
            float: The magnitude of the acceleration vector in g.
                   When the Modulino is at rest (on planet earth), this value should be approximately 1.0g due to gravity.
        """
        x, y, z = self.acceleration
        return (x**2 + y**2 + z**2) ** 0.5

    @property
    def angular_velocity(self) -> MovementValues:
        """
        Returns:
            MovementValues: The gyroscope values in the x, y, and z axes.
                            These values can be accessed as .x, .y, and .z properties
                            or by using the index operator for tuple unpacking.
        """
        with self._hub_port:
            sensor_values = self.sensor.gyro()
        return MovementValues(sensor_values[0], sensor_values[1], sensor_values[2])
    
    @property
    def gyro(self) -> MovementValues:
        """
        Alias for angular_velocity property.

        Returns:
            MovementValues: The gyroscope values in the x, y, and z axes.
                            These values can be accessed as .x, .y, and .z properties
                            or by using the index operator for tuple unpacking.
        """
        return self.angular_velocity

    def _configure_pedometer(self, enabled: bool, debounce_steps: int) -> None:
        with self._hub_port:
            self.sensor.pedometer_config(enable=enabled, debounce=debounce_steps)
        self._pedometer_enabled = enabled
        self._pedometer_debounce_steps = debounce_steps

    @property
    def pedometer_enabled(self) -> bool:
        """
        Returns:
            bool: True if the built-in pedometer of the IMU is enabled.
        """
        return self._pedometer_enabled

    @pedometer_enabled.setter
    def pedometer_enabled(self, value: bool) -> None:
        """
        Enables or disables the built-in pedometer of the IMU.
        Once enabled, steps are counted in the background by the sensor itself
        and can be read at any time using the step_count property.
        When disabled, the step count is kept until it gets reset using reset_step_count().

        Parameters:
            value (bool): True to enable the pedometer, False to disable it.
        """
        self._configure_pedometer(value, self._pedometer_debounce_steps)

    @property
    def pedometer_debounce_steps(self) -> int:
        """
        Returns:
            int: The number of steps that need to be detected in a row before they are counted.
        """
        return self._pedometer_debounce_steps

    @pedometer_debounce_steps.setter
    def pedometer_debounce_steps(self, value: int) -> None:
        """
        Sets the number of steps that need to be detected in a row before they are counted.
        This helps to filter out false positives e.g. from shaking the device.

        Parameters:
            value (int): The number of debounce steps. Range: 0-255. Default: 10.
        """
        if not 0 <= value <= 255:
            raise ValueError("pedometer_debounce_steps must be between 0 and 255")
        self._configure_pedometer(self._pedometer_enabled, value)

    @property
    def step_count(self) -> int:
        """
        Returns:
            int: The number of steps counted by the pedometer since it was enabled
                 or since the last call to reset_step_count().
                 The pedometer needs to be enabled first using pedometer_enabled.
        """
        with self._hub_port:
            return self.sensor.steps()

    def reset_step_count(self) -> None:
        """
        Resets the step count of the pedometer to 0.
        """
        with self._hub_port:
            self.sensor.pedometer_reset()
