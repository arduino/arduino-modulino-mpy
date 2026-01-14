import sys
from micropython import const
from machine import I2C
from .modulino import _I2CHelper
from . import *

_BOOTLOADER_ADDRESS = const(0x64)

class DeviceManager:

    # Modules to exclude from discovery
    _excluded_modules = ["modulino.modulino", 
                         "modulino.helpers", 
                         "modulino.lib"]

    def __init__(self, i2c_bus: I2C = None) -> None:
        if i2c_bus is None:
            i2c_bus = _I2CHelper.get_interface()
        self.i2c_bus = i2c_bus
        self._address_to_class_map = {}        
        self._init_address_to_class_map()

    def _init_address_to_class_map(self):
        modules = self._modulino_modules()

        for module in modules:
            classes = self._modulino_classes(module)
            for cls in classes:
                if hasattr(cls, 'default_addresses'):
                    for address in cls.default_addresses:
                        self._address_to_class_map[address] = cls

    def _modulino_modules(self) -> list:
        """
        Returns a list of all loaded Modulino modules.

        Returns:
            list: A list of Modulino module objects.
        """
        modulino_modules = []
        for module_name, module in sys.modules.items():
            # Skip submodules
            if module_name.count('.') > 1:
                continue
            if not module_name.startswith('modulino.'):
                continue
            if module_name in self._excluded_modules:
                continue            
            modulino_modules.append(module)
        return modulino_modules

    def _modulino_classes(self, module) -> list:
        """
        Returns a list of all classes in the given module that start with 'Modulino'.
        Parameters:
            module (module): The module to inspect.
        Returns:
            list: A list of class objects.
        """
        classes = dir(module) if module else []
        modulino_class_names = [cls for cls in classes if cls.startswith('Modulino') and cls != 'Modulino']
        modulino_classes = []
        
        for cls_name in modulino_class_names:
            cls = getattr(module, cls_name)
            if issubclass(cls, Modulino):
                modulino_classes.append(cls)

        return modulino_classes

    def _class_from_address(self, address: int):
        """
        Returns the Modulino device class for the given I2C address.
        Parameters:
            address (int): The I2C address of the device.
        Returns:
            class: The Modulino device class.
        """
        if address in self._address_to_class_map:
            return self._address_to_class_map[address]
        
        # Get pinstrap address from device that may have a custom address
        dev = Modulino(i2c_bus=self.i2c_bus, address=address, check_connection=False)
        pinstrap_address = dev.pin_strap_address
        
        if pinstrap_address in self._address_to_class_map:
            return self._address_to_class_map[pinstrap_address]
        
        return None

    def available_devices(self) -> list[Modulino]:
        """
        Finds all devices on the i2c bus and returns them as 
        a list of Modulino subclass objects.

        Returns:
        list: A list of Modulino subclass objects or empty list if no devices are found.
        """
        device_addresses = Modulino.scan(self.i2c_bus)
        devices = []
        for address in device_addresses:
            if address == _BOOTLOADER_ADDRESS:
                # Skip bootloader address
                continue
            device_class = self._class_from_address(address)
            if device_class is not None:
                device = device_class(i2c_bus=self.i2c_bus, address=address)
                devices.append(device)
        return devices
