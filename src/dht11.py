import asyncio
from machine import ADC, Pin
import dht

FREQ = 1
PERIOD_MS = int(1000/FREQ)

PIN = 10


async def main(states):
    dht11 = dht.DHT11(Pin(PIN))
    while True:
        try:
            dht11.measure()
            measurement = dict()
            measurement["temperature"] = dht11.temperature()
            measurement["humidity"] = dht11.humidity()
            states["dht11"] = measurement
            await asyncio.sleep_ms(PERIOD_MS)
        except OSError as e:
            print("[dht11] got error: ", e)
