from ..bank import Bank

class HSBC(Bank):
    def __init__(self):
        super().__init__()

    def set_selectors(self):
        self.creditos_selector = '//*[@class="A-LNKC28L-RW-ALL"]'
        self.url_container = '@href'
        self.url_target = '/hipotecario/productos/'
        self.exceptions = []