import asyncio
import network
import env

# NOTE:
# env.WIFI_CREDENTIALS = [
#     (ssid1, password1),
#     (ssid2, password2),
#     ...
# ]

#FREQ = 1
PERIOD_MS = 1_000

async def main(states, wlan):
    wifi_credientials_index = 0
    wlan.active(False)
    wlan.active(True)

    while True:
        # if it's connected, that's fine
        if wlan.isconnected():
            states["private_ip"] = wlan.ifconfig()[0]
        # if it's not connected
        elif wlan.status() != network.STAT_CONNECTING:
            try:
                print(f"[wifi] Attempting to connect to {env.WIFI_CREDENTIALS[wifi_credientials_index][0]}")
                ssid, password = env.WIFI_CREDENTIALS[wifi_credientials_index]
                wlan.connect(ssid, password)
            except Exception as e:
                print("[wifi] Connection error:", repr(e))
                wlan.active(False)
                wlan.active(True)
                wifi_credientials_index = (wifi_credientials_index + 1) % len(env.WIFI_CREDENTIALS)
        await asyncio.sleep_ms(PERIOD_MS)
