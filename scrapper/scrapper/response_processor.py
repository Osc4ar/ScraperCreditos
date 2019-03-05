class ResponseProcessor():
    def __init__(self, bank, response):
        self.bank = bank
        self.response = response

    def open_productos(self):
        productos = self.response.xpath(self.bank.creditos_selector)
        target_url_end = len(self.bank.url_target)
        urls = []
        for producto in productos:
            url = producto.xpath(self.bank.url_container).get()
            if target_url_end == 0 or url[:target_url_end] == self.bank.url_target:
                if url[target_url_end:] not in self.bank.exceptions:
                    urls.append(url)
        return urls