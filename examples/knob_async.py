"""
This example shows how to use the ModulinoKnob class to read the value of a rotary encoder knob asynchronously.

Asyncio is used to read the knob value and to blink the built-in LED at the same time.
The knob is used to increase or decrease a value. The knob is rotated clockwise to increase the value and counter-clockwise to decrease it.

You can register callbacks for the following events:
- Press: The knob is pressed.
- Release: The knob is released.
- Rotate clockwise: The knob is rotated clockwise.
- Rotate counter clockwise: The knob is rotated counter clockwise.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoKnob
from machine import Pin
import asyncio

led = Pin("LED_BUILTIN", Pin.OUT)

knob = ModulinoKnob()

knob.on_press = lambda: print("🔘 Pressed!")
knob.on_release = lambda: print("🔘 Released!")
knob.on_rotate_clockwise = lambda steps, value: print(f"🎛️ Rotated {steps} steps clockwise! Value: {value}")
knob.on_rotate_counter_clockwise = lambda steps, value: print(f"🎛️ Rotated {steps} steps counter clockwise! Value: {value}")

async def blink_led():
    while True:
        led.value(0)
        await asyncio.sleep(0.5)
        led.value(1)
        await asyncio.sleep(0.5)
    
async def read_knob():
    while True:
        if(knob.update()):
            print("👀 Knob value or state changed!")
        await asyncio.sleep_ms(20)

async def main():
    await asyncio.gather(
        blink_led(),
        read_knob()
    )

asyncio.run(main())
