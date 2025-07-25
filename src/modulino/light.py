from .modulino import Modulino
from ltr381rgb import LTR381RGB

class ModulinoLight(Modulino):
    """
    Class to interact with the light sensor of the Modulino Light.

    It offers an easy way to read how bright the surroundings are (in lux),
    the color of the light as red, green and blue values, the color
    temperature in kelvin and the amount of invisible infrared light.

    The readings come from an LTR-381RGB-01 ambient light and color sensor.
    Advanced users can access the underlying sensor through the `sensor`
    attribute to fine-tune settings such as gain or integration time.
    """

    default_addresses = [0x53]
    has_mcu = False

    def __init__(self, i2c_bus: I2C = None, address: int = None) -> None:
        """
        Initializes the Modulino Light.

        Parameters:
            i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
            address (int): The I2C address of the module. If not provided, the default address will be used.
        """
        super().__init__(i2c_bus, address, "Light")
        self.sensor = LTR381RGB(self.i2c_bus, self.address)

    @property
    def lux(self) -> float:
        """
        How bright the surroundings are, measured in lux.
        Higher numbers mean more light. For reference, a dim room is around
        50 lux, a well-lit office around 500 lux and direct sunlight can be
        tens of thousands of lux.

        Returns:
            float: The ambient brightness in lux.
        """
        return self.sensor.lux

    @property
    def rgb(self) -> tuple:
        """
        The color of the light as red, green and blue values.
        Each value goes from 0 (none) to 255 (most).

        Returns:
            tuple: A (red, green, blue) tuple.
        """
        return self.sensor.rgb_color

    @property
    def color_name(self) -> str:
        """
        A simple name for the color the sensor is seeing,
        for example "red", "green", "blue" or "yellow".

        Returns:
            str: The name of the closest matching color.
        """
        return self.sensor.approximate_color

    @property
    def color_temperature(self) -> int:
        """
        The color temperature of the light in kelvin (K).
        Warm light (like a candle) has a low value, while cool light
        (like a cloudy sky) has a high value.
        Returns None when there is not enough light to measure it.

        Returns:
            int: The color temperature in kelvin, or None if it can't be measured.
        """
        try:
            return round(self.sensor.color_temperature)
        except Exception:
            # Not enough light to estimate a color temperature.
            return None

    @property
    def infrared(self) -> int:
        """
        The amount of infrared light, which is invisible to the human eye.
        Sunlight and incandescent bulbs are rich in infrared, while most
        screens and LED lights emit very little.

        Returns:
            int: The infrared light level.
        """
        return self.sensor.ir_light
