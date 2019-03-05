from ..bank import Bank

class Banregio(Bank):
    def __init__(self):
        super().__init__()

    def set_selectors(self):
        self.creditos_selector = '//*[@class="cta small m10"]'
        self.url_container = '@href'
        self.url_target = ''
        self.exceptions = []