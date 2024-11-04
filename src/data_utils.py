"""Data utils"""
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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
