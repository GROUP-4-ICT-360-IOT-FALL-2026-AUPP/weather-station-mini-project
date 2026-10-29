# Plan

This project consists of 2 main parts:

- outdoor monitoring
- indoor monitoring

## Outdoor monitoring

We build a simple weather station that only collects data (no weather prediction or forecasting)

The sensors we will use include:

- DHT11 or DHT22 for temperature and humidity
- Simple rain sensor + guage to detect rain
- Simple anemometer to measure wind speed using a hall effect sensor
- Simple LDR to estimate the brightness, and daylight
- Barometer

## Indoor monitoring

In indoors, we will use:

- DHT11 or DHT22 for temperature and humidity
- PMS7003 to measure particulates
- SGP40 to estimate overall TVOC
- SCD30 to estimate CO2 concentration in homes

Each of these sensors will be connected to an ESP32, and the ESP32 will send data to an MQTT broker, where we can then subscribe to it and log it into influx db, and then also view the data using Grafana.

We will also include a telegram bot which you can use to query from the database, and notify you of any abnormal readings.
