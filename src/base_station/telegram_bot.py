from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler
from influxdb_client import InfluxDBClient
import env
import datetime
import time


RAIN_CHECKER_INTERVAL = 60
RAIN_THRESHOLD = 50000
RAIN_NOTIFICATION_INTERVAL = 60*60*4
RAIN_NOTIFICATION_LAST_SENT = 0

AIR_QUALITY_CHECKER_INTERVAL = 360
AIR_QUALITY_NOTIFICATION_INTERVAL = 60*60*4
AIR_QUALITY_NOTIFICATION_LAST_SENT = 0
BAD_AIR_QUALITY_THRESHOLD = 12


client = InfluxDBClient(
    url="http://localhost:8086",
    token=env.INFLUXDB_TOKEN,
    org="k1mch1"
)

query_api = client.query_api()

def query_measurement_and_field(measurement, field):
    query = f'''
    from(bucket: "local-weather-station-v1")
        |> range(start: 0)
        |> filter(fn: (r) => r._measurement == "{measurement}")
        |> filter(fn: (r) => r._field == "{field}")
        |> group()
        |> last()
    '''

    tables = query_api.query(query)
    records = [
        record
        for table in tables
        for record in table.records
    ]
    return records[0].get_value() if records else None

def query_all_measurements():
    query = '''
    from(bucket: "local-weather-station-v1")
    |> range(start: -1h)
    |> last()
    '''

    tables = query_api.query(query)
    reply_text = ""
    for table in tables:
        for record in table.records:
            reply_text += f"{record.get_field()} ({record.get_measurement()}) : {record.get_value()}\n"
    return reply_text

async def status(update: Update, context):
    measurements = query_all_measurements()
    if measurements == "":
        return
    await update.message.reply_text(
        measurements
    )

async def help_command(update: Update, context):
    await update.message.reply_text(
        "Available commands:\n"
        "/status - Station status\n"
    )


async def post_init(application):
    await application.bot.set_my_commands([
        BotCommand("status", "Show station status"),
        BotCommand("help", "Show available commands")
    ])

async def periodic_report(context):
    for chat_id in env.TELEGRAM_CHAT_ID:
        print(f"sending to {chat_id}")
        await context.bot.send_message(
            chat_id=chat_id,
            text=query_all_measurements()
        )

async def air_quality_checker(context):
    global AIR_QUALITY_NOTIFICATION_LAST_SENT
    reading = query_measurement_and_field("pms7003", "PM2.5(CF=ATM)")
    if reading is None or reading <= BAD_AIR_QUALITY_THRESHOLD:
        return
    if time.time() - AIR_QUALITY_NOTIFICATION_LAST_SENT <= AIR_QUALITY_NOTIFICATION_INTERVAL:
        return
    for chat_id in env.TELEGRAM_CHAT_ID:
        print(f"Sending bad air quality notification to {chat_id}")
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Bad air quality detected! PM2.5 is {reading} ug/m3"
        )
    AIR_QUALITY_NOTIFICATION_LAST_SENT = time.time()

async def rain_checker(context):
    global RAIN_NOTIFICATION_LAST_SENT
    reading = query_measurement_and_field("rain_sensor", "rain_sensor")
    if reading is None or reading >= RAIN_THRESHOLD:
        return
    if time.time() - RAIN_NOTIFICATION_LAST_SENT <= RAIN_NOTIFICATION_INTERVAL:
        return
    for chat_id in env.TELEGRAM_CHAT_ID:
        print(f"Sending rain notification notification to {chat_id}")
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Rain detected! ADC reading is {reading}"
        )
    RAIN_NOTIFICATION_LAST_SENT = time.time()

app = (
    Application.builder()
    .token(env.TELEGRAM_BOT_TOKEN)
    .post_init(post_init)
    .build()
)

app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("help", help_command))

app.job_queue.run_repeating(
    rain_checker,
    interval=RAIN_CHECKER_INTERVAL,
    first=0
)

app.job_queue.run_repeating(
    air_quality_checker,
    interval=AIR_QUALITY_CHECKER_INTERVAL,
    first=0
)


app.job_queue.run_daily(
    periodic_report,
    time=datetime.time(hour=8, minute=0)
)

app.run_polling()

