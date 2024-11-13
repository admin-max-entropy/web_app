"""Script to load relevant data"""

import datetime
import functools
import math
import src.data_utils
from src import config


def get_elasticity_data(start_date):
    """
    :param start_date:
    :return: dictionary of elasticity data by percentile
    """
    data = src.data_utils.read_elasticity_table()
    result = {}

    for key in data:
        mapped_key = key.replace("_", ".")
        result[mapped_key] = {}
        for date in data[key]:
            if date < start_date:
                continue
            result[mapped_key][date] = data[key][date]
    return result


def tga_balances(start_date: datetime, end_date: datetime):
    """
    :param start_date:
    :param end_date:
    :return: return daily GTA balances
    """
    table_name = src.config.TABLE_TGA_BALANCE
    time_series = src.data_utils.read_fred_related_table(table_name)
    time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    result = {}
    for knot in time_series:
        result[knot] = time_series[knot]/1e3
    return result

def rrp_data(start_date:datetime, end_date:datetime, key:str):
    """
    :param start_date:
    :param end_date:
    :return: rrp data
    """
    data = src.data_utils.read_fred_related_table(key)
    time_series = {k: v for k, v in data.items() if start_date <= k <= end_date}
    return time_series

def reserve_balance_data(start_date:datetime, end_date:datetime):
    """
    :param start_date:
    :param end_date:
    :return: bank reserves
    """
    data = src.data_utils.read_fred_related_table(src.config.TABLE_RESERVE_BALANCE)
    time_series = {k: v for k, v in data.items() if start_date <= k <= end_date}
    return time_series


@functools.lru_cache(maxsize=32)
def __iorb_timeseries(start_date: datetime, end_date: datetime):
    time_series = src.data_utils.read_fred_related_table(src.config.TABLE_IORB)
    time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    return time_series

def __effr_timeseries(start_date:datetime, end_date:datetime):
    time_series = src.data_utils.read_fred_related_table(
        src.config.TABLE_EFFR)
    time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    return time_series


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

def repo_volume_ts(start_date:datetime, end_date:datetime, is_repo:bool):
    """
    :param start_date:
    :param end_date:
    :return: spread between effr and iorb
    """
    repo_volumes = {}
    data_in_bulk = src.data_utils.read_ofr_data_table()
    keys = ["tgcr", "sofr", "bgcr"] if is_repo else ["effr", "obfr"]

    for key in keys:
        repo_volumes[key] = {}
        filtered_data = data_in_bulk[f"FNYR{key.upper()}_UVA"]
        for date in filtered_data:
            if date > end_date or date < start_date:
                continue
            repo_volumes[key][date] = filtered_data[date]/1e9 if filtered_data[date] is not None else math.nan

    return repo_volumes

def iorb_key_spread(start_date:datetime, end_date:datetime, key_input, cap: float, floor: float):
    """
    :param start_date:
    :param end_date:
    :return: spread between effr and iorb
    """
    iorb = __iorb_timeseries(start_date, end_date)
    tgcr = get_short_end_timeseries(key_input.upper(), start_date, end_date, apply_spread=False)

    print(" ................", start_date, end_date, key_input, cap, floor)
    spread = {}
    for key, ts in tgcr.items():
        spread[key] = {}
        for knot in iorb:
            if knot in ts:
                knot_value = ts[knot] if ts[knot] is not None else math.nan
                spread_val = (knot_value-iorb[knot])*100.
                spread_val = min(cap, spread_val) if not math.isnan(spread_val) else math.nan
                spread_val = max(floor, spread_val) if not math.isnan(spread_val) else math.nan
                spread[key][knot] = spread_val

    return spread

def iorb_rrp_spread(start_date:datetime, end_date:datetime):
    """
    :param start_date:
    :param end_date:
    :return: spread between effr and iorb
    """
    iorb = __iorb_timeseries(start_date, end_date)
    rrp = __rrp_rate(start_date, end_date)

    spread = {}
    for knot, value in rrp.items():
        if knot in iorb:
            spread[knot] = (value-iorb[knot])*100.
    return spread

