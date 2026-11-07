import asyncio

FREQ = 1
PERIOD_MS = int(1000/FREQ)
async def main():
    while True:
        print(f"[photoresistor] hello at {FREQ} Hz!")
        await asyncio.sleep_ms(PERIOD_MS)
