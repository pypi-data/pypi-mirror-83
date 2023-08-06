# Built-in Modules
import re
import os
import logging
from datetime import timedelta, datetime

# Third Party Modules
from astral import Observer
from astral import sun
import pandas as pd
from pytz import timezone

def get_sun_elevation(ts):
    """
    :param ts: Numpy Datetime
    :return: 1 if
    """
    # Default to the location of the St Lucia Campus
    # TODO: These coords should be pulled from the DB
    #  (integrate into dre-database-api)
    long = 153.014008
    lat = -27.497999
    observer = Observer(lat, long)
    return sun.elevation(observer, pd.to_datetime(ts))


def is_public_holiday(ts, hols):
    date = pd.to_datetime(ts, timezone('UTC')) \
        .astimezone(timezone('Australia/Brisbane')).date()
    return 1 if date in hols else 0


def is_working_hours(ts):
    dt = pd.to_datetime(ts, timezone('UTC'))\
        .astimezone(timezone('Australia/Brisbane'))
    return 1 if 7 < dt.hour < 18 else 0


def is_weekend(ts):
    dt = pd.to_datetime(ts, timezone('UTC')) \
        .astimezone(timezone('Australia/Brisbane'))
    return 1 if 5 <= dt.weekday() <= 6 else 0


def get_time_related_timeseries(config, freq, ts_start, ts_end, hols):
    features_df = None
    if config is None:
        return features_df
    date_rng = pd.date_range(start = ts_start, end=ts_end, freq=freq, tz='UTC')
    features_df = pd.DataFrame(index = date_rng)
    # Initialize Supported timeseries
    features = {name: [] for name in config}
    for ts in features_df.index:
        if "sunElevation" in features:
            features['sunElevation'].append(get_sun_elevation(ts))
        if "daylight" in features:
            features['daylight'].append(1 if get_sun_elevation(ts) > 0 else 0)
        if "publicHoliday":
            features['publicHoliday'].append(is_public_holiday(ts, hols))
        if "weekend":
            features['weekend'].append(is_weekend(ts))
        if "workingHours":
            features['workingHours'].append(is_working_hours(ts))
    # Fill out the dataframe
    for name, values in features.items():
        features_df[name] = values

    return features_df
