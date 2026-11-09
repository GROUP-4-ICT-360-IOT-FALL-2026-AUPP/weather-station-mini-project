#import asyncio
#import ssd1306
#from micropython import const
#
#WIDTH = const(128)
#HEIGHT = const(64)
#
#FREQ = 5
#PERIOD_MS = int(1000/FREQ)
#
#async def main(states, i2c):
#    # TODO: test this on a working display
#    disp = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
#
#    disp.invert(False)  # Toggle this True/False to invert pixels
#    disp.contrast(20)  # Set contrast
#
#    while True:
#        disp.text("hello", 0, 0)  # Set text starting from x=5, y=4 coordinates
#        disp.show()  # Update the display
#        disp.fill(0)  # Make all pixels low (depends on inverted or not)
#        await asyncio.sleep_ms(PERIOD_MS)
