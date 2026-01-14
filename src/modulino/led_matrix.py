import micropython
from modulino import Modulino
from framebuf import FrameBuffer, MONO_VLSB


class ModulinoLEDMatrix(Modulino):
    """
    Class to control the LED Matrix module of the Modulino.
    """

    name = "LED Matrix"
    receive_buffer_size: int = 12
    default_addresses = [0x72]

    def __init__(self, i2c_bus=None, address=None):
        """
        Initializes the Modulino LED Matrix.

        Parameters:
            i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
            address (int): The I2C address of the module. If not provided, the default address will be used.
        """
        super().__init__(i2c_bus, address, "LED Matrix")
        self._width = 12
        self._height = 8
        
        # 1. Internal Working Buffer (Standard padded)
        # Requires 1 byte per column -> 12 bytes total
        self._framebuf_buffer = bytearray(self._width * self._height // 8)  # 12
        self._framebuf = FrameBuffer(self._framebuf_buffer, self._width, self._height, MONO_VLSB)
        
        # 2. Hardware Output Buffer (Compact)
        # total_bytes = ((self._width * self._height) + 7) // 8
        # self._raw_buffer = bytearray(total_bytes)  # 12 bytes packed layout
        
        self._fb_dirty = False

    def set_frame(self, data: bytes | bytearray):
        """
        Sets the LED matrix frame from a bytes or bytearray object.

        Parameters:
            data (bytes | bytearray): The data representing the LED matrix frame.
                                      It should be a sequence of 96 bits, each byte representing a pixel.
        """
        expected_size = self._width * self._height // 8
        if len(data) != expected_size:
            raise ValueError(f"Data length must be {expected_size} bytes")
        
        self._raw_buffer = data

    def set_frame_from_ascii(self, ascii_art: str, fill_char: str = '#'):
        """
        Sets the LED matrix frame from an ASCII art string.

        Parameters:
            ascii_art (str): The ASCII art string representing the LED matrix.
            fill_char (str): The character that represents a lit pixel. Default is '#'.
        """
        self._fb_dirty = True
        lines = map(str.strip, ascii_art.splitlines()) # Split and remove leading/trailing whitespace  
        lines = [line for line in lines if line] # Remove empty lines
        
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if x < self._width and y < self._height:
                    self._framebuf.pixel(x, y, 1 if char == fill_char else 0)
        return self

    def fill(self, value: bool):
        """
        Fills the entire LED matrix with the specified value.

        Parameters:
            value (bool): True to turn all pixels on, False to turn them off.
        """
        self._fb_dirty = True
        self._framebuf.fill(1 if value else 0)
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

    def set_pixel(self, x, y, value = True):
        """
        Sets the state of a specific pixel in the LED matrix.

        Parameters:
            x (int): The x-coordinate of the pixel (0-11).
            y (int): The y-coordinate of the pixel (0-7).
            value (bool): True to turn the pixel on, False to turn it off.
        """
        if not (0 <= x < 12 and 0 <= y < 8):
            raise ValueError("Pixel coordinates out of bounds")

        self._fb_dirty = True
        self._framebuf.pixel(x, y, 1 if value else 0)
        return self

    def hline(self, x, y, length, value = True):
        """
        Draws a horizontal line on the LED matrix.

        Parameters:
            x (int): The starting x-coordinate of the line (0-11).
            y (int): The y-coordinate of the line (0-7).
            length (int): The length of the line.
            value (bool): True to turn the pixels on, False to turn them off.
        """
        self._fb_dirty = True
        self._framebuf.hline(x, y, length, 1 if value else 0)
        return self
    
    def vline(self, x, y, length, value = True):
        """
        Draws a vertical line on the LED matrix.

        Parameters:
            x (int): The x-coordinate of the line (0-11).
            y (int): The starting y-coordinate of the line (0-7).
            length (int): The length of the line.
            value (bool): True to turn the pixels on, False to turn them off.
        """
        self._fb_dirty = True
        self._framebuf.vline(x, y, length, 1 if value else 0)
        return self

    def line(self, x1, y1, x2, y2, value = True):
        """
        Draws a line on the LED matrix from (x1, y1) to (x2, y2).

        Parameters:
            x1 (int): The starting x-coordinate of the line (0-11).
            y1 (int): The starting y-coordinate of the line (0-7).
            x2 (int): The ending x-coordinate of the line (0-11).
            y2 (int): The ending y-coordinate of the line (0-7).
            value (bool): True to turn the pixels on, False to turn them off.
        """
        self._fb_dirty = True
        self._framebuf.line(x1, y1, x2, y2, 1 if value else 0)
        return self

    def rect(self, x, y, width, height, value = True):
        """
        Draws a rectangle on the LED matrix.

        Parameters:
            x (int): The x-coordinate of the top-left corner of the rectangle (0-11).
            y (int): The y-coordinate of the top-left corner of the rectangle (0-7).
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            value (bool): True to turn the pixels on, False to turn them off.
        """
        self._fb_dirty = True
        self._framebuf.rect(x, y, width, height, 1 if value else 0)
        return self
    
    def ellipse(self, x, y, width, height, value = True):
        """
        Draws an ellipse on the LED matrix.

        Parameters:
            x (int): The x-coordinate of the bounding box's top-left corner (0-11).
            y (int): The y-coordinate of the bounding box's top-left corner (0-7).
            width (int): The width of the bounding box.
            height (int): The height of the bounding box.
            value (bool): True to turn the pixels on, False to turn them off.
        """
        self._fb_dirty = True
        self._framebuf.ellipse(x, y, width, height, 1 if value else 0)
        return self
    
    def poly(self, x, y, points, value = True, fill = False):
        """
        Draws a polygon on the LED matrix.

        Parameters:
            x (int): The x-coordinate of the polygon's origin (0-11).
            y (int): The y-coordinate of the polygon's origin (0-7).
            points (list of tuples): A list of (x, y) tuples defining the polygon's vertices.
            value (bool): True to turn the pixels on, False to turn them off.
            fill (bool): True to fill the polygon, False for outline only.
        """
        self._fb_dirty = True
        self._framebuf.poly(x, y, points, 1 if value else 0, fill)
        return self

    def text(self, x, y, string, value = True):
        """
        Draws text on the LED matrix.

        Parameters:
            x (int): The x-coordinate of the text's starting position (0-11).
            y (int): The y-coordinate of the text's starting position (0-7).
            string (str): The text string to draw.
            value (bool): True to turn the pixels on, False to turn them off.
        """
        self._fb_dirty = True
        self._framebuf.text(string, x, y, 1 if value else 0)
        return self
    
    def scroll(self, dx, dy):
        """
        Scrolls the LED matrix content by the specified amounts.

        Parameters:
            dx (int): The amount to scroll in the x-direction.
            dy (int): The amount to scroll in the y-direction.
        """
        self._fb_dirty = True
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
        self._fb_dirty = True
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
        if self._fb_dirty:
            # self._pack_buffer(self._framebuf_buffer, self._raw_buffer, self._width, self._height)
            self._fb_dirty = False
        self.write(self._framebuf_buffer)
        self._fb_dirty = False
        self._raw_dirty = False

    @micropython.native
    def _pack_buffer(self, source, dest, width: int, height: int):
        # 1. Calculate layouts
        src_stride = (width + 7) // 8 # bytes per row in source
        full_bytes = width // 8 # bytes per row fully used
        remainder_bits = width % 8 # remaining bits in last byte per row
        
        # 2. Setup Bit Accumulator
        buffer = 0       # Holds bits waiting to be written
        bits_stored = 0  # Count of bits currently in 'buffer'
        dest_idx = 0     # Where we are writing in 'dest'
        
        # 3. Iterate over every row
        for y in range(height):
            row_start = y * src_stride
            
            # --- A. Process the Full Bytes (8 pixels) ---
            for i in range(full_bytes):
                b = source[row_start + i]
                
                # LSB PACKING LOGIC:
                # We put the NEW bits at the TOP of the buffer (shifted left)
                # keeping the OLD bits at the BOTTOM (right).
                buffer = buffer | (b << bits_stored)
                bits_stored += 8
                
                # Flush 8-bit chunks
                while bits_stored >= 8:
                    dest[dest_idx] = buffer & 0xFF
                    buffer = buffer >> 8  # Shift used bits out
                    bits_stored -= 8
                    dest_idx += 1
            
            # --- B. Process the Partial Byte ---
            if remainder_bits > 0:
                b = source[row_start + full_bytes]
                
                # Mask to keep only the valid bits (e.g., 00001111)
                mask = (1 << remainder_bits) - 1
                b = b & mask
                
                # Add to accumulator (at the top)
                buffer = buffer | (b << bits_stored)
                bits_stored += remainder_bits
                
                # Flush if full
                while bits_stored >= 8:
                    dest[dest_idx] = buffer & 0xFF
                    buffer = buffer >> 8
                    bits_stored -= 8
                    dest_idx += 1
                    
        # 4. Flush any lingering bits
        if bits_stored > 0:
            dest[dest_idx] = buffer & 0xFF
