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
        self.cerrar_detalle_xpath = '/html/body/div/div[1]/div[1]/a'

    def get_data(self):
        self.data_dictionary = []
        self.subproducto_id = 1
        for value in range(5, 21):
            self.send_values(value)
            self.subproducto_id += 1
        for value in range(25, 105, 5):
            self.send_values(value)
            self.subproducto_id += 1
        self.export_csv('banregio.csv')

    def get_controls(self):
        self.pagos_crecientes = self.driver.find_element_by_xpath(self.pagos_crecientes_xpath)
        self.pagos_fijos = self.driver.find_element_by_xpath(self.pagos_fijos_xpath)
        self.tipo_pagos = [self.pagos_crecientes, self.pagos_fijos]
        self.valor = self.driver.find_element_by_xpath(self.valor_xpath)
        self.ingresos = self.driver.find_element_by_xpath(self.ingresos_xpath)
        self.submit = self.driver.find_element_by_xpath(self.submit_xpath)
        self.select_seguro = Select(self.driver.find_element_by_xpath(self.select_seguro_xpath))
        self.select_plazos = Select(self.driver.find_element_by_xpath(self.select_plazos_xpath))
        self.select_financiamiento = Select(self.driver.find_element_by_xpath(self.select_financiamiento_xpath))
        self.select_estado = Select(self.driver.find_element_by_xpath(self.select_estado_xpath))

    def send_values(self, value):
        for plazo in [4, 9, 19]:
            time.sleep(1)
            self.get_controls()
            self.pagos_fijos.click()
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
        self.get_controls()
        self.pagos_crecientes.click()
        self.select_seguro.options[0].click()
        self.select_plazos.options[1].click()
        self.valor.clear()
        self.valor.send_keys(str(value) + '0'*5)
        self.select_financiamiento.options[12].click()
        self.select_estado.options[9].click()
        self.ingresos.clear()
        self.ingresos.send_keys('1'+'0'*5)
        self.submit.click()
        self.extract_data()

    def extract_data(self):
        time.sleep(4)
        self.open_detalle()
        self.get_data_elements()
        self.append_data()
        self.close_detalle()

    def open_detalle(self):
        self.ver_detalle = self.driver.find_element_by_xpath(self.ver_detalle_xpath)
        self.ver_detalle.click()
        time.sleep(1)

    def get_data_elements(self):
        self.tasa_anual = self.driver.find_element_by_xpath(self.tasa_anual_xpath)
        self.pago_mensual = self.driver.find_element_by_xpath(self.pago_mensual_xpath)
        self.valor_inmueble = self.driver.find_element_by_xpath(self.valor_inmueble_xpath)
        self.monto_credito = self.driver.find_element_by_xpath(self.monto_credito_xpath)
        self.ingresos_min = self.driver.find_element_by_xpath(self.ingresos_min_xpath)
        self.plazo = self.driver.find_element_by_xpath(self.plazo_xpath)
        self.factor_pago = self.driver.find_element_by_xpath(self.factor_pago_xpath)
        self.cerrar_detalle = self.driver.find_element_by_xpath(self.cerrar_detalle_xpath)

    def append_data(self):
        f_monto = float(self.monto_credito.text.replace(',', '').replace('$', ''))
        f_valor = float(self.valor_inmueble.text.replace(',', '').replace('$', ''))
        self.data_dictionary.append({
            'Subproducto': self.subproducto_id,
            'Producto': 'Adquisición de Vivienda',
            'Valor Vivienda': self.valor_inmueble.text,
            'AFORO': f_monto/f_valor*100,
            'Plazo': self.plazo.text,
            'Ingresos Requeridos': self.ingresos_min.text,
            'Tasa de Interes': self.tasa_anual.text,
            'Tipo de Tasa': 'Creciente',
            'CAT sin IVA': self.factor_pago.text,
            'Pago': self.pago_mensual.text,
            'Frecuencia de Pago': 'Mensual'
        })

    def close_detalle(self):
        self.cerrar_detalle = self.driver.find_element_by_xpath(self.cerrar_detalle_xpath)
        self.cerrar_detalle.click()
        time.sleep(1)