import os
from adapters import dao
import models
from utils.scraper import ZapScraper


class Listing:
    def __init__(self, dao: dao.Listing) -> None:
        self.dao = dao
        self.scraper = ZapScraper(os.getenv("ZAP_URL", "default_url_if_not_set"))

    def get_all(self) -> list[models.Listing]:
        return self.dao.get_all()

    def update(self) -> None:
        self.dao.update(self.scraper.run())

    def debug(self) -> None:
        listings = self.scraper.run()
        print(len(listings))
        print(listings[0])
