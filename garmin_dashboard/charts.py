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


def _plot(name, df):
    df.plot(kind="bar")

    plt.title(name)
    plt.xticks(rotation=45)

    plt.savefig(f"data/charts/{name}.png")

    return plt


def chart_body_battery():
    df = pd.DataFrame(garmin.get_body_battery(startdate.isoformat(), today.isoformat()))
    df = df[["date", "charged", "drained"]].set_index("date")
    print(df)

    return _plot("Body Battery", df)


# # resting heart rate
# garmin.get_rhr_day(today.isoformat())
#
# # sleep
# api.get_sleep_data(today.isoformat()),
#
# # stress
# api.get_stress_data(today.isoformat()),
