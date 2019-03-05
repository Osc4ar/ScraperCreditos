class Bank:
    def __init__(self):
        self.set_selectors()

    def set_selectors(self):
        self.creditos_selector = '//*'
        self.url_container = '@href'
        self.url_target = '/'
        self.exceptions = []