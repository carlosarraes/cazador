import uvicorn
from fastapi import Depends, FastAPI

import services
import models
from factories.listing import get_listing_service

app = FastAPI()


@app.get("/")
def get_all(
    services: services.Listing = Depends(get_listing_service),
) -> list[models.Listing]:
    return services.get_all()


@app.post("/update")
def update(
    services: services.Listing = Depends(get_listing_service),
) -> None:
    return services.update()


@app.get("/debug")
def debug(
    services: services.Listing = Depends(get_listing_service),
) -> dict[str, str]:
    services.debug()
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
