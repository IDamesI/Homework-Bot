from balethon import Client
from balethon.conditions import at_state, private
import json
import time
import datetime
import sched

bot = Client("256476940:IpEpljA2aWSOCbFYSPGgs7sDmS38EOuN5tPqLdE7")


def handle_remind():
    with bot:
        bot.send_document(1215365851, "admins-class.json", "admins-class.json")
        bot.send_document(1215365851, "admins.json", "admins.json")
        bot.send_document(1215365851, "chatids.json", "chatids.json")
        bot.send_document(1215365851, "classes.json", "classes.json")
        bot.send_document(1215365851, "homework-db.json", "homework-db.json")


def schedule_reminder():
    # Tehran timezone offset from UTC (3.5 hours)
    tehran_offset = 3.5 * 60 * 60  # Convert to seconds

    # Get current UTC time
    now = datetime.datetime.utcnow()

    # Calculate desired schedule time in Tehran time (3:00 PM)
    desired_time = datetime.datetime(now.year, now.month, now.day, 17, 00)  # 3:00 PM

    # Adjust the schedule time based on Tehran time offset
    if desired_time < now:
        # Desired time has already passed today, so schedule for tomorrow
        desired_time += datetime.timedelta(days=1)
    schedule_time = desired_time - datetime.timedelta(seconds=tehran_offset)

    # Calculate the time remaining until the next schedule
    delay = (schedule_time - now).total_seconds()

    # Schedule the reminder function call
    scheduler.enter(delay, 1, handle_remind)

    # Schedule the scheduler itself to run again in 24 hours
    scheduler.enter(24 * 60 * 60, 1, schedule_reminder)


scheduler = sched.scheduler(time.time, time.sleep)
schedule_reminder()
scheduler.run(blocking=True)
