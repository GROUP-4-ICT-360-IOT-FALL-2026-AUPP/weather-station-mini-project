import asyncio
import ssd1306
from micropython import const

WIDTH = const(128)
HEIGHT = const(64)

FREQ = 5
PERIOD_MS = int(1000/FREQ)

# the text is 8x8 pixel
TEXT_SIZE = 8
MAX_CHAR_HORIZONTAL = int(WIDTH/TEXT_SIZE)
MAX_CHAR_VERTICAL = int(HEIGHT/TEXT_SIZE)

VERTICAL_MARGIN = 1

def extract_text_to_display(states):
    text_to_display = []
    if states["dht11"] is not None:
        temperature = states["dht11"]["temperature"]
        if states["bmp280"] is not None:
            # prefer to use the bmp280 for temperature
            temperature = states["bmp280"]["temperature"]
        text_to_display.append(f"T:{temperature}C|RH:{states["dht11"]["humidity"]}%")
    if states["bmp280"] is not None:
        text_to_display.append(f"P:{states["bmp280"]["pressure"]}Pa")
    if states["photoresistor"] is not None:
        text_to_display.append("LDR:{}".format(
            states["photoresistor"]
        ))
    if states["rain_sensor"] is not None:
        text_to_display.append("RAIN:{}".format(
            states["rain_sensor"]
        ))
    if states["pms7003"] is not None:
        text_to_display.append(f"PM1.0:{states["pms7003"]["PM1.0(CF=ATM)"]}ug/m3")
        text_to_display.append(f"PM2.5:{states["pms7003"]["PM2.5(CF=ATM)"]}ug/m3")
        text_to_display.append(f"PM10:{states["pms7003"]["PM10(CF=ATM)"]}ug/m3")
    return text_to_display

async def main(states, i2c):
    # TODO: test this on a working display
    disp = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
    disp.invert(False)  # Toggle this True/False to invert pixels
    disp.contrast(20)  # Set contrast
    while True:
        disp.fill(0)
        display_text = extract_text_to_display(states)
        for i, line in enumerate(display_text[:MAX_CHAR_VERTICAL]):
            disp.text(line[:MAX_CHAR_HORIZONTAL], 0, VERTICAL_MARGIN + i*(VERTICAL_MARGIN + TEXT_SIZE))
        disp.show()
        await asyncio.sleep_ms(PERIOD_MS)
