from typing import Any, Self

from models.db import MongoModel


class Listing(MongoModel):
    __collection__ = "listing"

    id: str
    link: str
    below_price: bool | None
    iptu: float | None
    condominium: float | None
    short_description: str | None
    description: str | None
    value: float
    street: str | None
    images: list[str] | None
    area: int
    bedroom: int | None
    bathroom: int | None
    parking: int | None

    @classmethod
    def from_next_data(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data["id"],
            link=data["href"],
            short_description=None,
            description=data["description"],
            below_price=data["prices"]["belowPrice"],
            iptu=data["prices"]["iptu"] if "iptu" in data["prices"] else None,
            condominium=data["prices"]["condominium"]
            if "condominium" in data["prices"]
            else None,
            value=data["prices"]["mainValue"],
            street=data["address"]["street"],
            images=[image["src"] for image in data["imageList"]],
            area=data["amenities"]["usableAreas"],
            bedroom=data["amenities"]["bedrooms"],
            bathroom=data["amenities"]["bathrooms"],
            parking=data["amenities"]["parkingSpaces"],
        )

    @classmethod
    def from_web(cls, data: dict[str, str], ids: list[str]) -> Self:
        return cls(
            id=next((id for id in ids if id in data["link"]), "N/A"),
            street=data["street"],
            description=data["description"],
            link=data["link"],
            value=float(
                data["price"].replace("R$", "").replace(".", "").replace(",", ".")
            ),
            condominium=float(
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
            area=int(data["area"].replace("m²", "")),
            bedroom=int(data["rooms"]) if data["rooms"] != "N/A" else 0,
            bathroom=int(data["bathrooms"]) if data["bathrooms"] != "N/A" else 0,
            parking=int(data["parking"]) if data["parking"] != "N/A" else 0,
            below_price=None,
            images=None,
            short_description=None,
        )