def iorb_lower_spread(start_date:datetime, end_date:datetime):
    """
    :param start_date:
    :param end_date:
    :return: spread between effr and iorb
    """
    iorb = __iorb_timeseries(start_date, end_date)
    dummy_start_date = datetime.datetime(2018, 9, 1)
    rrp = __lower_rate(dummy_start_date, end_date)

    spread = {}
    for knot in rrp:
        if knot in iorb:
            spread[knot] = (rrp[knot]-iorb[knot])*100.
    return spread

def iorb_upper_spread(start_date:datetime, end_date:datetime):
    """
    :param start_date:
    :param end_date:
    :return: spread between effr and iorb
    """
    iorb = __iorb_timeseries(start_date, end_date)
    dummy_start_date = datetime.datetime(2018, 9, 1)
    rrp = __upper_rate(dummy_start_date, end_date)

    spread = {}
    for knot in rrp:
        if knot in iorb:
            spread[knot] = (rrp[knot]-iorb[knot])*100.
    return spread

def fedfund_volume_decomposition(start_date:datetime, end_date:datetime):
    """
    :param start_date:
    :param end_date:
    :return: dictionary of fedfund volume
    """
    data_table = src.data_utils.read_fedfund_volume_decomposition_table()
    result = {}
    end_date = end_date.replace(tzinfo=None)
    for row in data_table:
        date = row["date"]
        if date < start_date or date > end_date:
            continue
        result[date] = row["domestic_bank_volume"]/row["total_volume"] * 100.

    return result

def daylight_overdraft(is_average):
    """
    :return: daylight overdraft data
    """
    start_date = config.TS_START_DATE
    data = src.data_utils.read_daylight_overdraft_table()
    result = {}
    for key in data:
        if is_average:
            mapped_key = key.replace("Average_", "")
        else:
            mapped_key = key.replace("Peak_", "")
        if is_average:
            if "Average" not in key:
                continue
        else:
            if "Peak" not in key:
                continue

        mapped_key = mapped_key.replace("_", " ")
        result[mapped_key] = {}
        for knot in data[key]:
            if knot < start_date:
                continue
            result[mapped_key][knot] = data[key][knot]

    return result

def __key_set():
    result = {}
    for key in ["SOFR", "EFFR", "BGCR", "TGCR", "OBFR"]:
        result[key] = [f"FNYR{key}A", f"FNYR{key}_1PctlA", f"FNYR{key}_25PctlA",
                       f"FNYR{key}_75PctlA", f"FNYR{key}_99PctlA"]
    return result


def __rrp_rate(start_date:datetime, end_date:datetime):
    time_series = src.data_utils.read_fred_related_table(src.config.TABLE_RRP_RATE)
    time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    return time_series


def __upper_rate(start_date:datetime, end_date:datetime):
    time_series = src.data_utils.read_fred_related_table(src.config.TABLE_UPPER_BOUND)
    time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    return time_series

def __lower_rate(start_date:datetime, end_date:datetime):
    time_series = src.data_utils.read_fred_related_table(src.config.TABLE_UPPER_BOUND)
    time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    return time_series

@functools.lru_cache()
def get_short_end_timeseries(data_key, start_date, end_date, apply_spread=True):
    """
    :param data_key:
    :param start_date:
    :param end_date:
    :return: short end rates timeseries
    """
    data_in_bulk = src.data_utils.read_ofr_data_table()
    rate_ts_set = {}
    data_keys = __key_set()[data_key]

    rrp_rate = __rrp_rate(start_date, end_date)
    for key in data_in_bulk:
        if key not in data_keys:
            continue
        time_series = data_in_bulk[key]
        if apply_spread:
            for date in time_series:
                time_series[date] = time_series[date] - rrp_rate.get(date, math.nan)

        for date in rrp_rate:
            if date not in time_series:
                if date > start_date:
                    time_series[date] = math.nan

        time_series = dict(sorted(time_series.items()))
        rate_ts_set[key] = time_series

    return rate_ts_set


# date = datetime.datetime(2020, 1, 1)
# end_date = datetime.datetime(2024, 9, 25)
# iorb_tgcr_spread(date, end_date)
