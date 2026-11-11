import asyncio
from bmp280 import BMP280

FREQ = 1
PERIOD_MS = int(1000/FREQ)

async def main(states, i2c):
    bmp280 = BMP280(i2c)
    while True:
        data = {
                "temperature": bmp280.temperature,
                "pressure": bmp280.pressure,
                "altitude": bmp280.altitude
        }
        states["bmp280"] = data
        await asyncio.sleep_ms(PERIOD_MS)
