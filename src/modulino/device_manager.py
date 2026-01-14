# from .modulino import Modulino
# from .pixels import ModulinoPixels, ModulinoColor
# from .thermo import ModulinoThermo
# from .buzzer import ModulinoBuzzer
# from .buttons import ModulinoButtons
# from .knob import ModulinoKnob
# from .movement import ModulinoMovement
# from .distance import ModulinoDistance
# from .joystick import ModulinoJoystick
# from .latch_relay import ModulinoLatchRelay
# from .vibro import ModulinoVibro, PowerLevel
import sys
from micropython import const
from modulino import *

_BOOTLOADER_ADDRESS = const(0x64)

class DeviceManager:

    _excluded_modules = ["modulino.modulino", 
                         "modulino.helpers", 
                         "modulino.lib"]

    def _modulino_modules(self) -> list:
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

      @staticmethod
    def available_devices(bus: I2C = None) -> list[Modulino]:
        """
        Finds all devices on the i2c bus and returns them as a list of Modulino objects.

        Parameters:
        bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.

        Returns:
        list: A list of Modulino objects.
        """
        if bus is None:
        bus = _I2CHelper.get_interface()
        device_addresses = Modulino.scan(bus)
        devices = []
        for address in device_addresses:
        if address == _BOOTLOADER_ADDRESS:
            # Skip bootloader address
            continue
        device = Modulino(i2c_bus=bus, address=address, check_connection=False)
        devices.append(device)
        return devices

    def _classes_in_module(self, module):
        m = sys.modules.get(module, None)
        classes = dir(m) if m else []
        modulino_class_names = [cls for cls in classes if cls.startswith('Modulino') and cls != 'Modulino']
        modulino_classes = [getattr(m, cls) for cls in modulino_class_names]
        return modulino_classes

    def _device_classes(self):
        device_classes = []
        modules = self._modulino_modules()
        for module in modules:
            classes = self._classes_in_module(module.__name__)
            for cls in classes:
                if issubclass(cls, Modulino):
                    device_classes.append(cls)
        return device_classes

d = DeviceManager()
# mods = d._modulino_modules()
# print(f"Modulino modules found: {[mod.__name__ for mod in mods]}")

# for mod in mods:
#     classes = d._classes_in_module(mod.__name__)
#     print(f"Modulino classes in module {mod.__name__}: {[cls.__name__ for cls in classes]}")

device_classes = d._device_classes()
print(f"Modulino device classes found: {[cls.__name__ for cls in device_classes]}")