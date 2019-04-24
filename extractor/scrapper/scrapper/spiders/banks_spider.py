import scrapy
import csv

from ..bank import Bank
from ..bank_factory import BankFactory
from ..response_processor import ResponseProcessor

class BanksSpider(scrapy.Spider):
    name = "banks"

    def start_requests(self):
        with open('bancos.csv') as bancos:
            reader = csv.DictReader(bancos, delimiter=',')
            for row in reader:
                if row['Procesar'] == 'true':
                    yield scrapy.Request(url=row['URL'], callback=self.parse)

    def parse(self, response):
        bank_name = response.url.split('.')[1]
        bank = BankFactory.get_bank(bank_name)
        processor = ResponseProcessor(bank, response)
        for producto in processor.open_productos():
            next_page = response.urljoin(producto)
            request = scrapy.Request(next_page, callback=self.print_url)
            yield request

    def print_url(self, response):
        print('\n\n' + response.url + '\n\n')