from factories.get_db import get_database
import uvicorn
from fastapi import Depends, FastAPI
from pymongo.database import Database

app = FastAPI()


@app.post("/update")
def test_db(db: Database = Depends(get_database)) -> dict[str, str]:
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
