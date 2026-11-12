# Plan

We build a simple weather station that only collects data (no weather prediction or forecasting)

The sensors we will use include:

- DHT11 or DHT22 for temperature and humidity
- Simple rain sensor + guage to detect rain
- Simple anemometer to measure wind speed using a hall effect sensor
- Simple LDR to estimate the brightness, and daylight
- Barometer
- PMS7003 to measure particulates to determine particulates


Each of these sensors will be connected to an ESP32, and the ESP32 will send data to an MQTT broker, where we can then subscribe to it and log it into influx db, and then also view the data using Grafana.

We will also include a telegram bot which you can use to query from the database, and notify users on important readings.

For displaying the data, we will use a simple OLED display at the weather station to display the IP address and some information.

# Flashing micropython

We download micropython from [here](https://micropython.org/download/ESP32_GENERIC_C3/). 

In our case, since our ESP32 C3 shows up as `/dev/ttyACM1`

First:

```
uv tool run esptool erase_flash
```

Then:

```
uv tool run esptool write_flash 0 ./ESP32_GENERIC_C3-20260824-v1.29.0.bin
```

Now:

```
tio -b 115200 /dev/ttyACM1
```

should give you a python shell.


To list all files:

```
mpremote connect /dev/ttyACM1 ls
```

To install the libraries to the esp32:

```
./install /dev/ttyACM1
```

To transfer our code to the esp32, do:

```
./transfer /dev/ttyACM1
```

# Setting up influxdb on a Linux server

We will follow the [official guide](https://docs.influxdata.com/influxdb/v2/install/#install-linux).

After which, we can enable the `influxdb` service as such:

```
sudo systemctl enable --now influxdb
```

Set it up, create an API token and then store it in `env.py`. `env.py` should look something like:

```
INFLUXDB_TOKEN = "..."
TELEGRAM_BOT_TOKEN = "..."
TELEGRAM_CHAT_ID = [
  "..."
]
```

Make sure you have access to your github repository (adding a deploy key would be recommended)

Clone the repository and then go to the `base_station` directory, create a virtual environment and then run:

```
pip install -r requirements.txt
```

We can then run the middle man:

```
python ./main.py
```

> [!NOTE]
> you can make a service, or add it to your crontab to start it automatically on reboot

# Setting up grafana

We will follow the steps [here](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/)

Afterwards, we start it:

```
sudo systemctl start --now grafana-server
```

Now go to `http://<raspberry-pi-ip>:3000`, and connect an `influxdb` datasource.

Now write flux queries of this form to visualize the data:

```
from(bucket: "local-weather-station-v1")
    |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
    |> filter(fn: (r) =>
        r._measurement == "pms7003" and
        r._field == "PM2.5(CF=ATM)"
    )
    |> map(fn: (r) => ({
        r with
        category: if r._value <= 5 then "Excellent (WHO's recommended)"
                  else if r._value <= 15 then "Good"
                  else if r._value <= 25 then "Moderate"
                  else if r._value <= 37.5 then "Poor"
                  else if r._value <= 50 then "Very poor"
                  else if r._value <= 75 then "Severe"
                  else "Extremely severe"
    }))
```

# Telegram Bot

The telegram bot should do 3 things:

- Give a daily reading of yesterday's weather (average temperature, rain period, highest temperature)
- Handle user commands (simple queries)
  - for now, just have a `/status` that just gives the current state of the weather
- Give notification of notable events (rain detected, bad air quality) but only doing it once every day or so such that it doesn't flood the notification

## Usage

To run the telegram bot, simply run `telegram_bot.py`


