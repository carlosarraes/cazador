import models
from adapters.db import MongoDatabase


class Listing:
    def __init__(self, db: MongoDatabase) -> None:
        self.db = db

    def get_all(self) -> list[models.Listing]:
        return [
            models.Listing(**listing)
            for listing in self.db.collection(models.Listing).find()
        ]

    def update(self, listings: list[models.Listing]) -> None:
        self.db.collection(models.Listing).insert_many(
            [listing.model_dump() for listing in listings]
        )
