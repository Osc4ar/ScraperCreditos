insert into Instituciones(id_inst, nom_inst, web_madre_inst, web_credito_inst) values 
('040002', 'Banco Nacional de México', 'https://www.banamex.com/', 'https://www.banamex.com/es/personas/creditos/credito-hipotecario.html'),
('040036', 'Banco Inbursa', 'https://www.inbursa.com/', 'https://www.inbursa.com/portal/index.asp?page=document/doc_view_section.asp&id_document=878&id_category=36'),
('040044', 'Scotiabank Inverlat', 'https://www.scotiabank.com.mx/', 'https://www.scotiabank.com.mx/Personas/Creditos/Hipotecarios/default.aspx'),
('040058', 'Banco Regional de Monterrey', 'https://www.banregio.com/', 'https://www.banregio.com/creditos_hipoteca.php'),
('040072', 'Banco Mercantil del Norte', 'https://www.banorte.com', 'https://www.banorte.com/wps/portal/banorte/Home/creditos/credito-hipotecario');

insert into Productos(dest_id, id_inst, prod_nom, tiene_prog, cred_min, cred_max, cat_promedio) values 
('D01', '040002', 'HIPOTECA PERFILES', 'SI', 750000, 16000000, 11.7),
('D01', '040002', 'HIPOTECA PERFILES A TU MEDIDA', 'SI', 750000, 16000000, 11.7),
('D06', '040002', 'HIPOTECA PERFILES CAMBIA TU HIPOTECA', 'NO', 300000, 16000000, 11.4),
('D01', '040012', 'HIPOTECA BANCOMER FIJA', 'SI', 180000, 20000000, 15.2),
('D01', '040012', 'HIPOTECA BANCOMER CRECIENTE', 'SI', 180000, 20000000, 16.2),
('D01', '040012', 'HIPOTECA BANCOMER TU OPCIÓN EN MÉXICO', 'SI', 180000, 20000000, 16.5),
('D07', '040012', 'HIPOTECA BANCOMER FIJA LIQUIDEZ', 'NO', 180000, 10000000, 17.9),
('D06', '040012', 'HIPOTECA BANCOMER FIJA PAGO DE PASIVOS', 'NO', 50000, 18000000, 14.5),
('D05', '040012', 'HIPOTECA BANCOMER FIJA MEJORA TU CASA', 'NO', 180000, 20000000, 16.8),
('D02', '040012', 'HIPOTECA BANCOMER FIJA TERRENO', 'NO', 300000, 3000000, 16.6),
('D01', '040044', 'CREDIRESIDENCIAL', 'SI', 400000, 1000000, 11.3);

insert into Productos(dest_id, id_inst, prod_nom, tiene_prog, fiscal_id, cred_min, cred_max, cat_promedio) values 
('D01', '040021', 'CRÉDITO HIPOTECARIO HSBC PAGO FIJO', 'SI', 3, 350000, 10000000, 12.5),
('D01', '040021', 'CRÉDITO HIPOTECARIO HSBC PAGO FIJO PARA CLIENTES PREMIER', 'NO', 3, 350000, 10000000, 11.2),
('D06', '040021', 'PAGO DE HIPOTECA HSBC PAGO FIJO', 'SI', 3, 350000, 10000000, 12.0),
('D08', '040021', 'PAGO DE HIPOTECA MÁS LIQUIDEZ HSBC', 'SI', 3, 350000, 10000000, 12.7),
('D07', '040021', 'LIQUIDEZ HSBC', 'SI', 3, 350000, 5000000, 15.4);

insert into Productos(dest_id, id_inst, prod_nom, tiene_prog, fiscal_id, cred_min, cred_max, cat_promedio) values 
('D01', '040036', 'INBURCASA - ADQUISICIÓN VIVIENDA', 'SI', 3, 250000, 10000000, 14.2),
('D02', '040036', 'INBURCASA - ADQUISICIÓN TERRENO', 'SI', 3, 250000, 10000000, 14.2),
('D03', '040036', 'INBURCASA - CONSTRUCCIÓN VIVIENDA', 'SI', 3, 250000, 10000000, 14.2),
('D04', '040036', 'INBURCASA - CONSTRUCCIÓN TERRENO', 'SI', 3, 250000, 10000000, 14.2),
('D05', '040036', 'INBURCASA - REMODELACIÓN', 'NO', 3, 250000, 10000000, 14.2),
('D07', '040036', 'INBURCASA - LIQUIDEZ VIVIENDA', 'NO', 3, 250000, 10000000, 14.2),
('D07', '040036', 'INBURCASA - LIQUIDEZ TERRENO', 'NO', 3, 250000, 10000000, 14.2),
('D06', '040036', 'INBURCASA - SUSTITUCIÓN DE HIPOTECA VIVIENDA', 'NO', 3, 250000, 10000000, 14.2),
('D06', '040036', 'INBURCASA - SUSTITUCIÓN DE HIPOTECA TERRENO', 'NO', 3, 250000, 10000000, 14.2);

