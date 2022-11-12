import os

from pymongo import MongoClient

config = os.environ


def get_mongo_url():
    return config["MONGO_URL"]


def get_mongo_db():
    return config["MONGO_DB_NAME"]


def get_db_client():
    mongodb_client = MongoClient(get_mongo_url())
    return mongodb_client


def close_db_client(mongodb_client):
    mongodb_client.close()
