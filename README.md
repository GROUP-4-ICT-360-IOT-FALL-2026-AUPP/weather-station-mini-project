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
