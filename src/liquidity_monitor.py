"""Script to load relevant data"""

import datetime
import functools
import collections

import requests
import pandas
from src import config

def get_elasticity_data(start_date):
    """
    :param start_date:
    :return: dictionary of elasticity data by percentile
    """
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
    path = (f"https://api.stlouisfed.org/fred/series"
            f"/observations?series_id={series_id}&api_key={config.FRED_API_KEY}"
            f"&file_type=json&realtime_start={start_date}&realtime_end={end_date}")
    return path

@functools.lru_cache()
def tga_balances(start_date: datetime, end_date: datetime):
    """
    :param start_date:
    :param end_date:
    :return: tga balance
    """
    time_series = collections.OrderedDict()
    iorb_path = __query_format("WTREGEN", start_date, end_date)
    iorb_data = requests.get(iorb_path, timeout=60).json()
    for row in iorb_data["observations"]:
        if row["value"] == ".":
            continue
        time_series[datetime.datetime.strptime(row["date"], "%Y-%m-%d")] = float(row["value"])
    time_series = dict(sorted(time_series.items()))
    end_date = end_date.replace(tzinfo=None)
    time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    return time_series

    # link = ("https://api.fiscaldata.treasury.gov/services/api/fiscal_service
    # /v1/accounting/dts/operating_cash_balance?fields=record_date,account_type,"
    #         "open_today_bal&filter=record_date:gte:2017-01-01,account_type:eq:T
    #         reasury General Account (TGA) Opening Balance&page[size]=10000")
    # data = requests.get(link).json()
    # result = {}
    # for row in data["data"]:
    #     date = datetime.datetime.strptime(row["record_date"], "%Y-%m-%d")
    #     if date not in result:
    #         result[date] = 0
    #     if row["open_today_bal"] == "null":
    #         continue
    #     result[date] += float(row["open_today_bal"])/1000
    # time_series = dict(sorted(result.items()))
    # end_date = end_date.replace(tzinfo=None)
    # time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    # return time_series

# data = tga_balances(datetime.datetime(2017, 1, 1), datetime.datetime(2024, 10, 23))

@functools.lru_cache()
def rrp_data(start_date:datetime, end_date:datetime):
    """
    :param start_date:
    :param end_date:
    :return: rrp data
    """
    time_series = collections.OrderedDict()
    iorb_path = __query_format("RRPONTSYD", start_date, end_date)
    iorb_data = requests.get(iorb_path, timeout=60).json()
    for row in iorb_data["observations"]:
        if row["value"] == ".":
            continue
        time_series[datetime.datetime.strptime(row["date"], "%Y-%m-%d")] = float(row["value"])
    time_series = dict(sorted(time_series.items()))
    end_date = end_date.replace(tzinfo=None)
    time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    return time_series

@functools.lru_cache()
def reserve_balance_data(start_date:datetime, end_date:datetime):
    """
    :param start_date:
    :param end_date:
    :return: bank reserves
    """
    time_series = collections.OrderedDict()
    iorb_path = __query_format("WRESBAL", start_date, end_date)
    iorb_data = requests.get(iorb_path, timeout=60).json()
    for row in iorb_data["observations"]:
        if row["value"] == ".":
            continue
        time_series[datetime.datetime.strptime(row["date"], "%Y-%m-%d")] = float(row["value"])
    time_series = dict(sorted(time_series.items()))
    end_date = end_date.replace(tzinfo=None)
    time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    return time_series

@functools.lru_cache(maxsize=None)
def __iorb_timeseries(start_date: datetime, end_date: datetime):
    time_series = collections.OrderedDict()
    iorb_start_date = datetime.datetime(2021, 7, 28)
    iorb_path = __query_format("IORB", iorb_start_date, end_date)
    iorb_data = requests.get(iorb_path, timeout=60).json()
    for row in iorb_data["observations"]:
        time_series[datetime.datetime.strptime(row["date"], "%Y-%m-%d")] = float(row["value"])

    ioer_path = __query_format("IOER", start_date, iorb_start_date)
    ioer_data = requests.get(ioer_path, timeout=60).json()
    for row in ioer_data["observations"]:
        time_series[datetime.datetime.strptime(row["date"], "%Y-%m-%d")] = float(row["value"])

    time_series = dict(sorted(time_series.items()))
    end_date = end_date.replace(tzinfo=None)
    time_series = {k: v for k, v in time_series.items() if start_date <=k <= end_date}
    return time_series

@functools.lru_cache(maxsize=None)
def __effr_timeseries(start_date:datetime, end_date:datetime):
    path = __query_format("EFFR", start_date, end_date)
    data = requests.get(path, timeout=60).json()
    time_series = collections.OrderedDict()
    for row in data["observations"]:
        if row["value"] == ".":
            continue
        time_series[datetime.datetime.strptime(row["date"], "%Y-%m-%d")] = float(row["value"])
    end_date = end_date.replace(tzinfo=None)
    time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    return time_series

@functools.lru_cache()
def iorb_effr_spread(start_date:datetime, end_date:datetime):
    """
    :param start_date:
    :param end_date:
    :return: spread between effr and iorb
    """
    iorb = __iorb_timeseries(start_date, end_date)
    effr = __effr_timeseries(start_date, end_date)
    spread = {}
    for knot in iorb:
        if knot in effr:
            spread[knot] = (effr[knot]-iorb[knot])*100.
    return spread

@functools.lru_cache()
def fedfund_volume_decomposition(start_date:datetime, end_date:datetime):
    """
    :param start_date:
    :param end_date:
    :return: dictionary of fedfund volume
    """
    year = "2024"
    assert end_date.year<=float(year)
    quarters=["q4", "q3", "q2"]

    data = []
    for quarter in quarters:
        try:
            link = ("https://www.newyorkfed.org/medialibrary/media/markets/rate-revisions"
                    f"/{year}/FR2420-summary-statistics-{quarter}{year}.xlsx")
            data = pandas.read_excel(link, sheet_name="Effective Federal Funds Rate")
            data = data.to_dict(orient="records")

        except ValueError as e:
            print(str(e))

        if len(data) > 0:
            break

    result = {}
    end_date = end_date.replace(tzinfo=None)
    for row in data:
        date = row["Date"]
        if date < start_date or date > end_date:
            continue
        result[date] = row["Domestic Bank Volume"]/row["Total Volume "] * 100.

    return result

@functools.lru_cache()
def daylight_overdraft(is_average):
    """
    :return: daylight overdraft data
    """
    start_date = config.TS_START_DATE
    link = "https://www.federalreserve.gov/paymentsystems/files/psr_dlod.txt"
    data = requests.get(link, timeout=10)
    data = data.text.split("\n")
    start_row = 9
    result = {}
    if not is_average:
        column_mapping = {2: "Total",
                          3: "Funds",
                          4: "Book-Entry",
                          8: "Collateralized",
                          }
    else:
        column_mapping = {5: "Total",
                          6: "Funds",
                          7: "Book-Entry",
                          10: "Collateralized",
                          }

    for inx in range(start_row, len(data)):
        row_info = data[inx]
        dummy = ' '.join(row_info.split())
        dummy = dummy.split(" ")
        if len(dummy) != 12:
            break
        date = datetime.datetime.strptime(dummy[0], "%m/%d/%Y")
        if date < start_date:
            continue
        for inx_, key in column_mapping.items():
            if key not in result:
                result[key] = {}
            result[key][date] = float(dummy[inx_].replace(",", "").replace("$", ""))

    for key, ts in result.items():
        result[key] = dict(sorted(ts.items()))

    return result
