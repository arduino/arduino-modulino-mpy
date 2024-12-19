from .modulino import Modulino
from .lib.vl53l4cd import VL53L4CD

class ModulinoDistance(Modulino):
    """
    Class to interact with the distance sensor of the Modulino Distance.
    """

    default_addresses = [0x29]
    convert_default_addresses = False

    def __init__(self, i2c_bus = None, address: int | None = None) -> None:
        """
        Initializes the Modulino Distance.

        Parameters:
            i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
            address (int): The I2C address of the module. If not provided, the default address will be used.
        """
        
        super().__init__(i2c_bus, address, "Distance")
        self.sensor = VL53L4CD(self.i2c_bus, self.address) 
        self.sensor.timing_budget = 20     
        self.sensor.inter_measurement = 0
        self.sensor.start_ranging()

    @property
    def _distance_raw(self) -> int | None:
        """
        Reads the raw distance value from the sensor and clears the interrupt.

        Returns:
            int: The distance in centimeters.
        """
        try:            
            while not self.sensor.data_ready:
                pass
            self.sensor.clear_interrupt()
            sensor_value = self.sensor.distance
            return sensor_value
        except OSError:
            # Catch timeout errors
            return None

    @property
    def distance(self) -> int:
        """
        Returns:
            int: The distance in centimeters.
        """
        while True:
            raw_distance = self._distance_raw
            # Filter out invalid readings
            if not raw_distance is None and raw_distance > 0:
                return raw_distance