# Built-in Modules
import os
from datetime import datetime, timedelta
from pathlib import Path
import json

# Third Party Modules
import pandas as pd
import numpy as np
import pytz

from dotenv import load_dotenv


def get_db_client_kwargs():
    return {
        'dbname': os.environ.get('PGDATABASE'),
        'user': os.environ.get('PGUSER'),
        'password': os.environ.get('PGPASSWORD'),
        'host': os.environ.get('PGHOST'),
        'port': os.environ.get('PGPORT'),
    }


def populate_df(df, measurement_date, device_id, metrics, schema='json',
                check_duplicates=False):
    """
    :param df: Dataframe to be updated
    :param measurement_date: Datetime in string format
    :param device_id: String id in devices table
    :param metrics: Python object of device_metric_type_id: value (numeric)
    :param schema: json or narrow
    :return: Updated dataframe
    """
    if schema == 'json':
        if df is None:
            df = pd.DataFrame(columns=['measurement_date',
                                       'device_id',
                                       'metrics'])
        if check_duplicates:
            # Only append if unique new key
            if ((df['measurement_date'] == measurement_date)
                    & (df['device_id'] == device_id)).any():
                return df

        df = df.append({'measurement_date': measurement_date,
                        'device_id': device_id,
                        'metrics': json.dumps(metrics)}, ignore_index=True)
    if schema == 'narrow':
        if df is None:
            df = pd.DataFrame(
                columns=['measurement_date', 'device_id',
                         'device_metric_type_id', 'value'])

        for metric, value in metrics.items():
            if check_duplicates:
                if ((df['measurement_date'] == measurement_date)
                        & (df['device_id'] == device_id)
                        & (df['device_metric_type_id'] == metric)).any():
                    # Only append if unique new key
                    continue
            df = df.append({'measurement_date': measurement_date,
                            'device_id': device_id,
                            'device_metric_type_id': metric,
                            'value': value,
                            'received_date': measurement_date},
                           ignore_index=True)
    return df


def generate_sample_df(dates, device_metrics, schema='narrow'):
    flatten = lambda l: [item for sublist in l for item in sublist]
    if schema == 'narrow':
        cardinality = len(dates) * \
                      sum([len(v) for v in device_metrics.values()])
        df_data = {
            'measurement_date': dates * int(cardinality / len(dates)),
            'device_id': flatten([[k] * len(dates) * len(v)
                                  for k, v in device_metrics.items()]),
            'device_metric_type_id': flatten([
                [item for item in val for _ in range(len(dates))]
                for val in device_metrics.values()]),
            'value': np.random.uniform(low=-10.0, high=10.0,
                                       size=(cardinality,)),
            'received_date': dates * int(cardinality / len(dates))
        }
        return pd.DataFrame(data=df_data)
    elif schema == 'json':
        cardinality = len(dates) * len(device_metrics)
        df_data = {
            'measurement_date': dates * int(cardinality / len(dates)),
            'device_id': [key for key in device_metrics.keys()
                          for _ in range(len(dates))],
            'metrics': [dict.fromkeys(
                metrics, np.random.uniform(low=-10.0, high=10.0))
                for _ in range(len(dates))
                for metrics in device_metrics.values()]
        }
        return pd.DataFrame(data=df_data)
    else:
        return None


def apply_standard_index(df, dropna = False):
    idx = ['device_id', 'device_metric_type_id', 'measurement_date']
    df.set_index(idx, inplace=True)
    # Only need the value column
    df.drop(df.columns.difference(['value']), 1, inplace=True)
    df.index = df.index.set_levels(
        [df.index.levels[0].astype('int64'),
         df.index.levels[1],
         pd.to_datetime(df.index.levels[2], utc = True)])
    # Have time displayed from least recent to most recent.
    # Still grouped by device_id, metric_type first
    if dropna:
        df.dropna(inplace=True)
    df.sort_index(inplace=True, ascending=True)


