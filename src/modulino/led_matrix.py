from micropython import const
from modulino import Modulino
from framebuf import FrameBuffer, GS4_HMSB, MONO_VLSB
from time import sleep_ms

_MONOCHROME = const(b'MON')
_GRAYSCALE = const(b'GS4')

_FRAME_LOAD_DELAY_MS = const(5)  # Time to load each frame onto the LED matrix

class ModulinoLEDMatrix(Modulino):
    """
    Class to control the LED Matrix module of the Modulino.
    """

    default_addresses = [0x72]

    def __init__(self, i2c_bus=None, address=None, use_grayscale: bool = False):
        """
        Initializes the Modulino LED Matrix.

        Parameters:
            i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
            address (int): The I2C address of the module. If not provided, the default address will be used.
        """
        super().__init__(i2c_bus, address, "LED Matrix")
        self._width = 12
        self._height = 8

        self._read_buffer = bytearray(4)  # 1 byte for pinstrap address, 3 bytes for mode
        self._display_mode = None
        self._framebuf_buffer = None
        self._framebuf = None
        self._prev_data_buffer = None
        self._default_color = 1
        self.use_grayscale = use_grayscale

    def _read_mode(self) -> bytes:
        """
        Reads the current display mode from the LED matrix.

        Returns:
            bytes: The current display mode ('MON' for Monochrome, 'GS4' for Grayscale).
        """
        self.read(self._read_buffer)
        return self._read_buffer[1:4] # Skip pinstrap address

    @property
    def send_buffer_size(self) -> int:
        return 48 if self.use_grayscale else 12

    @property
    def use_grayscale(self) -> bool:
        """
        Gets whether the LED matrix is in grayscale mode.
        """
        return self._display_mode == _GRAYSCALE

    @use_grayscale.setter
    def use_grayscale(self, value: bool) -> None:
        """
        Sets the LED matrix display mode to grayscale or monochrome.
        """
        if value and self._display_mode == _GRAYSCALE:
            return
        if not value and self._display_mode == _MONOCHROME:
            return
     
        new_mode = _GRAYSCALE if value else _MONOCHROME
        current_mode = self._read_mode()
        expected_bytes = 48 if current_mode == _GRAYSCALE else 12
        buffer = new_mode
        buffer += b'\x00' * (expected_bytes - len(buffer)) # Pad to expected size
        
        if self.write(buffer):
            self._display_mode = new_mode
            if new_mode == _MONOCHROME:
                buffer_size = self._width * self._height // 8  # 12 bytes
                framebuf_format = MONO_VLSB
                self._default_color = 1
            else:
                buffer_size = self._width * self._height // 2  # 48 bytes
                framebuf_format = GS4_HMSB
                self._default_color = 15

            self._framebuf_buffer = bytearray(buffer_size)
            self._prev_data_buffer = bytearray(buffer_size)
            self._framebuf = FrameBuffer(self._framebuf_buffer, self._width, self._height, framebuf_format)

    def _normalize_color(self, color: int | None) -> int:
        """
        Sets the color to a default value if None.
        The default color is 1 for monochrome and 15 for grayscale.

        Parameters:
            color (int | None): The color value to normalize.
        Returns:
            int: The normalized color value.
        """
        return self._default_color if color is None else color

    def set_frame(self, data: bytes | bytearray):
        """
        Sets the LED matrix frame from a bytes or bytearray object.

        Parameters:
            data (bytes | bytearray): The data representing the LED matrix frame.
                                      It should be a sequence of 96 bits, each byte representing a pixel.
        """
        if len(data) != self.send_buffer_size:
            raise ValueError(f"Data length must be {self.send_buffer_size} bytes")
        
        self._framebuf_buffer[:] = data
        return self

    def set_frame_from_ascii(self, ascii_art: str, fill_char: str = '#', color: int = None):
        """
        Sets the LED matrix frame from an ASCII art string.

        Parameters:
            ascii_art (str): The ASCII art string representing the LED matrix.
            fill_char (str): The character that represents a lit pixel. Default is '#'.
            color (int): The color to set the filled pixels to. For grayscale, this can be 0-15. For monochrome, use 0 or 1.
        """
        color = self._normalize_color(color)
        lines = map(str.strip, ascii_art.splitlines()) # Split and remove leading/trailing whitespace  
        lines = [line for line in lines if line] # Remove empty lines
        
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if x < self._width and y < self._height:
                    self._framebuf.pixel(x, y, color if char == fill_char else 0)
        return self

    def fill(self, color: int = None):
        """
        Fills the entire LED matrix with the specified value.

        Parameters:
            color (int): The color to fill the matrix with. For grayscale, this can be 0-15. For monochrome, use 0 or 1.
        """
        color = self._normalize_color(color)
        self._framebuf.fill(color)
        return self

    def get_pixel(self, x, y) -> bool:
        """
        Gets the state of a specific pixel in the LED matrix.

        Parameters:
            x (int): The x-coordinate of the pixel (0-11).
            y (int): The y-coordinate of the pixel (0-7).
        Returns:
            bool: True if the pixel is on, False if it is off.
        """
        if not (0 <= x < 12 and 0 <= y < 8):
            raise ValueError("Pixel coordinates out of bounds")

        return bool(self._framebuf.pixel(x, y))

    def set_pixel(self, x, y, color = None):
        """
        Sets the state of a specific pixel in the LED matrix.

        Parameters:
            x (int): The x-coordinate of the pixel (0-11).
            y (int): The y-coordinate of the pixel (0-7).
            color (int): The color to set the pixel to. For grayscale, this can be 0-15. For monochrome, use 0 or 1.
        """
        if not (0 <= x < 12 and 0 <= y < 8):
            raise ValueError("Pixel coordinates out of bounds")

        color = self._normalize_color(color)
        self._framebuf.pixel(x, y, color)
        return self

    def hline(self, x, y, length, color = None):
        """
        Draws a horizontal line on the LED matrix.

        Parameters:
            x (int): The starting x-coordinate of the line (0-11).
            y (int): The y-coordinate of the line (0-7).
            length (int): The length of the line.
            color (int): The color to set the line to. For grayscale, this can be 0-15. For monochrome, use 0 or 1.
        """
        color = self._normalize_color(color)
        self._framebuf.hline(x, y, length, color)
        return self
    
    def vline(self, x, y, length, color = None):
        """
        Draws a vertical line on the LED matrix.

        Parameters:
            x (int): The x-coordinate of the line (0-11).
            y (int): The starting y-coordinate of the line (0-7).
            length (int): The length of the line.
            color (int): The color to set the line to. For grayscale, this can be 0-15. For monochrome, use 0 or 1.
        """
        color = self._normalize_color(color)
        self._framebuf.vline(x, y, length, color)
        return self

    def line(self, x1, y1, x2, y2, color = None):
        """
        Draws a line on the LED matrix from (x1, y1) to (x2, y2).

        Parameters:
            x1 (int): The starting x-coordinate of the line (0-11).
            y1 (int): The starting y-coordinate of the line (0-7).
            x2 (int): The ending x-coordinate of the line (0-11).
            y2 (int): The ending y-coordinate of the line (0-7).
            color (int): The color to set the line to. For grayscale, this can be 0-15. For monochrome, use 0 or 1.
        """
        color = self._normalize_color(color)
        self._framebuf.line(x1, y1, x2, y2, color)
        return self

    def rect(self, x, y, width, height, color = None):
        """
        Draws a rectangle on the LED matrix.

        Parameters:
            x (int): The x-coordinate of the top-left corner of the rectangle (0-11).
            y (int): The y-coordinate of the top-left corner of the rectangle (0-7).
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            color (int): The color to set the rectangle to. For grayscale, this can be 0-15. For monochrome, use 0 or 1.
        """
        color = self._normalize_color(color)
        self._framebuf.rect(x, y, width, height, color)
        return self
    
    def ellipse(self, x, y, width, height, color = None):
        """
        Draws an ellipse on the LED matrix.

        Parameters:
            x (int): The x-coordinate of the bounding box's top-left corner (0-11).
            y (int): The y-coordinate of the bounding box's top-left corner (0-7).
            width (int): The width of the bounding box.
            height (int): The height of the bounding box.
            color (int): The color to set the ellipse to. For grayscale, this can be 0-15. For monochrome, use 0 or 1.
        """
        color = self._normalize_color(color)
        self._framebuf.ellipse(x, y, width, height, color)
        return self
    
    def poly(self, x, y, points, color = None, fill = False):
        """
        Draws a polygon on the LED matrix.

        Parameters:
            x (int): The x-coordinate of the polygon's origin (0-11).
            y (int): The y-coordinate of the polygon's origin (0-7).
            points (list of tuples): A list of (x, y) tuples defining the polygon's vertices.
            color (int): The color to set the polygon to. For grayscale, this can be 0-15. For monochrome, use 0 or 1.
            fill (bool): True to fill the polygon, False for outline only.
        """
        color = self._normalize_color(color)
        self._framebuf.poly(x, y, points, color, fill)
        return self

    def text(self, x, y, string, color = None):
        """
        Draws text on the LED matrix.

        Parameters:
            x (int): The x-coordinate of the text's starting position (0-11).
            y (int): The y-coordinate of the text's starting position (0-7).
            string (str): The text string to draw.
            color (int): The color to set the text to. For grayscale, this can be 0-15. For monochrome, use 0 or 1.
        """
        color = self._normalize_color(color)
        self._framebuf.text(string, x, y, color)
        return self
    
    def scroll(self, dx, dy):
        """
        Scrolls the LED matrix content by the specified amounts.

        Parameters:
            dx (int): The amount to scroll in the x-direction.
            dy (int): The amount to scroll in the y-direction.
        """
        self._framebuf.scroll(dx, dy)
        return self
    
    def blit(self, buffer, x, y):
        """
        Blits another buffer onto the LED matrix at the specified position.

        Parameters:
            buffer (FrameBuffer): The source buffer to blit from.
            x (int): The x-coordinate on the LED matrix to blit to (0-11).
            y (int): The y-coordinate on the LED matrix to blit to (0-7).
        """
        self._framebuf.blit(buffer, x, y)
        return self

    def clear(self):
        """
        Clears the LED matrix by turning off all pixels.
        """
        self.fill(False)
        return self

    def show(self):
        """
        Sends the current buffer to the LED matrix to update the display.
        """
        if self._prev_data_buffer is not None and self._framebuf_buffer == self._prev_data_buffer:
            return self

        self.write(self._framebuf_buffer)
        if self._prev_data_buffer is not None:
            self._prev_data_buffer[:] = self._framebuf_buffer
        return self

