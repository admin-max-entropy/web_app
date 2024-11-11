"""Data utils"""
import functools
import collections
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from collections import OrderedDict
import src.config
import mysql.connector


@functools.lru_cache(maxsize=None)
def get_database(database_name):
    return mysql.connector.connect(
        host=src.config.HOST,
        user=src.config.USER,
        passwd=src.config.PWD,
        database=database_name
    )


def master_database():
    """
    :return:
    """
    db_password = "DmUKR0yONjMExVNN"
    uri = (f"mongodb+srv://admin:{db_password}@cluster0.vg3mk.mongodb.net"
           f"/?retryWrites=true&w=majority&appName=Cluster0")
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client["max_entropy"]


def fed_speech_collection():
    """
    :return:
    """
    return master_database()["fed_speech_summary"]

def read_fedfund_volume_decomposition_table():
    db = get_database(src.config.DATABASE_STIR)
    cursor = db.cursor(dictionary=True)
    table_name = src.config.TABLE_FF_DECOMP_VOLUME
    cursor.execute(f"SELECT * FROM {table_name}")
    result = cursor.fetchall()
    return result


def read_fred_related_table(table_name, start_date, end_date):
    db = get_database(src.config.DATABASE_STIR)
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    time_series = collections.OrderedDict()
    for row in data:
        time_series[row["date"]] = row["value"]
    time_series = dict(sorted(time_series.items()))
    time_series = {k: v for k, v in time_series.items() if start_date <= k <= end_date}
    return time_series

def read_ofr_data_table():
    db = get_database(src.config.DATABASE_STIR)
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {src.config.TABLE_OFR_ON_DATA}")
    data = cursor.fetchall()
    result = {}
    for row in data:
        date = row["date"]
        for key in row:
            if key == "date":
                continue
            if key not in result:
                result[key] = OrderedDict()
            result[key][date] = row[key]
    for key in result:
        result[key] = dict(sorted(result[key].items()))
    return result

@functools.lru_cache(maxsize=None)
def read_daylight_overdraft_table():
    db = get_database(src.config.DATABASE_STIR)
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {src.config.TABLE_DAYLIGHT_OVERDFRAT}")
    data = cursor.fetchall()
    result = {}
    for row in data:
        date = row["date"]
        for key in row:
            if key == "date":
                continue
            if key not in result:
                result[key] = OrderedDict()
            result[key][date] = row[key]
    for key in result:
        result[key] = dict(sorted(result[key].items()))
    return result

@functools.lru_cache(maxsize=None)
def read_elasticity_table():
    db = get_database(src.config.DATABASE_STIR)
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {src.config.TABLE_ELASTICITY}")
    data = cursor.fetchall()
    result = {}
    for row in data:
        date = row["date"]
        for key in row:
            if key == "date":
                continue
            if key not in result:
                result[key] = OrderedDict()
            result[key][date] = row[key]
    for key in result:
        result[key] = dict(sorted(result[key].items()))
    return result