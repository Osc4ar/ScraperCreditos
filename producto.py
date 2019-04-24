class Producto:
    def __init__(self, dest_id, id_inst, prod_nom, tiene_prog, mda_id, fiscal_id, frec_id, cred_min, cred_max, cat_promedio):
        self.dest_id = dest_id
        self.id_inst = id_inst
        self.prod_nom = prod_nom
        self.tiene_prog = tiene_prog
        self.mda_id = mda_id
        self.fiscal_id = fiscal_id
        self.frec_id = frec_id
        self.cred_min = cred_min
        self.cred_max = cred_max
        self.cat_promedio = cat_promedio

    def get_attributes_name(self):
        return [attribute for attribute in dir(self) if not (attribute.startswith('__') or attribute.startswith('get'))]

    def get_attributes_value(self):
        values = []
        for attribute in self.get_attributes_name():
            values.append(getattr(self, attribute))
        return tuple(values)