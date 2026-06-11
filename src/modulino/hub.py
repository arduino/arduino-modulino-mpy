from .modulino import Modulino
from micropython import const
from machine import I2C

class ModulinoHubPort:
    """
    Represents a port on the Modulino Hub.
    """
    def __init__(self, hub:'ModulinoHub', port_number: int):
        self._hub = hub
        self._port_number = port_number

    def __enter__(self):
        self._hub.select_port(self._port_number)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._hub.deselect_ports()

class ModulinoHub(Modulino):
    """
    Class to interact with the Modulino Hub (TCA9548A I2C multiplexer).
    """

    DEFAULT_ADDRESS = const(0x70)
    has_mcu = False

    def __init__(self, i2c_bus: I2C = None, address: int = DEFAULT_ADDRESS, hub_port=None, check_connection: bool = True) -> None:
        """
        Initializes the Modulino Hub.

        Parameters:
            i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
            address (int): The I2C address of the module.
            hub_port (ModulinoHubPort): The Modulino Hub port to which the device is connected.
            check_connection (bool): Whether to check the connection to the module.
        """
        super().__init__(i2c_bus, address, "Hub", check_connection=check_connection, hub_port=hub_port)
        self._write_buffer = bytearray(1)  # Buffer for writing data to the multiplexer

    def select_port(self, port: int) -> None:
        """
        Selects a specific port (0-7) on the multiplexer.
        """
        if not 0 <= port <= 7:
            raise ValueError("Port must be between 0 and 7")
        
        self._write_buffer[0] = 1 << port
        self.write(self._write_buffer)
        
    def deselect_ports(self) -> None:
        """
        Deselects all ports on the multiplexer.
        """
        self._write_buffer[0] = 0
        self.write(self._write_buffer)

    def get_port(self, port_number: int) -> ModulinoHubPort:
        """
        Creates a context manager for the specified port.
        """
        return ModulinoHubPort(self, port_number)