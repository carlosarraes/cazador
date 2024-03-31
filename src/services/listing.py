from adapters import dao
import models
from utils.scraper import ZapScraper

ZAP_URL = "https://www.zapimoveis.com.br/venda/apartamentos/sc+palhoca++pedra-branca/?__ab=exp-aa-test:B,rec-cta:control&transacao=venda&onde=,Santa%20Catarina,Palho%C3%A7a,,Pedra%20Branca,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EPalhoca%3EBarrios%3EPedra%20Branca,-27.662428,-48.661448,;,Santa%20Catarina,Palho%C3%A7a,,Pagani,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EPalhoca%3EBarrios%3EPagani,-27.640739,-48.685468,&tipos=apartamento_residencial&pagina=1&quartos=3,4&precoMaximo=550000"


class Listing:
    def __init__(self, dao: dao.Listing) -> None:
        self.dao = dao
        self.scraper = ZapScraper(ZAP_URL)

    def get_all(self) -> list[models.Listing]:
        return self.dao.get_all()

    def update(self) -> None:
        self.dao.update(self.scraper.run())

    def debug(self) -> None:
        listings = self.scraper.run()
        print(len(listings))
        print(listings[0])
