from typing import Any
import json
from bs4 import BeautifulSoup, Tag, NavigableString
import cloudscraper

from src.models.listing import Listing


ZAP_URL = "https://www.zapimoveis.com.br/venda/apartamentos/sc+palhoca++pedra-branca/?__ab=exp-aa-test:B,rec-cta:control&transacao=venda&onde=,Santa%20Catarina,Palho%C3%A7a,,Pedra%20Branca,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EPalhoca%3EBarrios%3EPedra%20Branca,-27.662428,-48.661448,&tipos=apartamento_residencial&pagina=1&quartos=3,4&precoMaximo=600000"


class ZapScraper:
    def __init__(self, url: str) -> None:
        self.url = url
        self.scraper = cloudscraper.create_scraper()

    def _get_data(self) -> BeautifulSoup:
        res = self.scraper.get(self.url)

        return BeautifulSoup(res.text, "html.parser")

    @staticmethod
    def _process_listing(listing: Any) -> dict[str, Any]:
        a_tag = listing.select(
            "a.result-card.result-card__highlight.result-card__highlight--default, a.result-card.result-card__highlight.result-card__highlight--standard"
        )[0]

        location_element = listing.find("h2", class_="card__address")
        location = location_element.get("title", "N/A") if location_element else "N/A"

        street_element = listing.find("p", class_="card__street")
        street = street_element.get("title", "N/A") if street_element else "N/A"

        description_tag = listing.find("p", class_="card__description")
        description = description_tag.get_text(strip=True) if description_tag else "N/A"

        price_info = listing.find("div", class_="listing-price")
        price = "N/A"
        additional_costs = "N/A"
        if price_info:
            price_tag = price_info.find("p", class_="l-text--weight-bold")
            if price_tag:
                price = price_tag.get_text(strip=True)
            additional_costs_tag = price_info.find("p", class_="l-text--weight-regular")
            if additional_costs_tag:
                additional_costs = additional_costs_tag.get_text(strip=True)

        area_info = listing.find("p", itemprop="floorSize")
        area = area_info.get_text(strip=True) if area_info else "N/A"

        amenities_section = listing.find("section", class_="card__amenities")
        amenities = {}
        if amenities_section:
            amenities = {
                (
                    amenity.find("span", role="document").get(
                        "aria-label", "Unknown Amenity"
                    )
                    if amenity.find("span", role="document")
                    else "N/A"
                ): (amenity.get_text(strip=True))
                for amenity in amenities_section.find_all("p", class_="card__amenity")
            }

        return {
            "location": location,
            "street": street,
            "description": description,
            "link": a_tag.get("href", "N/A"),
            "price": price,
            "additional_costs": additional_costs,
            "area": area,
            "rooms": amenities.get("Dormitórios", "N/A"),
            "bathrooms": amenities.get("Banheiros", "N/A"),
            "parking": amenities.get("Vagas", "N/A"),
        }

    @staticmethod
    def _get_from_next_data(next_data: NavigableString | Tag | None) -> list[Listing]:
        data = json.loads(next_data.text if next_data else "{}")["props"]["pageProps"][
            "initialProps"
        ]["data"]

        return [Listing.from_next_data(listing) for listing in data]

    @staticmethod
    def _get_ids(ids: list[dict[str, Any]]) -> list[str]:
        return [
            id["item"]["offers"]["url"].split("-")[-1].replace("/", "") for id in ids
        ]

    def run(self) -> list[Listing]:
        soup = self._get_data()

        next_data = soup.find("script", {"id": "__NEXT_DATA__"})
        listings = soup.find_all("div", class_="result-card")
        id_support = soup.find_all("script", {"type": "application/ld+json"})[2]
        ids = self._get_ids(json.loads(id_support.text)["itemListElement"])

        processed_listing = [self._process_listing(listing) for listing in listings]
        listings = [Listing.from_web(listing, ids) for listing in processed_listing]

        return listings + self._get_from_next_data(next_data)
