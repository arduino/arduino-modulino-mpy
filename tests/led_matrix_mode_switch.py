"""
Script for testing the mode switching of the LED matrix.
The test sends the command to switch to GS4 mode and then reads back the first 4 bytes of the device response.
If the response does not contain 'GS4', it indicates that the device reset after receiving the command, 
which would suggest CPU starvation in the LED matrix firmware due to tight IRQ handling.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""
from machine import I2C
from time import sleep_ms

bus = I2C(0)
dev_addr = 0x39

buffer = b'GS4'
buffer += b'\x00' * (12 - len(buffer))
bus.writeto(dev_addr, buffer)
sleep_ms(500)

dat = bus.readfrom(dev_addr, 4)
print(dat)
sleep_ms(500)
dat = bus.readfrom(dev_addr, 4)

# Should still be 'GS4' (first byte is pin strap address)
if dat[1:4] == b'GS4':
    print("PASS: Device responded correctly.")
else:
    print(f"FAIL: Unexpected device response: {dat}")