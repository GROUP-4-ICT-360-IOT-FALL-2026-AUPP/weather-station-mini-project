import asyncio
import machine
import photoresistor
import voltage

async def main():
    await asyncio.gather(
        photoresistor.main(),
        voltage.main()
    )

asyncio.run(main())
