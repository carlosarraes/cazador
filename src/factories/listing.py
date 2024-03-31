from typing import Iterator
from fastapi import Depends

from adapters import dao
from adapters.db import MongoDatabase
import services
from factories.db import get_database


def get_listing_dao(
    db: MongoDatabase = Depends(get_database),
) -> Iterator[dao.Listing]:
    try:
        yield dao.Listing(db)
    finally:
        pass


def get_listing_service(
    dao: dao.Listing = Depends(get_listing_dao),
) -> Iterator[services.Listing]:
    try:
        yield services.Listing(dao)
    finally:
        pass
