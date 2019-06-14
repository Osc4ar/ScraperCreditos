from . import selenium_automaton
from selenium.webdriver.support.ui import Select
import time
import csv

class InbursaAutomaton(selenium_automaton.SeleniumAutomaton):
    def __init__(self):
        self.set_control_data()
        self.get_data()
        #self.driver.quit()

    def set_control_data(self):
        self.url = 'https://cotizatuseguro.inbursa.com/multiplataforma/mvc/banco/inburcasaPublic/init'
        self.apepat_xpath = '//*[@id="txt_inburcasa_apepat"]'
        self.apemat_xpath = '//*[@id="txt_inburcasa_apemat"]'
        self.nom_xpath = '//*[@id="txt_inburcasa_nombre"]'
        self.ingresos_solicitante_xpath = '//*[@id="txt_inburcasa_ingresot"]'
        self.correo_xpath = '//*[@id="txt_inburcasa_email"]'
        self.boton_aceptar_xpath = '//*[@id="modal_seleccion_riesgos"]/div/div/div[3]/button'
        self.select_destinos_xpath = '//*[@id="sel_inburcasa_destinocredito"]'
        self.valor_vivienda_xpath = '//*[@id="txt_inburcasa_valor_aprox_inmueble"]'
        self.enganche_xpath = '//*[@id="txt_inburcasa_enganche"]'
        self.select_plazo_xpath = '//*[@id="sel_inburcasa_plazo_credito"]'
        self.enganche_min_xpath = '//*[@id="txt_inburcasa_enganche_minimo"]'
        self.interes_anual_xpath = '//*[@id="txt_inburcasa_interesanual"]'
        self.ingresos_min_xpath = '//*[@id="txt_inburcasa_ingreso_minimo_requerido"]'
        self.boton_cotizar_xpath = '//*[@id="btnCotizarInburcasa"]'
        self.boton_tyc_xpath = '//*[@id="aviso_privacidad_si"]'
        self.pago_mensual_xpath = '//*[@id="tableCotizacion"]/div/table/tbody/tr[2]/td[4]/label'
        self.seccion1_xpath = '//*[@id="div_cotizacion_oculta"]/div[1]/div[1]/div/div[1]/ul/li[1]/a'
        self.seccion2_xpath = '//*[@id="div_cotizacion_oculta"]/div[1]/div[1]/div/div[1]/ul/li[2]/a'
        self.cat_xpath = '//*[@id="txt_inburcasa_cat"]'

    def get_data(self):
        self.get_productos()

    def get_userdata_controls(self):
        self.apepat = self.driver.find_element_by_xpath(self.apepat_xpath)
        self.apemat = self.driver.find_element_by_xpath(self.apemat_xpath)
        self.nom = self.driver.find_element_by_xpath(self.nom_xpath)
        self.ingresos_solicitante = self.driver.find_element_by_xpath(self.ingresos_solicitante_xpath)
        self.correo = self.driver.find_element_by_xpath(self.correo_xpath)

    def get_producto_controls(self):
        self.destinos = Select(self.driver.find_element_by_xpath(self.select_destinos_xpath))
        self.valor_vivienda = self.driver.find_element_by_xpath(self.valor_vivienda_xpath)
        self.select_plazo = Select(self.driver.find_element_by_xpath(self.select_plazo_xpath))
        self.enganche_min = self.driver.find_element_by_xpath(self.enganche_min_xpath)
        self.ingresos_min = self.driver.find_element_by_xpath(self.ingresos_min_xpath)
        self.interes_anual = self.driver.find_element_by_xpath(self.interes_anual_xpath)
        self.enganche = self.driver.find_element_by_xpath(self.enganche_xpath)
        self.boton_cotizar = self.driver.find_element_by_xpath(self.boton_cotizar_xpath)
        self.seccion1 = self.driver.find_element_by_xpath(self.seccion1_xpath)
        self.seccion2 = self.driver.find_element_by_xpath(self.seccion2_xpath)
        self.cat = self.driver.find_element_by_xpath(self.cat_xpath)

    def insert_basic_userdata(self):
        self.apepat.send_keys('A')
        self.apemat.send_keys('A')
        self.nom.send_keys('A')
        self.ingresos_solicitante.send_keys('100000')
        self.correo.send_keys('A@gmail.com')
        time.sleep(1)
        self.boton_aceptar = self.driver.find_element_by_xpath(self.boton_aceptar_xpath)
        self.boton_aceptar.click()
        time.sleep(1)

    def get_productos(self):
        #for _ in range(len(self.destinos.options)):
        self.data_dictionary = []
        for index, plazoID in enumerate(range(9, 20, 5)):
            self.get_subproductos(plazoID, index)
        #self.export_csv('inbursa.csv')

    def get_subproductos(self, plazoID, index):
        for i in ['50', '75', '100', '150', '200', '300', '400', '500']:
            self.connect(10)
            self.get_userdata_controls()
            self.insert_basic_userdata()
            self.get_producto_controls()
            #Extracting
            self.valor_vivienda.clear()
            self.valor_vivienda.send_keys(i + '0'*4)
            self.select_plazo.options[plazoID].click()
            time.sleep(3)
            new_enganche = self.enganche_min.get_attribute('value')
            self.enganche.clear()
            self.enganche.send_keys(new_enganche)
            self.select_plazo.options[plazoID].click()
            time.sleep(3)
            int_value = self.interes_anual.get_attribute("value")
            ing_min_req = self.ingresos_min.get_attribute("value")
            plazo_value = self.select_plazo.options[plazoID].text
            self.driver.execute_script('cotiza();')
            time.sleep(3)
            #self.pago_mensual = self.driver.find_element_by_xpath(self.pago_mensual_xpath)
            #valor_pago_mensual = self.pago_mensual.text
            cat = self.cat.get_attribute('value')
            print(f'Monto: {i+"0"*4}\tPlazo: {plazo_value}\tInteres: {int_value}\tIngresos minimos: {ing_min_req}\tEnganche: {new_enganche}\tCAT: {cat}')
            #Re-starting
            self.driver.quit()
            """self.data_dictionary.append({
                'Subproducto': index,
                'Producto': 'Inburcasa ',
                'Valor Vivienda': '$'+ i + '0'*4 +'.00',
                'AFORO': str(aforo)+'%',
                'Plazo': plazo_value,
                'Ingresos Requeridos': ing_min_req,
                'Tasa de Interes': int_value,
                'Tipo de Tasa': 'Fija',
                'CAT sin IVA': cat,
                'Pago': valor_pago_mensual,
                'Frecuencia de Pago': 'Mensual'
            })"""

    def export_csv(self, file_name):
        with open(file_name, mode='w', newline='') as csv_file:
            fieldnames = ['Subproducto', 'Producto', 'Valor Vivienda', 'AFORO', 'Plazo', 'Ingresos Requeridos', 'Tasa de Interes', 'Tipo de Tasa', 'CAT sin IVA', 'Pago', 'Frecuencia de Pago']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.data_dictionary:
                writer.writerow(row)