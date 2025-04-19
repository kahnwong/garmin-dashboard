import json
import logging
import os
import datetime
from pprint import pprint
from matplotlib import pyplot as plt
from garminconnect import (
    Garmin,
)
import pandas as pd
import os

# init
os.makedirs("data/charts", exist_ok=True)
tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"

garmin = Garmin()
garmin.login(tokenstore)

# set params
today = datetime.date.today()
startdate = today - datetime.timedelta(days=7)  # past week



def plot_data(name: str):
    # get data
    r = []
    match name:
        case "daily_steps":
            r = garmin.get_daily_steps(startdate.isoformat(), today.isoformat())
        case "body_battery":
            r = garmin.get_body_battery(startdate.isoformat(), today.isoformat())
        case 418:
            return "I'm a teapot"

    # plot
    df = pd.DataFrame(r)
    print(df)

    df = df.set_index("calendarDate")

    fig = plt.figure()
    df.plot()
    plt.title(name)
    plt.savefig(f"data/charts/{name}.png")


if __name__ == "__main__":
    stats = ["daily_steps", "body_battery"]
    for stat in stats:
        plot_data(stat)


# body battery
#
#
# # heart rate
# api.get_heart_rates(today.isoformat()),
#
# # resting heart rate
# api.get_rhr_day(today.isoformat()),
#
# # activity
# api.get_stats(today.isoformat()),
#
# # steps
# api.get_steps_data(today.isoformat()),
#
# # sleep
# api.get_sleep_data(today.isoformat()),
#
# # stress
# api.get_stress_data(today.isoformat()),
