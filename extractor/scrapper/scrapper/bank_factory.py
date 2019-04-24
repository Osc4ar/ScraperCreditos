from .banks import bancomer
from .banks import banregio
from .banks import hsbc

class BankFactory:
    bank_classes = {
        'bancomer': bancomer.Bancomer,
        'banregio': banregio.Banregio,
        'hsbc': hsbc.HSBC
    }

    @staticmethod
    def get_bank(bank_name):
        bank_class = BankFactory.bank_classes[bank_name]
        return bank_class()