insert into Productos(dest_id, id_inst, prod_nom, tiene_prog, fiscal_id, cred_min, cred_max, cat_promedio) values 
('D01', '040072', 'HIPOTECA MÁS POR MENOS - ADQUIRIR UNA CASA', 'SI', 1, 350000, 10000000, 14.4),
('D01', '040072', 'HIPOTECA FUERTE - ADQUIRIR UNA CASA', 'NO', 1, 350000, 10000000, 12.3),
('D06', '040072', 'HIPOTECA MÁS POR MENOS - MEJORAR MI HIPOTECA', 'NO', 1, 350000, 10000000, 14.4),
('D06', '040072', 'HIPOTECA FUERTE - MEJORAR MI HIPOTECA', 'NO', 1, 350000, 10000000, 12.3),
('D10', '040072', 'HIPOTECA MÁS POR MENOS - MEJORAR MI HIPOTECA  CON REMODELACIÓN', 'NO', 1, 350000, 10000000, 14.4),
('D10', '040072', 'HIPOTECA FUERTE - MEJORAR MI HIPOTECA CON REMODELACIÓN', 'NO', 1, 350000, 10000000, 12.3),
('D03', '040072', 'HIPOTECA MÁS POR MENOS - CONSTRUIR', 'NO', 1, 500000, 10000000, 14.4),
('D03', '040072', 'HIPOTECA FUERTE - CONSTRUIR', 'NO', 1, 500000, 10000000, 12.3),
('D05', '040072', 'HIPOTECA MÁS POR MENOS - REMODELAR', 'NO', 1, 500000, 10000000, 14.4),
('D05', '040072', 'HIPOTECA FUERTE - REMODELAR', 'NO', 1, 500000, 10000000, 12.3),
('D04', '040072', 'HIPOTECA MÁS POR MENOS - TERRENO MÁS CONSTRUCCIÓN', 'NO', 1, 800000, 10000000, 14.4),
('D04', '040072', 'HIPOTECA FUERTE - TERRENO MÁS CONSTRUCCIÓN', 'NO', 1, 800000, 10000000, 12.3),
('D03', '040072', 'HIPOTECA MÁS POR MENOS - COMPRAVENTA CON TERMINACIÓN DE OBRA', 'NO', 1, 350000, 10000000, 14.4),
('D03', '040072', 'HIPOTECA FUERTE - COMPRAVENTA CON TERMINACIÓN DE OBRA', 'NO', 1, 350000, 10000000, 12.3);

CREATE VIEW ResumenSubproductos AS
SELECT S.subprod_id AS 'Subproducto',
    P.prod_nom AS 'Producto',
    M.mda_moneda AS 'Moneda',
    S.valor_vivienda AS 'Valor Vivienda',
    S.aforo AS 'Aforo',
    S.plazo AS 'Plazo',
    S.ingresos_requeridos AS 'Ingresos Requeridos',
    S.tasa_interes AS 'Tasa de Interés',
    T.tipo_tasa_des AS 'Tipo de Tasa',
    S.cat AS 'CAT',
    S.cat_incluye_iva AS 'CAT Incluye IVA',
    S.monto_pago AS 'Pago',
    F.frec_des AS 'Frecuencia de Pago',
    S.avaluo AS 'Avaluo',
    S.comision_por_apertura AS 'Comisión por Apertura',
    S.gastos_notariales AS 'Gastos Notariales',
    S.desembolso_inicial AS 'Desembolso Inicial'
FROM Subproductos AS S,
    Productos AS P,
    Destinos AS D,
    Instituciones AS I,
    TipoTasas AS T,
    Monedas AS M,
    RegimenFiscal AS R,
    FrecuenciaPago AS F;

CREATE VIEW ResumenSubproductos AS
SELECT S.subprod_id AS 'Subproducto',
    Instituciones.nom_inst AS 'Institución',
    Productos.prod_nom AS 'Producto',
    Destinos.dest_nom AS 'Destino',
    Monedas.mda_moneda AS 'Moneda',
    S.valor_vivienda AS 'Valor Vivienda',
    S.aforo AS 'Aforo',
    S.plazo AS 'Plazo',
    S.ingresos_requeridos AS 'Ingresos Requeridos',
    S.tasa_interes AS 'Tasa de Interés',
    TipoTasas.tipo_tasa_des AS 'Tipo de Tasa',
    S.cat AS 'CAT',
    S.cat_incluye_iva AS 'CAT Incluye IVA',
    S.monto_pago AS 'Pago',
    FrecuenciaPago.frec_des AS 'Frecuencia de Pago',
    S.avaluo AS 'Avaluo',
    S.comision_por_apertura AS 'Comisión por Apertura',
    S.gastos_notariales AS 'Gastos Notariales',
    S.desembolso_inicial AS 'Desembolso Inicial'
FROM Subproductos as S
NATURAL JOIN Productos
NATURAL JOIN TipoTasas
NATURAL JOIN Monedas
NATURAL JOIN Destinos
NATURAL JOIN Instituciones
NATURAL JOIN FrecuenciaPago;

SELECT S.subprod_id AS 'Subproducto',
    P.prod_nom AS 'Producto',
    M.mda_moneda AS 'Moneda',
    S.valor_vivienda AS 'Valor Vivienda',
    S.aforo AS 'Aforo',
    S.plazo AS 'Plazo',
    S.ingresos_requeridos AS 'Ingresos Requeridos',
    S.tasa_interes AS 'Tasa de Interés',
    T.tipo_tasa_des AS 'Tipo de Tasa',
    S.cat AS 'CAT',
    S.cat_incluye_iva AS 'CAT Incluye IVA',
    S.monto_pago AS 'Pago',
    F.frec_des AS 'Frecuencia de Pago',
    S.avaluo AS 'Avaluo',
    S.comision_por_apertura AS 'Comisión por Apertura',
    S.gastos_notariales AS 'Gastos Notariales',
    S.desembolso_inicial AS 'Desembolso Inicial'
FROM Subproductos AS S,
    Productos AS P,
    Destinos AS D,
    Instituciones AS I,
    TipoTasas AS T,
    Monedas AS M,
    RegimenFiscal AS R,
    FrecuenciaPago AS F;