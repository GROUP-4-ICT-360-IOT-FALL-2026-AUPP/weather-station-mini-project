import asyncio
from machine import ADC, Pin

FREQ = 1
PERIOD_MS = int(1000/FREQ)

PIN = 3

async def main(states):
    adc = ADC(Pin(PIN))
    while True:
        raw_value = adc.read_u16()
        states["rain_sensor"] = raw_value
        await asyncio.sleep_ms(PERIOD_MS)
