# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_vl53l4cd`
================================================================================

CircuitPython helper library for the VL53L4CD time of flight distance sensor.


* Author(s): Carter Nelson

Implementation Notes
--------------------

**Hardware:**

* `Adafruit VL53L4CD Time of Flight Distance Sensor <https://www.adafruit.com/product/5396>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

import time
import struct
from micropython import const

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_VL53L4CD.git"

_VL53L4CD_SOFT_RESET = const(0x0000)
_VL53L4CD_I2C_SLAVE_DEVICE_ADDRESS = const(0x0001)
_VL53L4CD_VHV_CONFIG_TIMEOUT_MACROP_LOOP_BOUND = const(0x0008)
_VL53L4CD_XTALK_PLANE_OFFSET_KCPS = const(0x0016)
_VL53L4CD_XTALK_X_PLANE_GRADIENT_KCPS = const(0x0018)
_VL53L4CD_XTALK_Y_PLANE_GRADIENT_KCPS = const(0x001A)
_VL53L4CD_RANGE_OFFSET_MM = const(0x001E)
_VL53L4CD_INNER_OFFSET_MM = const(0x0020)
_VL53L4CD_OUTER_OFFSET_MM = const(0x0022)
_VL53L4CD_I2C_FAST_MODE_PLUS = const(0x002D)
_VL53L4CD_GPIO_HV_MUX_CTRL = const(0x0030)
_VL53L4CD_GPIO_TIO_HV_STATUS = const(0x0031)
_VL53L4CD_SYSTEM_INTERRUPT = const(0x0046)
_VL53L4CD_RANGE_CONFIG_A = const(0x005E)
_VL53L4CD_RANGE_CONFIG_B = const(0x0061)
_VL53L4CD_RANGE_CONFIG_SIGMA_THRESH = const(0x0064)
_VL53L4CD_MIN_COUNT_RATE_RTN_LIMIT_MCPS = const(0x0066)
_VL53L4CD_INTERMEASUREMENT_MS = const(0x006C)
_VL53L4CD_THRESH_HIGH = const(0x0072)
_VL53L4CD_THRESH_LOW = const(0x0074)
_VL53L4CD_SYSTEM_INTERRUPT_CLEAR = const(0x0086)
_VL53L4CD_SYSTEM_START = const(0x0087)
_VL53L4CD_RESULT_RANGE_STATUS = const(0x0089)
_VL53L4CD_RESULT_SPAD_NB = const(0x008C)
_VL53L4CD_RESULT_SIGNAL_RATE = const(0x008E)
_VL53L4CD_RESULT_AMBIENT_RATE = const(0x0090)
_VL53L4CD_RESULT_SIGMA = const(0x0092)
_VL53L4CD_RESULT_DISTANCE = const(0x0096)

_VL53L4CD_RESULT_OSC_CALIBRATE_VAL = const(0x00DE)
_VL53L4CD_FIRMWARE_SYSTEM_STATUS = const(0x00E5)
_VL53L4CD_IDENTIFICATION_MODEL_ID = const(0x010F)

RANGE_VALID = const(0x00)
RANGE_WARN_SIGMA_ABOVE = const(0x01)
RANGE_WARN_SIGMA_BELOW = const(0x02)
RANGE_ERROR_DISTANCE_BELOW_DETECTION_THRESHOLD = const(0x03)
RANGE_ERROR_INVALID_PHASE = const(0x04)
RANGE_ERROR_HW_FAIL = const(0x05)
RANGE_WARN_NO_WRAP_AROUND_CHECK = const(0x06)
RANGE_ERROR_WRAPPED_TARGET_PHASE_MISMATCH = const(0x07)
RANGE_ERROR_PROCESSING_FAIL = const(0x08)
RANGE_ERROR_CROSSTALK_FAIL = const(0x09)
RANGE_ERROR_INTERRUPT = const(0x0A)
RANGE_ERROR_MERGED_TARGET = const(0x0B)
RANGE_ERROR_SIGNAL_TOO_WEAK = const(0x0C)
RANGE_ERROR_OTHER = const(0xFF)


class VL53L4CD:
    """Driver for the VL53L4CD distance sensor."""

    def __init__(self, i2c, address=41):
        self._i2c = i2c
        self._device_address = address
        model_id, module_type = self.model_info
        if model_id != 0xEB or module_type != 0xAA:
            raise RuntimeError(f"Wrong sensor ID ({model_id}) or type!")
        self._ranging = False
        self._sensor_init()

    def _sensor_init(self):
        # pylint: disable=line-too-long
        init_seq = (
            # value    addr : description
            b"\x12"  # 0x2d : set bit 2 and 5 to 1 for fast plus mode (1MHz I2C), else don't touch
            b"\x00"  # 0x2e : bit 0 if I2C pulled up at 1.8V, else set bit 0 to 1 (pull up at AVDD)
            b"\x00"  # 0x2f : bit 0 if GPIO pulled up at 1.8V, else set bit 0 to 1 (pull up at AVDD)
            b"\x11"  # 0x30 : set bit 4 to 0 for active high interrupt and 1 for active low (bits 3:0 must be 0x1)
            b"\x02"  # 0x31 : bit 1 = interrupt depending on the polarity
            b"\x00"  # 0x32 : not user-modifiable
            b"\x02"  # 0x33 : not user-modifiable
            b"\x08"  # 0x34 : not user-modifiable
            b"\x00"  # 0x35 : not user-modifiable
            b"\x08"  # 0x36 : not user-modifiable
            b"\x10"  # 0x37 : not user-modifiable
            b"\x01"  # 0x38 : not user-modifiable
            b"\x01"  # 0x39 : not user-modifiable
            b"\x00"  # 0x3a : not user-modifiable
            b"\x00"  # 0x3b : not user-modifiable
            b"\x00"  # 0x3c : not user-modifiable
            b"\x00"  # 0x3d : not user-modifiable
            b"\xFF"  # 0x3e : not user-modifiable
            b"\x00"  # 0x3f : not user-modifiable
            b"\x0F"  # 0x40 : not user-modifiable
            b"\x00"  # 0x41 : not user-modifiable
            b"\x00"  # 0x42 : not user-modifiable
            b"\x00"  # 0x43 : not user-modifiable
            b"\x00"  # 0x44 : not user-modifiable
            b"\x00"  # 0x45 : not user-modifiable
            b"\x20"  # 0x46 : interrupt configuration 0->level low detection, 1-> level high, 2-> Out of window, 3->In window, 0x20-> New sample ready , TBC
            b"\x0B"  # 0x47 : not user-modifiable
            b"\x00"  # 0x48 : not user-modifiable
            b"\x00"  # 0x49 : not user-modifiable
            b"\x02"  # 0x4a : not user-modifiable
            b"\x14"  # 0x4b : not user-modifiable
            b"\x21"  # 0x4c : not user-modifiable
            b"\x00"  # 0x4d : not user-modifiable
            b"\x00"  # 0x4e : not user-modifiable
            b"\x05"  # 0x4f : not user-modifiable
            b"\x00"  # 0x50 : not user-modifiable
            b"\x00"  # 0x51 : not user-modifiable
            b"\x00"  # 0x52 : not user-modifiable
            b"\x00"  # 0x53 : not user-modifiable
            b"\xC8"  # 0x54 : not user-modifiable
            b"\x00"  # 0x55 : not user-modifiable
            b"\x00"  # 0x56 : not user-modifiable
            b"\x38"  # 0x57 : not user-modifiable
            b"\xFF"  # 0x58 : not user-modifiable
            b"\x01"  # 0x59 : not user-modifiable
            b"\x00"  # 0x5a : not user-modifiable
            b"\x08"  # 0x5b : not user-modifiable
            b"\x00"  # 0x5c : not user-modifiable
            b"\x00"  # 0x5d : not user-modifiable
            b"\x01"  # 0x5e : not user-modifiable
            b"\xCC"  # 0x5f : not user-modifiable
            b"\x07"  # 0x60 : not user-modifiable
            b"\x01"  # 0x61 : not user-modifiable
            b"\xF1"  # 0x62 : not user-modifiable
            b"\x05"  # 0x63 : not user-modifiable
            b"\x00"  # 0x64 : Sigma threshold MSB (mm in 14.2 format for MSB+LSB), default value 90 mm
            b"\xA0"  # 0x65 : Sigma threshold LSB
            b"\x00"  # 0x66 : Min count Rate MSB (MCPS in 9.7 format for MSB+LSB)
            b"\x80"  # 0x67 : Min count Rate LSB
            b"\x08"  # 0x68 : not user-modifiable
            b"\x38"  # 0x69 : not user-modifiable
            b"\x00"  # 0x6a : not user-modifiable
            b"\x00"  # 0x6b : not user-modifiable
            b"\x00"  # 0x6c : Intermeasurement period MSB, 32 bits register
            b"\x00"  # 0x6d : Intermeasurement period
            b"\x0F"  # 0x6e : Intermeasurement period
            b"\x89"  # 0x6f : Intermeasurement period LSB
            b"\x00"  # 0x70 : not user-modifiable
            b"\x00"  # 0x71 : not user-modifiable
            b"\x00"  # 0x72 : distance threshold high MSB (in mm, MSB+LSB)
            b"\x00"  # 0x73 : distance threshold high LSB
            b"\x00"  # 0x74 : distance threshold low MSB ( in mm, MSB+LSB)
            b"\x00"  # 0x75 : distance threshold low LSB
            b"\x00"  # 0x76 : not user-modifiable
            b"\x01"  # 0x77 : not user-modifiable
            b"\x07"  # 0x78 : not user-modifiable
            b"\x05"  # 0x79 : not user-modifiable
            b"\x06"  # 0x7a : not user-modifiable
            b"\x06"  # 0x7b : not user-modifiable
            b"\x00"  # 0x7c : not user-modifiable
            b"\x00"  # 0x7d : not user-modifiable
            b"\x02"  # 0x7e : not user-modifiable
            b"\xC7"  # 0x7f : not user-modifiable
            b"\xFF"  # 0x80 : not user-modifiable
            b"\x9B"  # 0x81 : not user-modifiable
            b"\x00"  # 0x82 : not user-modifiable
            b"\x00"  # 0x83 : not user-modifiable
            b"\x00"  # 0x84 : not user-modifiable
            b"\x01"  # 0x85 : not user-modifiable
            b"\x00"  # 0x86 : clear interrupt, 0x01=clear
            b"\x00"  # 0x87 : ranging, 0x00=stop, 0x40=start
        )
        self._wait_for_boot()
        self._write_register(0x002D, init_seq)
        self._start_vhv()
        self.clear_interrupt()
        self.stop_ranging()
        self._write_register(_VL53L4CD_VHV_CONFIG_TIMEOUT_MACROP_LOOP_BOUND, b"\x09")
        self._write_register(0x0B, b"\x00")
        self._write_register(0x0024, b"\x05\x00")
        self.inter_measurement = 0
        self.timing_budget = 50

    @property
    def model_info(self):
        """A 2 tuple of Model ID and Module Type."""
        info = self._read_register(_VL53L4CD_IDENTIFICATION_MODEL_ID, 2)
        return info[0], info[1]  # Model ID, Module Type

    @property
    def distance(self):
        """The distance in units of centimeters."""
        dist = self._read_register(_VL53L4CD_RESULT_DISTANCE, 2)
        dist = struct.unpack(">H", dist)[0]
        return dist / 10

    @property
    def range_status(self):
        """Measurement validity. If the range status is equal to 0, the distance is valid."""
        status_rtn = [
            RANGE_ERROR_OTHER,
            RANGE_ERROR_OTHER,
            RANGE_ERROR_OTHER,
            RANGE_ERROR_HW_FAIL,
            RANGE_WARN_SIGMA_BELOW,
            RANGE_ERROR_INVALID_PHASE,
            RANGE_WARN_SIGMA_ABOVE,
            RANGE_ERROR_WRAPPED_TARGET_PHASE_MISMATCH,
            RANGE_ERROR_DISTANCE_BELOW_DETECTION_THRESHOLD,
            RANGE_VALID,
            RANGE_ERROR_OTHER,
            RANGE_ERROR_OTHER,
            RANGE_ERROR_CROSSTALK_FAIL,
            RANGE_ERROR_OTHER,
            RANGE_ERROR_OTHER,
            RANGE_ERROR_OTHER,
            RANGE_ERROR_OTHER,
            RANGE_ERROR_OTHER,
            RANGE_ERROR_INTERRUPT,
            RANGE_WARN_NO_WRAP_AROUND_CHECK,
            RANGE_ERROR_OTHER,
            RANGE_ERROR_OTHER,
            RANGE_ERROR_MERGED_TARGET,
            RANGE_ERROR_SIGNAL_TOO_WEAK,
        ]
        status = self._read_register(_VL53L4CD_RESULT_RANGE_STATUS, 1)
        status = struct.unpack(">B", status)[0]
        status = status & 0x1F
        if status < 24:
            status = status_rtn[status]
        else:
            status = RANGE_ERROR_OTHER
        return status

    @property
    def sigma(self):
        """Sigma estimator for the noise in the reported target distance in units of centimeters."""
        sigma = self._read_register(_VL53L4CD_RESULT_SIGMA, 2)
        sigma = struct.unpack(">H", sigma)[0]
        return sigma / 40

    @property
    def timing_budget(self):
        """Ranging duration in milliseconds. Valid range is 10ms to 200ms."""
        osc_freq = struct.unpack(">H", self._read_register(0x0006, 2))[0]

        macro_period_us = 16 * (int(2304 * (0x40000000 / osc_freq)) >> 6)

        macrop_high = struct.unpack(
            ">H", self._read_register(_VL53L4CD_RANGE_CONFIG_A, 2)
        )[0]

        ls_byte = (macrop_high & 0x00FF) << 4
        ms_byte = (macrop_high & 0xFF00) >> 8
        ms_byte = 0x04 - (ms_byte - 1) - 1

        timing_budget_ms = (
            ((ls_byte + 1) * (macro_period_us >> 6)) - ((macro_period_us >> 6) >> 1)
        ) >> 12
        if ms_byte < 12:
            timing_budget_ms >>= ms_byte
        if self.inter_measurement == 0:
            # mode continuous
            timing_budget_ms += 2500
        else:
            # mode autonomous
            timing_budget_ms *= 2
            timing_budget_ms += 4300

        return int(timing_budget_ms / 1000)

    @timing_budget.setter
    def timing_budget(self, val):
        if self._ranging:
            raise RuntimeError("Must stop ranging first.")

        if not 10 <= val <= 200:
            raise ValueError("Timing budget range duration must be 10ms to 200ms.")

        inter_meas = self.inter_measurement
        if inter_meas != 0 and val > inter_meas:
            raise ValueError(
                "Timing budget can not be greater than inter-measurement period ({})".format(
                    inter_meas
                )
            )

        osc_freq = struct.unpack(">H", self._read_register(0x0006, 2))[0]
        if osc_freq == 0:
            raise RuntimeError("Osc frequency is 0.")

        timing_budget_us = val * 1000
        macro_period_us = int(2304 * (0x40000000 / osc_freq)) >> 6

        if inter_meas == 0:
            # continuous mode
            timing_budget_us -= 2500
        else:
            # autonomous mode
            timing_budget_us -= 4300
            timing_budget_us //= 2

        # VL53L4CD_RANGE_CONFIG_A register
        ms_byte = 0
        timing_budget_us <<= 12
        tmp = macro_period_us * 16
        ls_byte = int(((timing_budget_us + ((tmp >> 6) >> 1)) / (tmp >> 6)) - 1)
        while ls_byte & 0xFFFFFF00 > 0:
            ls_byte >>= 1
            ms_byte += 1
        ms_byte = (ms_byte << 8) + (ls_byte & 0xFF)
        self._write_register(_VL53L4CD_RANGE_CONFIG_A, struct.pack(">H", ms_byte))

        # VL53L4CD_RANGE_CONFIG_B register
        ms_byte = 0
        tmp = macro_period_us * 12
        ls_byte = int(((timing_budget_us + ((tmp >> 6) >> 1)) / (tmp >> 6)) - 1)
        while ls_byte & 0xFFFFFF00 > 0:
            ls_byte >>= 1
            ms_byte += 1
        ms_byte = (ms_byte << 8) + (ls_byte & 0xFF)
        self._write_register(_VL53L4CD_RANGE_CONFIG_B, struct.pack(">H", ms_byte))

    @property
    def inter_measurement(self):
        """
        Inter-measurement period in milliseconds. Valid range is timing_budget to
        5000ms, or 0 to disable.
        """
        reg_val = struct.unpack(
            ">I", self._read_register(_VL53L4CD_INTERMEASUREMENT_MS, 4)
        )[0]
        clock_pll = struct.unpack(
            ">H", self._read_register(_VL53L4CD_RESULT_OSC_CALIBRATE_VAL, 2)
        )[0]
        clock_pll &= 0x3FF
        clock_pll = int(1.065 * clock_pll)
        return int(reg_val / clock_pll)

    @inter_measurement.setter
    def inter_measurement(self, val):
        if self._ranging:
            raise RuntimeError("Must stop ranging first.")

        timing_bud = self.timing_budget
        if val != 0 and val < timing_bud:
            raise ValueError(
                "Inter-measurement period can not be less than timing budget ({})".format(
                    timing_bud
                )
            )

        clock_pll = struct.unpack(
            ">H", self._read_register(_VL53L4CD_RESULT_OSC_CALIBRATE_VAL, 2)
        )[0]
        clock_pll &= 0x3FF
        int_meas = int(1.055 * val * clock_pll)
        self._write_register(_VL53L4CD_INTERMEASUREMENT_MS, struct.pack(">I", int_meas))

        # need to reset timing budget so that it will be based on new inter-measurement period
        self.timing_budget = timing_bud

    def start_ranging(self):
        """Starts ranging operation."""
        # start ranging depending inter-measurement setting
        if self.inter_measurement == 0:
            # continuous mode
            self._write_register(_VL53L4CD_SYSTEM_START, b"\x21")
        else:
            # autonomous mode
            self._write_register(_VL53L4CD_SYSTEM_START, b"\x40")

        # wait for data ready
        timed_out = True
        for _ in range(1000):
            if self.data_ready:
                timed_out = False
                break
            time.sleep(0.001)
        if timed_out:
            raise TimeoutError("Time out waiting for data ready.")

        self.clear_interrupt()
        self._ranging = True

    def stop_ranging(self):
        """Stops ranging operation."""
        self._write_register(_VL53L4CD_SYSTEM_START, b"\x00")
        self._ranging = False

    def clear_interrupt(self):
        """Clears new data interrupt."""
        self._write_register(_VL53L4CD_SYSTEM_INTERRUPT_CLEAR, b"\x01")

    @property
    def data_ready(self):
        """Returns true if new data is ready, otherwise false."""
        if (
            self._read_register(_VL53L4CD_GPIO_TIO_HV_STATUS)[0] & 0x01
            == self._interrupt_polarity
        ):
            return True
        return False

    @property
    def _interrupt_polarity(self):
        int_pol = self._read_register(_VL53L4CD_GPIO_HV_MUX_CTRL)[0] & 0x10
        int_pol = (int_pol >> 4) & 0x01
        return 0 if int_pol else 1

    def _wait_for_boot(self):
        for _ in range(1000):
            if self._read_register(_VL53L4CD_FIRMWARE_SYSTEM_STATUS)[0] == 0x03:
                return
            time.sleep(0.001)
        raise TimeoutError("Time out waiting for system boot.")

    def _start_vhv(self):
        self.start_ranging()
        for _ in range(1000):
            if self.data_ready:
                return
            time.sleep(0.001)
        raise TimeoutError("Time out starting VHV.")

    def _write_register(self, address, data, length=None):
        if length is None:
            length = len(data)
        self._i2c.writeto(self._device_address, struct.pack(">H", address) + data[:length])

    def _read_register(self, address, length=1):
        data = bytearray(length)
        self._i2c.writeto(self._device_address, struct.pack(">H", address), False)
        self._i2c.readfrom_into(self._device_address, data)
        return data

    def set_address(self, new_address):
        """
        Set a new I2C address to the instantaited object. This is only called when using
        multiple VL53L4CD sensors on the same I2C bus (SDA & SCL pins). See also the
        `example <examples.html#id2>`_ for proper usage.
        """
        self._write_register(
            _VL53L4CD_I2C_SLAVE_DEVICE_ADDRESS, struct.pack(">B", new_address)
        )
        self._device_address = new_address