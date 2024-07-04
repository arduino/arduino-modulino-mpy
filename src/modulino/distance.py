from micropython import const
#from ..lib.vl53l4cd import VL53L4CD

class ModulinoDistance():
    DEFAULT_ADDRESS = const(0x29)

    def __init__(self, i2c_bus, address: int = DEFAULT_ADDRESS) -> None:
        self._i2c_bus = i2c_bus
        self._address = address
        #self._sensor = VL53L4CD(i2c_bus, address)        

    def begin(self):
        self._sensor.start_ranging()

    @property
    def distance(self):
        while not self._sensor.data_ready:
            pass
        self._sensor.clear_interrupt()
        return self._sensor.distance