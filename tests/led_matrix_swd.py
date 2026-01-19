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
# Should still be 'GS4'
if dat[1:4] == b'GS4':
    print("PASS: Device responded correctly.")
else:
    print(f"FAIL: Unexpected device response: {dat}")