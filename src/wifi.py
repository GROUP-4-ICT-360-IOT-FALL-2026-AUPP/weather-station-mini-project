import asyncio
import network
import env

#FREQ = 1
PERIOD_MS = 1_000

async def main(states, wlan):
    wlan.active(False)
    wlan.active(True)
    while True:
        # if it's connected, that's fine
        if wlan.isconnected():
            states["private_ip"] = wlan.ifconfig()[0]
        # if it's not connected
        elif wlan.status() != network.STAT_CONNECTING:
            try:
                print("[wifi] Attempting to connect to wifi")
                wlan.connect(env.WIFI_SSID, env.WIFI_PASSWORD)
            except Exception as e:
                print("[wifi] Connection error:", repr(e))
        await asyncio.sleep_ms(PERIOD_MS)
