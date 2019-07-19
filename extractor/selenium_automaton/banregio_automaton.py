from . import selenium_automaton
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BanregioAutomaton(selenium_automaton.SeleniumAutomaton):
    def __init__(self):
        self.set_control_data()
        self.connect(10)
        self.get_data()
        self.driver.quit()

    def set_control_data(self):
        self.url = 'https://www.banregio.com/cot_nueva.php'
        self.submit_xpath = '/html/body/section[2]/div[2]/div[2]/div/div[1]/div/div/form/div[7]/div[2]/input'
        self.pagos_fijos_xpath = '/html/body/section[2]/div[2]/div[2]/div/div[1]/div/div/form/div[1]/div[1]/div[1]/label'
        self.pagos_crecientes_xpath = '/html/body/section[2]/div[2]/div[2]/div/div[1]/div/div/form/div[1]/div[1]/div[2]/label'
        self.select_seguro_xpath = '//*[@id="CoA"]'
        self.select_plazos_xpath = '//*[@id="plazo"]'
        self.select_financiamiento_xpath = '//*[@id="porc"]'
        self.select_estado_xpath = '//*[@id="estados"]'
        self.valor_xpath = '//*[@id="Valor"]'
        self.ver_detalle_xpath = '/html/body/section[1]/div/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[2]/a'
        self.ingresos_xpath = '//*[@id="Sueldo"]'
        self.tasa_anual_xpath = '//*[@id="divTasaanual"]'
        self.pago_mensual_xpath = '//*[@id="divmesint"]'
        self.valor_inmueble_xpath = '//*[@id="divvalor"]'
        self.monto_credito_xpath = '//*[@id="divmontonormal"]'
        self.ingresos_min_xpath = '//*[@id="divingresosminimos"]'
        self.plazo_xpath = '//*[@id="divplazo"]'
        self.factor_pago_xpath = '//*[@id="divfactortotal"]'
        self.avaluo_xpath = '//*[@id="divavaluo"]'
        self.comision_xpath = '//*[@id="divapertura"]'
        self.gastos_notariales_xpath = '//*[@id="divnotariales"]'
        self.desembolso_inicial_xpath = '//*[@id="divinicial"]'
        self.cerrar_detalle_xpath = '/html/body/div/div[1]/div[1]/a'

    def get_data(self):
        #self.data_dictionary = []
        self.data = []
        for value in range(5, 21):
            self.send_values(value)
        for value in range(25, 105, 5):
            self.send_values(value)
        #self.export_csv('banregio.csv')
        self.save_data_to_db()

    def get_controls(self):
        self.get_tipos_pagos()
        self.valor = self.driver.find_element_by_xpath(self.valor_xpath)
        self.ingresos = self.driver.find_element_by_xpath(self.ingresos_xpath)
        self.submit = self.driver.find_element_by_xpath(self.submit_xpath)
        self.select_seguro = Select(self.driver.find_element_by_xpath(self.select_seguro_xpath))
        self.select_plazos = Select(self.driver.find_element_by_xpath(self.select_plazos_xpath))
        self.select_financiamiento = Select(self.driver.find_element_by_xpath(self.select_financiamiento_xpath))
        self.select_estado = Select(self.driver.find_element_by_xpath(self.select_estado_xpath))

    def get_tipos_pagos(self):
        self.pagos_crecientes = self.driver.find_element_by_xpath(self.pagos_crecientes_xpath)
        self.pagos_fijos = self.driver.find_element_by_xpath(self.pagos_fijos_xpath)
        self.tipo_pagos = [self.pagos_crecientes, self.pagos_fijos]

    def send_values(self, value):
        for plazo in [4, 9, 19]:
            self.perform_actions(value, plazo, False)
        self.perform_actions(value, 1, True)

    def perform_actions(self, value, plazo, pago_creciente):
        time.sleep(1)
        self.get_controls()
        if not pago_creciente:
            self.pagos_fijos.click()
        else:
            self.pagos_crecientes.click()
        self.select_seguro.options[0].click()
        self.select_plazos.options[plazo].click()
        self.valor.clear()
        self.valor.send_keys(str(value) + '0'*5)
        self.select_financiamiento.options[12].click()
        self.select_estado.options[9].click()
        self.ingresos.clear()
        self.ingresos.send_keys('1'+'0'*5)
        self.submit.click()
        self.extract_data()

    def extract_data(self):
        time.sleep(5)
        self.open_detalle()
        self.get_data_elements()
        self.append_data()
        self.close_detalle()

    def open_detalle(self):
        self.ver_detalle = self.driver.find_element_by_xpath(self.ver_detalle_xpath)
        self.ver_detalle.click()
        time.sleep(1.5)

    def get_data_elements(self):
        self.tasa_anual = self.driver.find_element_by_xpath(self.tasa_anual_xpath)
        self.pago_mensual = self.driver.find_element_by_xpath(self.pago_mensual_xpath)
        self.valor_inmueble = self.driver.find_element_by_xpath(self.valor_inmueble_xpath)
        self.monto_credito = self.driver.find_element_by_xpath(self.monto_credito_xpath)
        self.ingresos_min = self.driver.find_element_by_xpath(self.ingresos_min_xpath)
        self.avaluo = self.driver.find_element_by_xpath(self.avaluo_xpath)
        self.comision = self.driver.find_element_by_xpath(self.comision_xpath)
        self.gastos_notariales = self.driver.find_element_by_xpath(self.gastos_notariales_xpath)
        self.desembolso_inicial = self.driver.find_element_by_xpath(self.desembolso_inicial_xpath)
        self.plazo = self.driver.find_element_by_xpath(self.plazo_xpath)
        self.factor_pago = self.driver.find_element_by_xpath(self.factor_pago_xpath)
        self.cerrar_detalle = self.driver.find_element_by_xpath(self.cerrar_detalle_xpath)

    def append_data(self):
        f_monto = float(self.monto_credito.text.replace(',', '').replace('$', ''))
        f_valor = float(self.valor_inmueble.text.replace(',', '').replace('$', ''))
        '''self.data_dictionary.append({
            'Producto': self.get_producto_id_from_url(),
            'Valor Vivienda': self.clean_float_number(self.valor_inmueble.text),
            'AFORO': f_monto/f_valor*100,
            'Plazo': self.get_plazo_in_months(self.plazo.text),
            'Ingresos Requeridos': self.clean_float_number(self.ingresos_min.text),
            'Tasa de Interes': self.clean_float_number(self.tasa_anual.text),
            'Tipo de Tasa': 0,
            'CAT': self.factor_pago.text,
            'Incluye IVA': 0,
            'Pago': self.clean_float_number(self.pago_mensual.text),
            'Avaluo': self.clean_float_number(self.avaluo.text),
            'Comision': self.clean_float_number(self.comision.text),
            'Gastos Notariales': self.clean_float_number(self.gastos_notariales.text),
            'Desembolso Inicial': self.clean_float_number(self.desembolso_inicial.text)
        })'''
        self.data.append((
            self.get_producto_id_from_url(),
            self.clean_float_number(self.valor_inmueble.text),
            f_monto/f_valor*100,
            self.get_plazo_in_months(self.plazo.text),
            self.clean_float_number(self.ingresos_min.text),
            self.clean_float_number(self.tasa_anual.text),
            0,
            self.factor_pago.text,
            0,
            self.clean_float_number(self.pago_mensual.text),
            self.clean_float_number(self.avaluo.text),
            self.clean_float_number(self.comision.text),
            self.clean_float_number(self.gastos_notariales.text),
            self.clean_float_number(self.desembolso_inicial.text)
        ))

    def get_producto_id_from_url(self):
        if 'nueva' in self.url:
            return 14
        if 'terreno' in self.url:
            return 15
        if 'term' in self.url:
            return 16
        if 'mejora' in self.url:
            return 17
        if 'remo' in self.url:
            return 18

    def get_plazo_in_months(self, text_plazo):
        if '20' in text_plazo:
            return 240
        if '15' in text_plazo:
            return 180
        if '10' in text_plazo:
            return 120
        if '5' in text_plazo:
            return 60

    def close_detalle(self):
        self.cerrar_detalle = self.driver.find_element_by_xpath(self.cerrar_detalle_xpath)
        self.cerrar_detalle.click()
        time.sleep(1.5)