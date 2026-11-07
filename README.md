# Plan

We build a simple weather station that only collects data (no weather prediction or forecasting)

The sensors we will use include:

- DHT11 or DHT22 for temperature and humidity
- Simple rain sensor + guage to detect rain
- Simple anemometer to measure wind speed using a hall effect sensor
- Simple LDR to estimate the brightness, and daylight
- Barometer
- PMS7003 to measure particulates to determine particulates


Each of these sensors will be connected to an ESP32, and the ESP32 will send data to an MQTT broker, where we can then subscribe to it and log it into influx db, and then also view the data using Grafana.

We will also include a telegram bot which you can use to query from the database, and notify users on important readings.

For displaying the data, we will use a simple OLED display at the weather station to display the IP address and some information.

# Concurrency on micropython

So we'll use micropython's builtin asyncio implementation, which uses a coorperative scheduler (so we'll need to be extremely disciplined to make sure that the coroutine must yield, and also must be as non-blocking as possible).

The boilerplate looks something like:

```python
import asyncio
import machine

led = machine.Pin(25, machine.Pin.OUT)

async def blink_led(delay_ms):
    while True:
        led.toggle()
        await asyncio.sleep_ms(delay_ms) 

async def read_sensor():
    while True:
        print("Reading sensor data...")
        await asyncio.sleep(2) 

async def main():
    task1 = asyncio.create_task(blink_led(500))
    task2 = asyncio.create_task(read_sensor())
    while True:
        await asyncio.sleep(1)

asyncio.run(main())
```

Alternatively, we can do:

```python
async def main():
    await asyncio.gather(
        oled_task(oled),
        mqtt_task(),
        temperature_task(),
        humidity_task()
    )

asyncio.run(main())
```

Given that the tasks are all `async` functions.

