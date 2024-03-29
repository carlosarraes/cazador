from factories.get_db import get_database
from models.listing import TestList
import uvicorn
from fastapi import Depends, FastAPI
from pymongo.database import Database

app = FastAPI()


@app.get("/")
def test_db(db: Database = Depends(get_database)) -> dict[str, str]:
    test_list = TestList(name="John Doe", age=25)
    result = db.collection(TestList).insert_one(test_list.model_dump())

    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
