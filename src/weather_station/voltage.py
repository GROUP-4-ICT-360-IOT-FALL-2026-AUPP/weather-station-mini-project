import asyncio
from machine import ADC, Pin

FREQ = 1
PERIOD_MS = int(1000/FREQ)

PIN = 0

# assume our circuit is 
# bat -> r1 --read here-> r2 -> gnd
# call that V_r

#R_1 = 65_000
#R_2 = 58_000

K = 0.8073

# we can find the voltage of the battery as such:
# V = \frac{V_r R_1}{R_2} + V_2


async def main(states):
    adc = ADC(Pin(PIN))
    while True:
        raw_value = adc.read_u16()
        v_r = 3.3 * raw_value / ((1 << 16) - 1)
        v_bat = v_r * (K + 1)
        states["voltage"] = v_bat
        await asyncio.sleep_ms(PERIOD_MS)
