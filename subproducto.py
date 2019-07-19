class Subproducto:
    def __init__(self,
                prod_id,
                valor_vivienda,
                aforo,
                plazo,
                ingresos_requeridos,
                tasa_interes,
                tipo_tasa_id,
                cat,
                cat_incluye_iva,
                monto_pago,
                avaluo,
                comision_por_apertura,
                gastos_notariales,
                desembolso_inicial
                ):
        self.prod_id = prod_id
        self.valor_vivienda = valor_vivienda
        self.aforo = aforo
        self.plazo = plazo
        self.ingresos_requeridos = ingresos_requeridos
        self.tasa_interes = tasa_interes
        self.tipo_tasa_id = tipo_tasa_id
        self.cat = cat
        self.cat_incluye_iva = cat_incluye_iva
        self.monto_pago = monto_pago
        self.avaluo = avaluo
        self.comision_por_apertura = comision_por_apertura
        self.gastos_notariales = gastos_notariales
        self.desembolso_inicial = desembolso_inicial