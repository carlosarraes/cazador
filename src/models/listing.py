from typing import Self

from models.db import MongoModel


class TestList(MongoModel):
    __collection__ = "test_list"

    name: str
    age: int


class Listing(MongoModel):
    __collection__ = "listing"

    location: str
    street: str | None
    description: str
    link: str | None
    price: float
    cond: float | None
    iptu: float | None
    area: float
    rooms: int
    bathrooms: int
    parking: int

    @classmethod
    def from_web(cls, data: dict[str, str]) -> Self:
        return cls(
            location=data["location"],
            street=data["street"],
            description=data["description"],
            link=data["link"],
            price=float(
                data["price"].replace("R$", "").replace(".", "").replace(",", ".")
            ),
            cond=float(
                data["additional_costs"]
                .split("|")[0]
                .replace("Cond.", "")
                .replace("R$", "")
                .strip()
            )
            if "Cond." in data["additional_costs"]
            else None,
            iptu=float(
                data["additional_costs"]
                .split("|")[1]
                .replace("IPTU", "")
                .replace("R$", "")
                .strip()
            )
            if "IPTU" in data["additional_costs"]
            else None,
            area=float(data["area"].replace("m²", "")),
            rooms=int(data["rooms"]) if data["rooms"] != "N/A" else 0,
            bathrooms=int(data["bathrooms"]) if data["bathrooms"] != "N/A" else 0,
            parking=int(data["parking"]) if data["parking"] != "N/A" else 0,
        )
