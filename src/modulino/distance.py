from .modulino import Modulino
from .lib.vl53l4cd import VL53L4CD

class ModulinoDistance(Modulino):
    default_addresses = [0x29]
    convert_default_addresses = False

    def __init__(self, i2c_bus = None, address: int | None = None) -> None:
        super().__init__(i2c_bus, address, "DISTANCE")
        self.sensor = VL53L4CD(self.i2c_bus, self.address) 
        self.sensor.timing_budget = 20     
        self.sensor.inter_measurement = 0
        self.sensor.start_ranging()

    @property
    def _distance_raw(self):
        while not self.sensor.data_ready:
            pass
        self.sensor.clear_interrupt()
        return self.sensor.distance

    @property
    def distance(self):
        while True:
            raw_distance = self._distance_raw
            # Filter out invalid readings
            if raw_distance > 0:
                return raw_distance