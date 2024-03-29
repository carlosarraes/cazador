from pymongo.database import Database
from pymongo.collection import Collection
from pydantic import BaseModel


class MongoModel(BaseModel):
    __collection__: str = ""

    @classmethod
    def get_collection_name(cls) -> str:
        if not cls.__collection__:
            raise AttributeError(
                f"Class {cls.__name__} lacks '__collection__' attribute"
            )
        return cls.__collection__


class MongoDatabase:
    def __init__(self, db: Database) -> None:
        self.db = db

    def collection(self, model_cls: type[MongoModel]) -> Collection:
        collection_name = model_cls.get_collection_name()
        return self.db[collection_name]