def apply_forecast_index(df):
    idx = ['device_id', 'device_metric_type_id',
           'measurement_date', 'forecast_date']
    # Convert datetime columns to brisbane local time
    df.set_index(idx, inplace=True)
    # Only need the value column
    df.drop(df.columns.difference(['value']), 1, inplace = True)
    df.index = df.index.set_levels(
        [df.index.levels[0],
         df.index.levels[1],
         pd.to_datetime(df.index.levels[2], utc = True),
         pd.to_datetime(df.index.levels[3], utc = True)])
    # TODO


def validate_timestamp(ts):
    if isinstance(ts, datetime):
        ts_end = ts.astimezone(pytz.utc)
    else:
        raise ValueError("Reference Time must be type datetime but was"
                         " '{0}'".format(type(ts)))
    return ts_end


def generate_ts_conditionals(simulation=None, reference_time=None, window=None):
    """
    All timestamp based conditionals passed to the database must be in UTC.
    :param simulation: The name of the simulation if provided
    :param reference_time: Timestamp which is the upper bound of the time index
    (exclusive)
    :param window: The number of minutes prior to reference_time which forms
    the time interval for the query.
    :return:
    """
    if reference_time is None:
        reference_time = datetime.utcnow()
    reference_time = validate_timestamp(reference_time)
    if reference_time is not None:
        if isinstance(reference_time, datetime):
            ts_end = reference_time.astimezone(pytz.utc)
        else:
            raise ValueError("Reference Time must be type datetime but was"
                             " '{0}'".format(type(reference_time)))
    else:
        ts_end = datetime.utcnow()
    # This statement must have an end date conditional
    conditionals = "AND measurement_date < %s "
    conditional_vals = [ts_end.isoformat(sep=' ',
                                         timespec='milliseconds')]

    if window is not None:
        ts_start = ts_end - timedelta(minutes = window)
        conditionals += "AND measurement_date >= %s "
        conditional_vals.append(ts_start.isoformat(sep=' ',
                                                   timespec='milliseconds'))
    if simulation is not None:
        conditionals += "AND simulation = %s "
        conditional_vals.append(simulation)

    return conditionals, conditional_vals


def get_clean_df(df, columns=None, min_size=None, all=False):
    """
    Handles any rows in the the dataframe where values in 'columns' are NAN by
    splitting the table. This ensures that a continguous dataframe result is
    returned.
    :param df: The dataframe to be cleaned by removing NAN columns
    :param columns: List of columns where NAN values are to be removed.
    :param min_size: The minimum number of rows required for dataframe to be
    returned.
    :param all: Boolean indicating whether all of the split dataframe blocks
    should be returned. The default value False ensures that only the latest
    clean datafram is returned.
    :return:
    Either a single dataframe or a list of dataframse if all = True.
    """
    if columns is None:
        # Split DataFrame on NaN values in any of 'columns'
        df_split = np.split(df, np.where(np.isnan(df))[0])
        # removing NaN entries
        df_split = [df.dropna(subset=columns) for df in df_split
                    if not isinstance(df, np.ndarray)]
    else:
        # Split DataFrame on NaN values in any of 'columns'
        df_split = np.split(df, np.where(np.isnan(df.loc[:, columns]))[0])
        # removing NaN entries
        df_split = [df.dropna() for df in df_split
                    if not isinstance(df, np.ndarray)]
    if min_size is not None:
        # Filter DataFrame by Size
        df_split = [df for df in df_split
                    if len(df.index) >= min_size]
    if all:
        return df_split
    else:
        return df_split[-1]


def get_lvfm(df, metric, device_id=None):
    """
    Get Last Value For Metric from a dataframe, df in the standardized format
    :return: Value
    """
    if device_id is None:
        return df.xs(metric, level='device_metric_type_id').iloc[-1]
    else:
        return df.loc[(device_id, metric), 'value'].iloc[-1]


def get_fvfm(df, metric, device_id=None):
    """
    Get First Value For Metric from a dataframe, df in the standardized format
    :return: Value
    """
    if device_id is None:
        return df.xs(metric, level = 'device_metric_type_id').iloc[0]
    else:
        return df.loc[(device_id, metric), 'value'].iloc[0]