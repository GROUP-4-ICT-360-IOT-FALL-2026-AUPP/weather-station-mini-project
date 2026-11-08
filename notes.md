# Choosing resistor values 

## Voltage Divider

KVL states:

$$
V = V_1 + V_2
$$

We measure $V_2$, and we want to know $V$

$$
V = \frac{V_2 R_1}{R_2} + V_2
$$


$$
V = \left(\frac{R_1}{R_2} + 1)V_2
$$

the idea is that $V_2$ is capped based on the logic level of the MCU's ADC.


In our case, we need:

$$
V_2 \leq 3.3 V
$$

If we also place the constraint that $V \leq V_{bat}$, then we can solve for the valid range for the ratio $K = \frac{R_1}{R_2}$.

A graphical method to determine this $K$ value can be used using [this Desmos graph](https://www.desmos.com/calculator/sagrdbpkkw).

### Determining K experimentally

So want to determine the actual value of $K = \frac{R_1}{R_2}$ but let's say that we can't measure it directly. If we have a trusted multimeter, we can then determine the $K$ value directly.

What we have so far is that we measured that $V_r = 1.837 V$, and we know that $V = 3.32V$, so solving for $K$:

$$
\frac{V}{V_r} - 1 = K = \frac{3.32}{1.837} - 1 = 0.8073
$$

> [!NOTE]
> idk why but it doesn't follow it linearly (it's close, but error starts to grow)

## Voltage Divider for battery readings

So because our battery is directly connected to the ESP32 breakout board, we should only supply a voltage of around 6V and below (one lithium ion cell is good)

Using a 1 to 1 voltage divider should be good (almost the best resolution).

## Voltage dividier for photoresistor

In our case, we want to estimate the resistance of the photoresistor, and then try to categorize the brightness into:

- high brightness (afternoon sunshine)
- brightness (sunshine)
- medium brightness (sunset)
- low brightness (cloudy weather)
- very low brightness (night)

So let's start with estimating resistance. We start with a lowerbound that says that $R_p \geq R_{min}$

We want to choose $R$, as a value of our voltage divider. We measure $V_o$, and $V$ is going to be the voltage coming out of the MCU.

$$
V = I R + V_o
$$

$$
V_o = I R_p
$$

$$
V = \frac{R_p}{R} V_o + V_o
$$

We want to determine how $R_p$ changes as $V_o$ changes

$$
R_p = (\frac{V}{V_o} - 1) R
$$

So it's a weird non-linear relationship. We need to determine $R$ so that we get the desired ranges.

From our measurements:

- very close to the desk lamp: 150 ohms
- fairly close to the bulb: 1K ohms
- at the distance from the desk from the bulb: 3k
- normal room: 150k
- in shade: 1.5M ohms
- dark room: 3M ohms
- complete darkness: 100M ohms

I think selecting a resistor of $67K\Ohm$ should provide decent range.



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

# Reading from sensors

Repositories are stored [here](https://github.com/micropython/micropython-lib/tree/master/micropython/drivers).

## I2C

So we kinda have no choice but to send addresses to the registers directly, because there aren't really any libraries (plus, i don't think it's too bad)

Our I2C sensors include:

- bmp280 (this is probably fine)
- oled (this might be tough, so we might need a library)

We can find this here:

- [oled driver](https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/display/ssd1306)

## UART

- PMS7003

Not sure how to talk to the air quality sensor, so we're going to need to think about that

## DHT

micropython already has a built in DHT11 library

## ADC

that's also fine, DHT11 has analog library. This covers:

- photoresistor
- battery voltage reading
- rain sensor
- hall effect sensor


