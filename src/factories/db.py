import os
from typing import Iterator
from pymongo import MongoClient

from adapters.db import MongoDatabase


def get_database() -> Iterator[MongoDatabase]:
    client = MongoClient(
        f'mongodb://user:password@{os.getenv("DB_HOST", "mongo-clusterip")}:27017/'
    )
    try:
        yield MongoDatabase(client["cazador"])
    finally:
        client.close()
