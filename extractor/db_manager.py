import sqlite3

class DBManager:
    def __init__(self):
        self.create_connection_cursor()

    def close_connection(self):
        self.conn.commit()
        self.conn.close()

    def create_connection_cursor(self):
        try:
            self.conn = sqlite3.connect('./db/Credito.db')
            self.c = self.conn.cursor()
        except Exception as e:
            print(e)

    def insert_subproducto(self, subproducto):
        insert_producto_query = ''' INSERT INTO Subproductos(prod_id, valor_vivienda,
                                    aforo, plazo, ingresos_requeridos, tasa_interes,
                                    tipo_tasa_id, cat, cat_incluye_iva, monto_pago,
                                    avaluo, comision_por_apertura, gastos_notariales,
                                    desembolso_inicial) VALUES 
                                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        self.c.execute(insert_producto_query, subproducto)