import datetime
import os

import pandas as pd
from matplotlib import pyplot as plt

from garmin_dashboard import auth

# init
garmin = auth.init_api()
os.makedirs("data/charts", exist_ok=True)

# set params
today = datetime.date.today()
startdate = today - datetime.timedelta(days=7)  # past week
date_all = [
    startdate + datetime.timedelta(days=x) for x in range((today - startdate).days + 1)
]


def _plot(name, kind, df):
    df.plot(kind=kind)

    plt.title(name)
    plt.xticks(rotation=45)

    plt.savefig(f"data/charts/{name}.png")

    return plt


def body_battery():
    df = pd.DataFrame(garmin.get_body_battery(startdate.isoformat(), today.isoformat()))
    df = df[["date", "charged", "drained"]].set_index("date")

    return _plot(name="Body Battery", kind="bar", df=df)


def resting_heart_rate():
    r = []
    for date in date_all:
        r.append(garmin.get_rhr_day(date.isoformat()))

    r_filtered = []
    for i in r:
        try:
            d = {
                "date": i["statisticsStartDate"],
                "restingHeartRate": i["allMetrics"]["metricsMap"][
                    "WELLNESS_RESTING_HEART_RATE"
                ][0]["value"],
            }
            r_filtered.append(d)
        except KeyError:
            pass

    df = pd.DataFrame(r_filtered).set_index("date")

    return _plot(name="Resting Heart Rate", kind="line", df=df)


def sleep():
    r = []
    for date in date_all:
        r.append(garmin.get_sleep_data(date.isoformat()))

    r_filtered = []
    for i in r:
        try:
            d = {
                "date": i["dailySleepDTO"]["calendarDate"],
                "deep": i["dailySleepDTO"]["deepSleepSeconds"],
                "light": i["dailySleepDTO"]["lightSleepSeconds"],
                "rem": i["dailySleepDTO"]["remSleepSeconds"],
                "awake": i["dailySleepDTO"]["awakeSleepSeconds"],
            }
            r_filtered.append(d)
        except KeyError:
            pass

    df = pd.DataFrame(r_filtered).set_index("date")

    return _plot(name="Sleep", kind="area", df=df)


def stress():
    r = []
    for date in date_all:
        r.append(garmin.get_stress_data(date.isoformat()))

    r_filtered = []
    for i in r:
        try:
            d = {
                "date": i["calendarDate"],
                "max": i["maxStressLevel"],
                "avg": i["avgStressLevel"],
            }
            r_filtered.append(d)
        except KeyError:
            pass

    df = pd.DataFrame(r_filtered).set_index("date")

    return _plot(name="Stress", kind="bar", df=df)
