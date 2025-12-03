from .modulino import Modulino
from time import ticks_ms
from micropython import const

class ModulinoJoystick(Modulino):
    """
    Class to operate the Modulino Joystick module.
    """

    default_addresses = [0x58]
    default_long_press_duration = const(1000)  # milliseconds

    def __init__(self, i2c_bus=None, address=None):
        """
        Initializes the Modulino Joystick module.

        Parameters:
            i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
            address (int): The I2C address of the module. If not provided, the default address will be used.
        """
        super().__init__(i2c_bus, address, "Joystick")
        self._state = [0, 0, 0]  # x, y, button state
        self._x = 0
        self._y = 0
        self._deadzone_threshold = 10
        self._last_press_timestamp = 0
        self._button_pressed = False
        self._on_button_press = None
        self._on_button_release = None
        self._on_button_long_press = None
        self._long_press_duration = self.default_long_press_duration  # milliseconds

    def _values_changed(self, x_old, x_new, y_old, y_new, threshold=2):
        """
        Checks if the joystick state has changed significantly.

        Parameters:
            x_old (int): Old x-coordinate.
            x_new (int): New x-coordinate.
            y_old (int): Old y-coordinate.
            y_new (int): New y-coordinate.
            threshold (int): The minimum change in position to consider it a state change.
        """
        return abs(x_new - x_old) > threshold or abs(y_new - y_old) > threshold

    def _normalize_coordinates(self, x, y):
        """
        Applies deadzone logic to joystick coordinates and maps them to a range centered around 0.

        Parameters:
            x (int): The x-coordinate of the joystick.
            y (int): The y-coordinate of the joystick.

        Returns:
            tuple: Adjusted x and y coordinates after applying deadzone.
        """
        if abs(x - 128) < self._deadzone_threshold:
            x = 128
        if abs(y - 128) < self._deadzone_threshold:
            y = 128
        return x - 128, y - 128

    def update(self):
        """
        Updates the joystick state by reading the current position and button state.
        """
        new_state = self.read(3)
        previous_state = self._state
        self._state = new_state
        current_timestamp = ticks_ms()        
        button_state_changed = new_state[2] != previous_state[2]

        x = new_state[0]
        y = new_state[1]                
        x, y = self._normalize_coordinates(x, y)
        x_y_changed = self._values_changed(x, self._x, y, self._y)
        
        if x_y_changed:
            self._x = x
            self._y = y
        
        # Check for long press
        if(new_state[2] == 1 and previous_state[2] == 1 and self._last_press_timestamp and current_timestamp - self._last_press_timestamp > self.long_press_duration):
            self._last_press_timestamp = None
            if self._on_button_long_press:
                self._on_button_long_press()

        if button_state_changed:
            self._button_pressed = bool(new_state[2] & 0x01)

            # Handle button press and release events
            if new_state[2] == 1 and previous_state[2] == 0:
                self._last_press_timestamp = ticks_ms()
                if self._on_button_press:
                    self._on_button_press()
            elif new_state[2] == 0 and previous_state[2] == 1 and self._on_button_release:
                self._on_button_release()

        return x_y_changed or button_state_changed

    @property
    def button_pressed(self):
        """
        Returns True if the joystick button is pressed, False otherwise.
        """
        return self._button_pressed

    @property
    def x(self) -> int:
        """
        Returns the x-coordinate of the joystick position.
        """
        return self._x

    @property
    def y(self) -> int:
        """
        Returns the y-coordinate of the joystick position.
        """
        return self._y

    @property
    def deadzone_threshold(self) -> int:
        """
        Returns the deadzone threshold for joystick movement.
        """
        return self._deadzone_threshold

    @deadzone_threshold.setter
    def deadzone_threshold(self, value: int):
        """
        Sets the deadzone threshold for joystick movement.

        Parameters:
            value (int): The new deadzone threshold.
        """
        if value < 0:
            raise ValueError("Deadzone threshold must be non-negative.")
        self._deadzone_threshold = value

    @property
    def on_button_press(self):
        """
        Callback function to be called when the joystick button is pressed.
        """
        return self._on_button_press

    @on_button_press.setter
    def on_button_press(self, callback):
        """
        Sets the callback function to be called when the joystick button is pressed.

        Parameters:
            callback (callable): The function to call when the button is pressed.
        """
        if not callable(callback):
            raise ValueError("Callback must be a callable function.")
        self._on_button_press = callback

    @property
    def on_button_release(self):
        """
        Callback function to be called when the joystick button is released.
        """
        return self._on_button_release

    @on_button_release.setter
    def on_button_release(self, callback):
        """
        Sets the callback function to be called when the joystick button is released.

        Parameters:
            callback (callable): The function to call when the button is released.
        """
        if not callable(callback):
            raise ValueError("Callback must be a callable function.")
        self._on_button_release = callback

    @property
    def on_button_long_press(self):
        """
        Callback function to be called when the joystick button is long-pressed.
        """
        return self._on_button_long_press
    
    @on_button_long_press.setter
    def on_button_long_press(self, callback):
        """
        Sets the callback function to be called when the joystick button is long-pressed.

        Parameters:
            callback (callable): The function to call when the button is long-pressed.
        """
        if not callable(callback):
            raise ValueError("Callback must be a callable function.")
        self._on_button_long_press = callback

    @property
    def long_press_duration(self) -> int:
        """
        Returns the duration in milliseconds for a long press.
        """
        return self._long_press_duration
    
    @long_press_duration.setter
    def long_press_duration(self, duration: int):
        """
        Sets the duration in milliseconds for a long press.

        Parameters:
            duration (int): The new long press duration in milliseconds.
        """
        if duration < 0:
            raise ValueError("Long press duration must be non-negative.")
        self._long_press_duration = duration