class Animation:
    """
    Class to represent an animation for the LED Matrix.
    """

    def __init__(self, led_matrix : ModulinoLEDMatrix, frames: list[bytes | bytearray], fps: int):
        """
        Initializes the Animation.

        Parameters:
            led_matrix (ModulinoLEDMatrix): The LED matrix to display the animation on.
            frames (list[bytes | bytearray]): A list of frames, each represented as bytes or bytearray.
            fps (int): The frames per second for the animation.
        """
        self._led_matrix = led_matrix
        self._frames = frames
        self._frame_delay = max(0, int(1000 / fps) - _FRAME_LOAD_DELAY_MS) # Delay to achieve target FPS

    def play(self, loop: bool = False):
        """
        Plays the animation on the LED matrix.

        Parameters:
            loop (bool): If True, the animation will loop indefinitely. Default is False.
        """
        matrix = self._led_matrix
        while True:
            for frame in self._frames:
                matrix.set_frame(frame).show()
                sleep_ms(self._frame_delay)
            if not loop:
                break

class TimedAnimation:
    """
    Class to represent a timed animation for the LED Matrix.
    Each frame can have its own display duration.
    """

    def __init__(self, led_matrix : ModulinoLEDMatrix, frames: list[tuple[bytes | bytearray, int]]):
        """
        Initializes the TimedAnimation.

        Parameters:
            led_matrix (ModulinoLEDMatrix): The LED matrix to display the animation on.
            frames (list[tuple[bytes | bytearray, int]]): A list of tuples, each containing a frame (bytes or bytearray)
                                                          and its display duration in milliseconds.
        """
        self._led_matrix = led_matrix
        self._frames = frames

    def play(self, loop: bool = False):
        """
        Plays the timed animation on the LED matrix.

        Parameters:
            loop (bool): If True, the animation will loop indefinitely. Default is False.
        """
        matrix = self._led_matrix
        while True:
            for frame, duration in self._frames:
                matrix.set_frame(frame).show()
                # Subtract frame load delay as the current frame
                # will keep displaying while the next frame is being loaded
                sleep_ms(max(0, duration - _FRAME_LOAD_DELAY_MS))
            if not loop:
                break
    