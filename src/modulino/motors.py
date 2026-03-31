from .modulino import Modulino
from micropython import const

class DecayMode:
  """Enum-like decay mode constants for `ModulinoMotors.set_decay`."""
  SLOW = const(0)
  MIXED_30_FAST_70_SLOW = const(1)
  MIXED_60_FAST_40_SLOW = const(2)
  FAST = const(3)

class ModulinoMotors(Modulino):
  """
  Class to operate the motors of the Modulino.
  """
  class DecayMode:
    """Enum-like decay mode constants for `set_decay`."""
    SLOW = 0
    MIXED_30_FAST_70_SLOW = 1
    MIXED_60_FAST_40_SLOW = 2
    FAST = 3

  default_addresses = [0x48]

  CMD_MODE      = const(ord('M'))
  CMD_SPEED_DC  = const(ord('S'))
  CMD_STEPPER   = const(ord('G'))
  CMD_DECAY     = const(ord('T'))
  CMD_STEP_MODE = const(ord('H'))
  CMD_FREQ_DC   = const(ord('F'))
  CMD_HFS       = const(ord('X'))

  MODE_DC       = const(0)
  MODE_STEPPER  = const(1)

  FLAG_BUSY        = const(0x01)
  FLAG_MODE        = const(0x02)
  FLAG_STEP_MODE   = const(0x04)
  FLAG_HFS         = const(0x08)
  FLAG_DECAY_MASK  = const(0x30)
  FLAG_DECAY_SHIFT = const(4)

  MAX_SPEED = const(32767)  # Max speed value for 16-bit signed integer
  ADC_FULL_SCALE = const(4095)  # 12-bit ADC full scale
  ADC_REF_MV = const(3300)  # ADC reference in millivolts
  ISEN_RESISTOR_OHMS = const(4700)  # ISEN pull-down resistor on the host board
  KISEN_FULL_SCALE = const(7500)  # MAX22211 KISEN when HFS is low
  KISEN_HALF_SCALE = const(3750)  # MAX22211 KISEN when HFS is high

  def __init__(self, i2c_bus=None, address=None, check_connection: bool = True,
               steps_per_revolution=None):
    """
    Initializes the Modulino Motors.
    
    Parameters:
        i2c_bus (I2C): The I2C bus to use. If not provided, the default I2C bus will be used.
        address (int): The I2C address of the module. If not provided, the default address will be used.
        check_connection (bool): Whether to check the connection to the module.
        steps_per_revolution (int | None): Full-step motor steps per shaft
          revolution. Required for RPM-based stepper control.
    """
    super().__init__(i2c_bus, address, "Motors", check_connection=check_connection)
    self._send_buffer = bytearray(7)  # Buffer for sending commands
    self._receive_buffer = bytearray(6)  # Buffer for receiving sense data
    self._speed_a = 0
    self._invert_a = False
    self._speed_b = 0
    self._invert_b = False
    self._frequency = 20000
    self._mode = self.MODE_DC
    self._half_step = False
    self._decay_mode = 0
    self._hfs_enabled = False
    self._busy = False
    self._sense_a = 0
    self._sense_b = 0
    self.steps_per_revolution = steps_per_revolution

  def _send_command(self, msg):
    # Padding to 7 bytes to match firmware expectation
    length = len(msg)
    if length < 7:
        msg += b'\x00' * (7 - length)
    elif length > 7:
        raise ValueError(f"Message length {length} exceeds maximum of 7 bytes")
    self.write(msg)

  def _update_speed(self):
    val_a = int(self._speed_a * self.MAX_SPEED / 100) * (-1 if self._invert_a else 1)
    val_b = int(self._speed_b * self.MAX_SPEED / 100) * (-1 if self._invert_b else 1)
    self._set_dc_speed_raw(val_a, val_b)

  def _set_dc_speed_raw(self, speed_a: int, speed_b: int) -> None:
    """Set DC motor speeds in raw signed int16 units (-32767..32767)."""
    speed_a = int(speed_a)
    speed_b = int(speed_b)
    if speed_a < -self.MAX_SPEED or speed_a > self.MAX_SPEED:
      raise ValueError("speed_a must be in range -32767..32767")
    if speed_b < -self.MAX_SPEED or speed_b > self.MAX_SPEED:
      raise ValueError("speed_b must be in range -32767..32767")

    self._send_buffer[:] = b'\x00' * len(self._send_buffer)
    self._send_buffer[0] = self.CMD_SPEED_DC
    self._send_buffer[1:3] = speed_a.to_bytes(2, 'little', True)
    self._send_buffer[3:5] = speed_b.to_bytes(2, 'little', True)
    self._send_command(self._send_buffer)

  def _sense_raw_to_ma(self, raw: int, hfs_enabled: bool) -> float:
    """Convert raw ADC delta counts from ISEN to motor current in mA."""
    kisen = self.KISEN_HALF_SCALE if hfs_enabled else self.KISEN_FULL_SCALE
    return (float(raw) * self.ADC_REF_MV * kisen) / (self.ADC_FULL_SCALE * self.ISEN_RESISTOR_OHMS)

  def stop(self) -> None:
    """Stop both motors."""
    self._set_dc_speed_raw(0, 0)

  def move_stepper(self, steps: int, speed_period: int) -> None:
    """Command a stepper move using signed steps and uint16 period."""
    speed_period = int(speed_period)
    if speed_period < 1 or speed_period > 0xFFFF:
      raise ValueError("speed_period must be in range 1..65535")

    self._send_buffer[:] = b'\x00' * len(self._send_buffer)
    self._send_buffer[0] = self.CMD_STEPPER
    self._send_buffer[1:5] = int(steps).to_bytes(4, 'little', True)
    self._send_buffer[5:7] = speed_period.to_bytes(2, 'little')
    self._send_command(self._send_buffer)

  def move_stepper_rpm(self, steps: int, rpm: float) -> None:
    """Command a stepper move using target speed in RPM."""
    if self._steps_per_revolution is None:
      raise ValueError("steps_per_revolution must be set before using move_stepper_rpm")

    rpm = float(rpm)
    if rpm <= 0:
      raise ValueError("rpm must be > 0")

    effective_steps_per_rev = self._steps_per_revolution * (2 if self._half_step else 1)
    period_us = int(60000000.0 / (rpm * effective_steps_per_rev))
    if period_us < 1 or period_us > 0xFFFF:
      raise ValueError("rpm out of range for current step mode and steps_per_revolution")

    self.move_stepper(steps, period_us)

  @property
  def speed_a(self) -> int:
    """
    Gets or sets the speed of motor A in percentage (0-100).
    """
    return self._speed_a

  @speed_a.setter
  def speed_a(self, value: int):
    if not 0 <= value <= 100:
      raise ValueError("Speed must be between 0 and 100")
    self._speed_a = value
    self._update_speed()

  @property
  def invert_a(self) -> bool:
    """
    Gets or sets if the direction of motor A is inverted.
    """
    return self._invert_a

  @invert_a.setter
  def invert_a(self, value: bool):
    self._invert_a = value
    self._update_speed()

  @property
  def speed_b(self) -> int:
    """
    Gets or sets the speed of motor B in percentage (0-100).
    """
    return self._speed_b

  @speed_b.setter
  def speed_b(self, value: int):
    if not 0 <= value <= 100:
      raise ValueError("Speed must be between 0 and 100")
    self._speed_b = value
    self._update_speed()

  @property
  def invert_b(self) -> bool:
    """
    Gets or sets if the direction of motor B is inverted.
    """
    return self._invert_b

  @invert_b.setter
  def invert_b(self, value: bool):
    self._invert_b = value
    self._update_speed()

  def set_decay(self, decay_mode: int) -> None:
    """
    Sets the decay mode of the motors.

    Parameters:
      decay_mode (int): One of `ModulinoMotors.DecayMode.*` or a raw int in range 0..3.
    """
    decay_mode = int(decay_mode)
    if decay_mode < 0 or decay_mode > 3:
      raise ValueError("decay_mode must be in range 0..3")
    self._send_command(bytes([self.CMD_DECAY, decay_mode]))
    self._decay_mode = decay_mode

  @property
  def frequency(self) -> int:
    """
    Gets or sets the frequency of the motors.
    """
    return self._frequency

  @frequency.setter
  def frequency(self, value: int):
    """Set DC Motor PWM Frequency in Hz (200 - 60000)"""
    value = int(value)
    if value < 200 or value > 60000:
      raise ValueError("frequency must be in range 200..60000 Hz")
    self._frequency = value
    # Command: 'F' + uint16
    self._send_buffer[:] = b'\x00' * len(self._send_buffer)  # Clear buffer
    self._send_buffer[0] = self.CMD_FREQ_DC
    self._send_buffer[1:3] = value.to_bytes(2, 'little')
    self._send_command(self._send_buffer)

  def update(self) -> tuple[int, int, bool, bool, int, bool, int]:
    """
    Refresh telemetry from the module.

    Returns:
      tuple[int, int, bool, bool, int, bool, int]:
      (sense_a, sense_b, busy, hfs_enabled, mode, half_step, decay_mode)
    """
    self._receive_buffer[:] = b'\x00' * len(self._receive_buffer)
    self.read(self._receive_buffer)

    self._sense_a = int.from_bytes(self._receive_buffer[1:3], 'little')
    self._sense_b = int.from_bytes(self._receive_buffer[3:5], 'little')
    flags = self._receive_buffer[5]
    self._busy = bool(flags & self.FLAG_BUSY)
    self._hfs_enabled = bool(flags & self.FLAG_HFS)
    self._mode = self.MODE_STEPPER if (flags & self.FLAG_MODE) else self.MODE_DC
    self._half_step = bool(flags & self.FLAG_STEP_MODE)
    self._decay_mode = (flags & self.FLAG_DECAY_MASK) >> self.FLAG_DECAY_SHIFT

    return (self._sense_a, self._sense_b, self._busy, self._hfs_enabled,
            self._mode, self._half_step, self._decay_mode)

  @property
  def busy(self) -> bool:
    """Returns True when the module reports an active move."""
    self.update()
    return self._busy

  @property
  def half_full_scale_enabled(self) -> bool:
    """Gets or sets the half-full-scale (HFS) mode."""
    self.update()
    return self._hfs_enabled

  @half_full_scale_enabled.setter
  def half_full_scale_enabled(self, value: bool) -> None:
    """Set HFS pin: False=full range, True=half range."""
    val = 1 if value else 0
    self._send_command(bytes([self.CMD_HFS, val]))
    self._hfs_enabled = bool(value)

  @property
  def sensed_current_a(self) -> float:
    """Gets sensed current of motor A in milliamps (mA)."""
    self.update()
    return self._sense_raw_to_ma(self._sense_a, self._hfs_enabled)

  @property
  def sensed_current_b(self) -> float:
    """Gets sensed current of motor B in milliamps (mA)."""
    self.update()
    return self._sense_raw_to_ma(self._sense_b, self._hfs_enabled)

  @property
  def sensed_current(self) -> tuple[float, float]:
    """Gets sensed currents of both motors in milliamps (mA)."""
    self.update()
    return (
      self._sense_raw_to_ma(self._sense_a, self._hfs_enabled),
      self._sense_raw_to_ma(self._sense_b, self._hfs_enabled),
    )

  @property
  def stepper_mode_enabled(self) -> bool:
    """Returns True if stepper mode is active, False if DC mode."""
    self.update()
    return self._mode == self.MODE_STEPPER

  @stepper_mode_enabled.setter
  def stepper_mode_enabled(self, value: bool) -> None:
    """Set stepper mode: True=stepper, False=DC."""
    mode = self.MODE_STEPPER if value else self.MODE_DC
    if mode not in (self.MODE_DC, self.MODE_STEPPER):
      raise ValueError("mode must be MODE_DC (0) or MODE_STEPPER (1)")
    self._send_command(bytes([self.CMD_MODE, mode]))
    self._mode = mode

  @property
  def half_step_enabled(self) -> bool:
    """Gets or sets the half-step mode."""
    self.update()
    return self._half_step

  @half_step_enabled.setter
  def half_step_enabled(self, value: bool) -> None:
    """Set step mode: False=full step, True=half step."""
    val = 1 if value else 0
    self._send_command(bytes([self.CMD_STEP_MODE, val]))
    self._half_step = bool(value)

  @property
  def steps_per_revolution(self) -> int | None:
    """Gets or sets full-step motor steps per shaft revolution."""
    return self._steps_per_revolution

  @steps_per_revolution.setter
  def steps_per_revolution(self, value: int) -> None:
    if value is not None and value < 1:
      raise ValueError("steps_per_revolution must be >= 1")
    self._steps_per_revolution = value

  @property
  def decay_mode(self) -> int:
    """Returns decay mode reported by the latest telemetry update."""
    self.update()
    return self._decay_mode

  @property
  def send_buffer_size(self) -> int:
    return len(self._send_buffer)