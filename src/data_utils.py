from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def master_database():
    db_password = "DmUKR0yONjMExVNN"
    uri = f"mongodb+srv://admin:{db_password}@cluster0.vg3mk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client["max_entropy"]

def fed_speech_collection():
    return master_database()["fed_speech_summary"]
