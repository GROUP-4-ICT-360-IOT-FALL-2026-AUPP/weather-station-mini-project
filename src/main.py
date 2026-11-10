import asyncio
import photoresistor
import voltage
import serial_logger
import dht11
from machine import UART, Pin, I2C
import bmp280_poller
import rain_sensor
import oled
import pms7003
import mqtt

SDA_PIN = 8
SCL_PIN = 9

i2c =  I2C(
    0,
    sda = Pin(SDA_PIN),
    scl = Pin(SCL_PIN),
    freq = 100_000
)

# we will use UART for reading the pms7003 which outputs at a maximum of 200ms intervals, 
# so if we happened to chime in mid frame, we want to exit out of it if we haven't received like in (1/9600)*8 seconds (I'll do 5ms just to be safe, this shouldn't affect the other processes too much)

UART_TIMEOUT_MS = 5

uart1 = UART(1, baudrate=9600, rx=6, tx=7, timeout=UART_TIMEOUT_MS)

states = {
    "voltage": None,
    "photoresistor": None,
    "dht11": None,
    "bmp280": None,
    "rain_sensor": None,
    "pms7003": None
}

async def main():
    await asyncio.gather(
        serial_logger.main(states, i2c),
        photoresistor.main(states),
        rain_sensor.main(states),
        voltage.main(states),
        dht11.main(states),
        bmp280_poller.main(states, i2c),
        pms7003.main(states, uart1),
        mqtt.main(states),
        oled.main(states, i2c)
    )
    #await oled.main(states, i2c)

asyncio.run(main())
