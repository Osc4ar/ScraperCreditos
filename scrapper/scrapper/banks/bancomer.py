from ..bank import Bank

class Bancomer(Bank):
    def __init__(self):
        super().__init__()

    def set_selectors(self):
        self.creditos_selector = '//*[@class="card__link"]'
        self.url_container = '@href'
        self.url_target = '/personas/productos/creditos/credito-hipotecario/'
        self.exceptions = ['programas-de-apoyo-al-credito.html']