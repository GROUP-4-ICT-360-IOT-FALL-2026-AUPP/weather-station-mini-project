import asyncio
import machine
import photoresistor
import voltage
import serial_logger

states = {
    "voltage": None,
    "photoresistor": None
}

async def main():
    await asyncio.gather(
        serial_logger.main(states),
        photoresistor.main(states),
        voltage.main(states)
    )

asyncio.run(main())
