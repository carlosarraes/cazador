from typing import Iterator
from pymongo import MongoClient

from adapters.db import MongoDatabase


def get_database() -> Iterator[MongoDatabase]:
    client = MongoClient("mongodb://user:password@localhost:27017/")
    try:
        yield MongoDatabase(client["cazador"])
    finally:
        client.close()
