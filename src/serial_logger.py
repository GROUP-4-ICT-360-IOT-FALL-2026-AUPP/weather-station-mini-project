import asyncio

FREQ = 1
PERIOD_MS = int(1000/FREQ)

async def main(states, i2c):
    while True:
        #print(states)
        await asyncio.sleep_ms(PERIOD_MS)
