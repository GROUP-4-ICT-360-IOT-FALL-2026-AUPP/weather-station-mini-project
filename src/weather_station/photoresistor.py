import asyncio
from machine import ADC, Pin
import math

FREQ = 1
PERIOD_MS = int(1000/FREQ)
PIN = 1

PULL_DOWN_RESISTANCE = 66_500

async def main(states):
    adc = ADC(Pin(PIN))
    while True:
        raw_value = adc.read_u16()
        voltage = raw_value * 3.3 / 65535
        # we can determine the resistance of the photoresistor by the following formula:
        # R_p = (\frac{V}{V_o} - 1) R
        if voltage == 0:
            photoresistor_resistance = math.inf
        else:
            photoresistor_resistance = (3.3/voltage - 1) * PULL_DOWN_RESISTANCE
        #print(f"[photoresistor] hello at {FREQ} Hz!")
        states["photoresistor"] = photoresistor_resistance
        await asyncio.sleep_ms(PERIOD_MS)
