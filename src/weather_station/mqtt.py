import asyncio
from umqtt.simple import MQTTClient
import json

#FREQ = 0.2
PERIOD_MS = 5_000

MQTT_TOPIC_PUB = b"aupp/local-weather-station"
MQTT_CLIENT_ID = "weather-station-v1"
MQTT_BROKER = "public-mqtt-broker.bevywise.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60


async def main(states, wlan):
    # a client of None means that that it's not connected yet
    mqtt_client = None
    while True:
        await asyncio.sleep_ms(PERIOD_MS)
        if not wlan.isconnected():
            continue
        # if it's connected to wifi, then try to connect to mqtt
        if mqtt_client is None:
            try:
                mqtt_client = MQTTClient(
                    client_id=MQTT_CLIENT_ID,
                    server=MQTT_BROKER,
                    port=MQTT_PORT,
                    keepalive=MQTT_KEEPALIVE
                )
                mqtt_client.connect()
                print("[mqtt] Connected!")
            except Exception as e:
                print("[mqtt] Connection failed:", repr(e))
                mqtt_client = None
                continue
        try:
            payload = json.dumps(states)
            mqtt_client.publish(MQTT_TOPIC_PUB, payload)
            print("[mqtt] Published successfully")
        except Exception as e:
            print("[mqtt] Publish failed:", repr(e))
            try:
                mqtt_client.disconnect()
            except Exception:
                pass
            mqtt_client = None
