import os.path
from datetime import datetime
from engine.mongodb import get_db_client, close_db_client, get_mongo_url, get_mongo_db
from engine.scrapper.model import Analytic
import nest_asyncio
import twint
import json

from engine.utils import get_now, get_time_minutes_ago

nest_asyncio.apply()

ANALYTIC_COLLECTION = "analytics"
ANALYTIC_CRAWLED_DATA_COLLECTION = "analytic_data"


def get_analytic_data(db, analytic_id: str) -> (Analytic, str):
    analytic = db[ANALYTIC_COLLECTION].find_one({"_id": analytic_id})
    if not analytic:
        return None, "data is not found"
    return analytic, None


def run_scrapper(analytic_id: str, minutes: int) -> str:
    db = get_db_client()
    analytic, err = get_analytic_data(db[get_mongo_db()], analytic_id)
    close_db_client(db)
    if err:
        return err

    collection_name = f"{ANALYTIC_CRAWLED_DATA_COLLECTION}_{analytic_id}"
    keywords = analytic['keyword']
    since = get_time_minutes_ago(minutes)
    city = 'indonesia'
    if 'city' in analytic:
        city = analytic['city']

    for keyword in keywords:
        twint_scraper(keyword, since, city, collection_name=collection_name)

    delete_tmp_file(collection_name)
    return None


def twint_scraper(keyword, since, city="indonesia", until=get_now(), collection_name="") -> (bool, str):
    if collection_name == "":
        return False, "mongo_collection is required"

    output_name = get_tmp_file_path(collection_name)
    print(keyword, since, city, until, output_name)

    # Basic Twint scraper configuration (see: https://github.com/twintproject/twint)
    c = twint.Config()
    c.Search = keyword  # keywords inputed must be a single string of word or phrase
    c.Near = city  # the city name that as the geolocation tweet that will be scraped, default is indonesia
    c.Since = since  # the start datetime of crawling, e.g. "2022-06-03" or "2022-06-03 00:35:23"
    c.until = until  # the end datetime of crawling, e.g. "2022-06-03" or "2022-06-03 00:35:23", default is today including the time
    c.Hide_output = True  # set False if you want to verbose (watch) the scraping process
    c.Count = True
    c.Stats = True
    c.hashtags = True
    c.Store_json = True
    c.Output = output_name
    twint.run.Search(c)

    copy_to_mongo_db(output_name, collection_name)

    return True, None


def copy_to_mongo_db(file_path: str, collection_name: str):
    if os.path.exists(file_path):
        db_client = get_db_client()
        collection = db_client[get_mongo_db()][collection_name]
        with open(file_path, 'r') as f:
            for line in iter(f.readline, ''):
                text = line.strip()
                d = json.loads(text)
                d["_id"] = d["id"]
                collection.update_one({"_id": d["_id"]}, {"$set": d}, True)

        close_db_client(db_client)


def get_tmp_file_path(collection_name: str) -> str:
    return f"output/{collection_name}.json"


def delete_tmp_file(collection_name: str):
    tmp_file = get_tmp_file_path(collection_name)
    if os.path.exists(tmp_file):
        os.remove(tmp_file)
