import asyncio
import machine
import photoresistor
import voltage
import serial_logger
import dht11

states = {
    "voltage": None,
    "photoresistor": None,
    "dht11": None
}

async def main():
    await asyncio.gather(
        serial_logger.main(states),
        photoresistor.main(states),
        voltage.main(states),
        dht11.main(states)
    )

asyncio.run(main())
