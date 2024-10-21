import datetime
import functools
import collections
import requests
import pandas
from src import config

def get_elasticity_data(start_date):
    data_link = ("https://www.newyorkfed.org/medialibrary/Research/Interactives"
                 "/Data/elasticity/download-data")
    data = pandas.read_excel(data_link, sheet_name="chart data", skiprows=3, header=1)
    data = data.to_dict(orient="records")
    data_result = {}
    for row in data:
        date = row["Date"]
        if date.date() < start_date.date():
            continue
        for key in row:
            if key == "Date":
                continue
            key_ = key.split(" - ")[-1].replace("percentile", "%")
            if key_ not in data_result:
                data_result[key_] = {}
            data_result[key_][date] = row[key]
    return data_result


def __query_format(series_id: str, start_date: datetime, end_date: datetime):
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    path = (f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={config.FRED_API_KEY}"
            f"&file_type=json&realtime_start={start_date}&realtime_end={end_date}")
    return path

@functools.lru_cache(maxsize=None)
def iorb_timeseries(start_date: datetime, end_date: datetime):
    time_series = collections.OrderedDict()

    iorb_start_date = datetime.datetime(2021, 7, 28)
    iorb_path = __query_format("IORB", iorb_start_date, end_date)
    iorb_data = requests.get(iorb_path, timeout=10).json()
    for row in iorb_data["observations"]:
        time_series[datetime.datetime.strptime(row["date"], "%Y-%m-%d")] = float(row["value"])

    ioer_path = __query_format("IOER", start_date, iorb_start_date)
    ioer_data = requests.get(ioer_path, timeout=10).json()
    for row in ioer_data["observations"]:
        time_series[datetime.datetime.strptime(row["date"], "%Y-%m-%d")] = float(row["value"])

    time_series = dict(sorted(time_series.items()))
    time_series = {k: v for k, v in time_series.items() if start_date <=k <= end_date}
    return time_series

@functools.lru_cache(maxsize=None)
def effr_timeseries(start_date:datetime, end_date:datetime):
    path = __query_format("EFFR", start_date, end_date)
    data = requests.get(path, timeout=10).json()
    time_series = collections.OrderedDict()
    for row in data["observations"]:
        if row["value"] == ".":
            continue
        time_series[datetime.datetime.strptime(row["date"], "%Y-%m-%d")] = float(row["value"])
    time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    return time_series

@functools.lru_cache()
def iorb_effr_spread(start_date:datetime, end_date:datetime):
    """
    :param start_date:
    :param end_date:
    :return: spread between effr and iorb
    """
    iorb = iorb_timeseries(start_date, end_date)
    effr = effr_timeseries(start_date, end_date)
    spread = {}
    for knot in iorb:
        if knot in effr:
            spread[knot] = (effr[knot]-iorb[knot])*100.
    return spread
