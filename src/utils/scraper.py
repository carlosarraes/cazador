from bs4 import BeautifulSoup
import cloudscraper

from models.listing import Listing

ZAP_URL = "https://www.zapimoveis.com.br/venda/apartamentos/sc+palhoca++pedra-branca/?__ab=exp-aa-test:B,rec-cta:control&transacao=venda&onde=,Santa%20Catarina,Palho%C3%A7a,,Pedra%20Branca,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EPalhoca%3EBarrios%3EPedra%20Branca,-27.662428,-48.661448,&tipos=apartamento_residencial&pagina=1&quartos=3,4&precoMaximo=600000"


if __name__ == "__main__":
    scraper = cloudscraper.create_scraper()
    res = scraper.get(ZAP_URL)

    soup = BeautifulSoup(res.text, "html.parser")

    listings = soup.find_all("div", class_="result-card")

    for listing in listings:
        a_tag = listing.select(
            "a.result-card.result-card__highlight.result-card__highlight--default, a.result-card.result-card__highlight.result-card__highlight--standard"
        )[0]

        location = (
            listing.find("h2", class_="card__address").get("title", "N/A")
            if listing.find("h2", class_="card__address")
            else "N/A"
        )

        street = (
            listing.find("p", class_="card__street").get("title", "N/A")
            if listing.find("p", class_="card__street")
            else "N/A"
        )

        description_tag = listing.find("p", class_="card__description")
        description = description_tag.text.strip() if description_tag else "N/A"

        price_info = listing.find("div", class_="listing-price")
        price = (
            price_info.find("p", class_="l-text--weight-bold").text.strip()
            if price_info and price_info.find("p", class_="l-text--weight-bold")
            else "N/A"
        )
        additional_costs = (
            price_info.find("p", class_="l-text--weight-regular").text.strip()
            if price_info and price_info.find("p", class_="l-text--weight-regular")
            else "N/A"
        )

        area_info = listing.find("p", itemprop="floorSize")
        area = area_info.text.strip() if area_info else "N/A"

        amenities_section = listing.find("section", class_="card__amenities")
        amenities = {}
        if amenities_section:
            for amenity in amenities_section.find_all("p", class_="card__amenity"):
                amenity_label = (
                    amenity.find("span", role="document").get(
                        "aria-label", "Unknown Amenity"
                    )
                    if amenity.find("span", role="document")
                    else "N/A"
                )
                amenity_value = amenity.text.strip() if amenity else "N/A"
                amenities[amenity_label] = amenity_value

        data = {
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

        listing_class = Listing.from_web(data)

        print(listing_class.model_dump())
        print("----------------------------")
