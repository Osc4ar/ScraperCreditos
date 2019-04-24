import sqlite3
import producto

class DBManager:

    def __init__(self):
        self.create_connection_cursor()

    def close_connection(self):
        self.conn.commit()
        self.conn.close()

    def create_connection_cursor(self):
        self.conn = sqlite3.connect('./db/Credito.db')
        self.c = self.conn.cursor()

    def insert_producto(self, producto):
        attributes = producto.get_attributes_name()
        values = producto.get_attributes_value()
        insert_producto_query = 'INSERT INTO Productos(%s) VALUES (?,?,?,?,?,?,?,?,?,?)' % ','.join(attributes)
        self.c.execute(insert_producto_query, values)

    def update_producto(self, producto):
        attributes = producto.get_attributes_name()
        attributes_expr = self.parse_attributes_for_update(attributes)
        values = producto.get_attributes_value()
        update_producto_query = f'UPDATE Productos SET {attributes_expr} WHERE '
        self.c.execute(update_producto_query, values)

    def get_productos(self):
        pass

    def insert_subproducto(self, subproducto):
        attributes = subproducto.get_attributes_name()
        values = subproducto.get_attributes_value()
        insert_producto_query = 'INSERT INTO Productos(%s) VALUES (?,?,?,?,?,?,?,?,?)' % ','.join(attributes)
        self.c.execute(insert_producto_query, values)

    def update_subproducto(self, subproducto):
        pass

    def parse_attributes_for_update(self, attributes):
        expr = ''
        for attribute in attributes:
            expr = expr + attribute + '=?'
            if attribute != attributes[-1]:
                expr = expr + ','
            expr = expr + ' '
        return expr