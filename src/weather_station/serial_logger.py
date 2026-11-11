import asyncio

FREQ = 1
PERIOD_MS = int(1000/FREQ)

async def main(states, i2c):
    while True:
        print(states)
        #print(i2c.scan())
        await asyncio.sleep_ms(PERIOD_MS)
