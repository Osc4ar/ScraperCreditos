CREATE TABLE IF NOT EXISTS "Productos"(
        prod_id integer PRIMARY KEY AUTOINCREMENT,
        dest_id varchar(3) DEFAULT 'D01',
        id_inst varchar(10) NOT NULL,
        prod_nom varchar(250) NOT NULL,
        tiene_prog varchar(100) DEFAULT 'NO',
        mda_id int DEFAULT 1,
        fiscal_id int DEFAULT 1,
        frec_id int DEFAULT 3,
        fecha_consulta_prod timestamp DEFAULT CURRENT_TIMESTAMP,
        cred_min real DEFAULT 0.0,
        cred_max real DEFAULT 0.0,
        cat_promedio real DEFAULT 0.0,
        FOREIGN KEY(dest_id) REFERENCES Destinos
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        FOREIGN KEY(id_inst) REFERENCES Instituciones(id_inst)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        FOREIGN KEY(mda_id) REFERENCES Monedas(mda_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        FOREIGN KEY(fiscal_id) REFERENCES RegimenFiscal(fiscal_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        FOREIGN KEY(frec_id) REFERENCES FrecuenciaPago(frec_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS "Subproductos"(
        subprod_id INTEGER PRIMARY KEY AUTOINCREMENT,
        prod_id integer,
        valor_vivienda int DEFAULT 0,
        aforo real DEFAULT 65.0,
        plazo int DEFAULT 120,
        ingresos_requeridos real DEFAULT 0.0,
        tasa_interes real DEFAULT 0.0,
        tipo_tasa_id int DEFAULT 1,
        cat real DEFAULT 0.0,
        cat_incluye_iva int DEFAULT 0,
        monto_pago real DEFAULT 0.0,
        FOREIGN KEY(prod_id) REFERENCES Productos(prod_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        FOREIGN KEY(tipo_tasa_id) REFERENCES TipoTasas(tipo_tasa_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE VIEW ResumenSubproductos AS
SELECT
  S.subprod_id,
  S.prod_id,
  S.valor_vivienda,
  S.aforo,
  S.plazo,
  S.ingresos_requeridos,
  S.tasa_interes,
  T.tipo_tasa_des,
  S.cat,
  S.cat_incluye_iva,
  S.monto_pago
FROM
  Subproductos as S,
  Productos as P,
  TipoTasas as T
WHERE
  S.prod_id = P.prod_id AND
  S.tipo_tasa_id = T.tipo_tasa_id;

CREATE VIEW ResumenProductos AS
SELECT
  P.prod_id,
  D.dest_nom,
  I.nom_inst, 
  P.prod_nom,
  P.tiene_prog,
  M.mda_moneda,
  Fisc.fiscal_nom,
  Frec.frec_des,
  P.fecha_consulta_prod,
  P.cred_min,
  P.cred_max,
  P.cat_promedio
FROM
  Productos as P,
  Destinos as D,
  Instituciones as I,
  Monedas as M,
  RegimenFiscal as Fisc,
  FrecuenciaPago as Frec
WHERE
  P.dest_id = D.dest_id AND
  P.id_inst = I.id_inst AND
  P.mda_id = M.mda_id AND
  P.fiscal_id = Fisc.fiscal_id AND
  P.frec_id = Frec.frec_id;

INSERT INTO Productos(dest_id, id_inst, prod_nom, tiene_prog, mda_id, fiscal_id, frec_id, cred_min, cred_max, cat_promedio) VALUES ('D01','040012','Prueba Manager','NO',1,1,3,100000.0,10000000.0,11.1);
INSERT INTO Productos(dest_id, id_inst, prod_nom, tiene_prog, mda_id, fiscal_id, frec_id, cred_min, cred_max, cat_promedio) VALUES ('D01','040021','Prueba 2 Manager','NO',1,1,3,100000.0,10000000.0,14.4);

INSERT INTO Subproductos(prod_id, valor_vivienda, aforo, plazo, ingresos_requeridos, tasa_interes, tipo_tasa_id, cat, monto_pago) VALUES (1, 5000000.0, 75, 120, 20000.0, 10.0, 0, 11.3, 10000.0);
INSERT INTO Subproductos(prod_id, valor_vivienda, aforo, plazo, ingresos_requeridos, tasa_interes, tipo_tasa_id, cat, monto_pago) VALUES (2, 2000000.0, 80, 180, 17000.0, 9.0, 0, 14.3, 8000.0);