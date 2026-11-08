import asyncio

FREQ = 1
PERIOD_MS = int(1000/FREQ)

async def main(states):
    while True:
        print(states)
        await asyncio.sleep_ms(PERIOD_MS)
