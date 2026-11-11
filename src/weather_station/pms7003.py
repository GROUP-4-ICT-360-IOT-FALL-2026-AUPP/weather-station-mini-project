import asyncio
from machine import ADC, Pin

FREQ = 1
PERIOD_MS = int(1000/FREQ)

def validate_checksum(frame):
    if len(frame) != 32:
        return False

    calculated = sum(frame[:30]) & 0xFFFF

    received = (frame[30] << 8) | frame[31]

    return calculated == received

async def main(states, uart):
    while True:
        await asyncio.sleep_ms(PERIOD_MS)
        if not uart.any():
            continue
        raw_data = uart.read(32)

        # first check is that they're of length 32
        if len(raw_data) != 32:
            continue

        #print("[pms7003] length ok")
        # pointer always point to the next byte to read
        pointer = 0
        
        # now check that the first and second byte is valid
        if not (raw_data[pointer] == 0x42 and raw_data[pointer + 1] == 0x4d):
            continue
        # now compute checksum

        #print("[pms7003] header ok")

        if not validate_checksum(raw_data):
            continue

        #print("[pms7003] checksum ok")
        pointer += 2
        # now we start parsing the data
        data = dict()
        #data["raw_data"] = raw_data

        data["frame_length"] = raw_data[pointer] << 8 | raw_data[pointer + 1]
        pointer += 2

        data_contents = [
            "PM1.0(CF=1)",
            "PM2.5(CF=1)",
            "PM10(CF=1)",
            "PM1.0(CF=ATM)",
            "PM2.5(CF=ATM)",
            "PM10(CF=ATM)",
            "#particles > 0.3um in 0.1L air",
            "#particles > 0.5um in 0.1L air",
            "#particles > 1.0um in 0.1L air",
            "#particles > 2.5um in 0.1L air",
            "#particles > 5.0um in 0.1L air",
            "#particles > 10.0um in 0.1L air",
        ]

        for data_content in data_contents:
            data[data_content] = raw_data[pointer] << 8 | raw_data[pointer + 1]
            pointer += 2

        states["pms7003"] = data
