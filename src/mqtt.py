import asyncio
import network
from umqtt.simple import MQTTClient
import env
import json

PERIOD_MS = 5_000

MQTT_TOPIC_PUB = b"aupp/local-weather-station"
MQTT_CLIENT_ID = "weather-station-v1"
MQTT_BROKER = "public-mqtt-broker.bevywise.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60


def create_mqtt_client():
    return MQTTClient(
        client_id=MQTT_CLIENT_ID,
        server=MQTT_BROKER,
        port=MQTT_PORT,
        keepalive=MQTT_KEEPALIVE
    )

def discard_mqtt_client(client):
    if client is not None:
        try:
            client.disconnect()
        except Exception:
            pass


async def main(states):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(env.WIFI_SSID, env.WIFI_PASSWORD)

    mqtt_client = None

    while True:
        await asyncio.sleep_ms(PERIOD_MS)

        if not wlan.isconnected():
            if mqtt_client is not None:
                print("[mqtt] WiFi lost. Discarding MQTT connection.")
                discard_mqtt_client(mqtt_client)
                mqtt_client = None

            # Don't restart an ongoing WiFi connection attempt
            if wlan.status() != network.STAT_CONNECTING:
                print("[wifi] Attempting reconnection...")
                try:
                    wlan.connect(env.WIFI_SSID, env.WIFI_PASSWORD)
                except Exception as e:
                    print("[wifi] Connection error:", repr(e))

            continue

        if mqtt_client is None:
            print("[mqtt] Connecting to broker...")

            try:
                mqtt_client = create_mqtt_client()
                mqtt_client.connect()
                print("[mqtt] Connected!")

            except Exception as e:
                print("[mqtt] Connection failed:", repr(e))
                discard_mqtt_client(mqtt_client)
                mqtt_client = None
                continue

        try:
            payload = json.dumps(states)
            mqtt_client.publish(MQTT_TOPIC_PUB, payload)
            print("[mqtt] Published successfully")

        except Exception as e:
            print("[mqtt] Publish failed:", repr(e))
            discard_mqtt_client(mqtt_client)
            mqtt_client = None
