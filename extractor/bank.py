from ..db_manager import DBManager

class Bank:
    def __init__(self):
        self.productos = []
        self.dbManager = DBManager()

    def extract(self):
        raise NotImplementedError

    def save(self):
        for producto in self.productos:
            self.dbManager.insert_producto(producto)