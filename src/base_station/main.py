import env
import json
from datetime import datetime, UTC
import pprint

from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.subscribe as subscribe
from influxdb_client import InfluxDBClient

MQTT_BROKER = "public-mqtt-broker.bevywise.com"
MQTT_PORT = 1883
MQTT_TOPIC_SUB = "aupp/local-weather-station"
MQTT_CLIENT_ID = "base-station-v1"

URL = "http://localhost:8086"
ORG = "k1mch1"
BUCKET = "local-weather-station-v1"
TOKEN = env.INFLUXDB_TOKEN

def main():
    with InfluxDBClient(url=URL, token=TOKEN, org=ORG) as client:
            with client.write_api(write_options=SYNCHRONOUS) as write_api:
                while True:
                    msg = subscribe.simple(MQTT_TOPIC_SUB, hostname=MQTT_BROKER, port=MQTT_PORT)
                    if msg.payload == None:
                        continue
                    payload = json.loads(msg.payload)
                    for k, v in payload.items():
                        field = v
                        if type(v) != dict:
                            field = {
                                k:v
                        }
                        data_point = {
                            "measurement": k,
                            "tags": {
                                "server": "raspberry pi base station"
                            },
                            "fields": field,
                            "time": datetime.now(UTC)
                        }
                        write_api.write(
                            bucket=BUCKET,
                            record=data_point
                        )
                        print(f"measurement: {k}")
                        pprint.pprint(field)

if __name__ == "__main__":
    while True:
        try:
            main()
        except:
            pass
