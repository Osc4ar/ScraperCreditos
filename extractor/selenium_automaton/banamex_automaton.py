from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from . import selenium_automaton
import time
import csv

class BanamexAutomaton(selenium_automaton.SeleniumAutomaton):

    db_id_perfiles = 3
    db_id_perfiles_medida = 4
    db_id_cambia = 5
    ids_tipo_de_pago = [db_id_perfiles, db_id_perfiles_medida, db_id_cambia]

    def __init__(self):
        self.set_control_data()
        self.connect(10)
        self.get_controls()
        self.get_data()
        self.driver.quit()

    def set_control_data(self):
        self.url = 'https://www.banamex.com/es/personas/creditos/credito-hipotecario.html'
        self.cat_xpath = '/html/body/section/section/div/div/section/div[4]/div[4]/div/p[2]/span'
        self.aforo_xpath = '/html/body/section/section/div/div/section/div[4]/div[2]/div/p[2]'
        self.ingresos_xpath = '/html/body/section/section/div/div/section/div[4]/div[1]/div/p[2]'
        self.tasa_xpath = '/html/body/section/section/div/div/section/div[4]/div[3]/div/p[2]'
        self.pago_xpath = '/html/body/section/section/div/div/section/div[8]/div/p[2]'
        self.desembolso_inicial_xpath = '/html/body/section/section/div/div/section/div[7]/div/p[2]'
        self.comision_apertura_xpath = '/html/body/section/section/div/div/section/div[7]/table/tbody/tr[1]/td[2]'
        self.avaluo_xpath = '/html/body/section/section/div/div/section/div[7]/table/tbody/tr[3]/td[2]'
        self.gastos_notariales_xpath = '/html/body/section/section/div/div/section/div[7]/table/tbody/tr[5]/td[2]'
        self.plazos = [120, 180, 240]
        self.nombre_fija = '//*[@id="seccMobile"]/picture[2]/figcaption/div[2]/div/h3'
        self.nombre_creciente = '//*[@id="seccMobile"]/picture[1]/figcaption/div[2]/div/h3'
        self.resta_credito_xpath = '//*[@id="restaCredito_txt"]'
        self.valor_aprox_xpath = '//*[@id="valorAprox_txt"]'

    def get_controls(self):
        self.switch_to_frame('/html/body/section[5]/div[2]/div/div/iframe')
        self.comprar_casa = self.driver.find_element_by_id('dec1')
        self.cambiar_hipoteca = self.driver.find_element_by_id('dec2')
        self.pagos_fijos = self.driver.find_element_by_id('pfijos')
        self.pagos_crecientes = self.driver.find_element_by_id('pcrecientes')
        self.list_buttons_pagos = [self.pagos_fijos, self.pagos_crecientes]
        self.valor_vivienda = self.driver.find_element_by_id('vvivienda')
        self.select_enganche = Select(self.driver.find_element_by_id('enganche'))
        self.plazo_10_anios = self.driver.find_element_by_xpath('//*[@id="itiempo"]/div[2]/div[1]/div/button')
        self.plazo_15_anios = self.driver.find_element_by_xpath('//*[@id="itiempo"]/div[2]/div[2]/div/button')
        self.plazo_20_anios = self.driver.find_element_by_xpath('//*[@id="itiempo"]/div[2]/div[3]/div/button')
        self.list_buttons_plazos = [self.plazo_10_anios, self.plazo_15_anios, self.plazo_20_anios]

    def get_data(self):
        self.data = []
        self.valor_vivienda.click()
        for tipo_pago in range(len(self.list_buttons_pagos)):
            self.list_buttons_pagos[tipo_pago].click()
            if tipo_pago == 0:
                self.iterate_plazo(tipo_pago)
            else:
                self.iterate_enganche(tipo_pago)
        self.process_cambiar_hipoteca()
        self.save_data_to_db()

    def iterate_plazo(self, tipo_pago):
        for plazo in range(len(self.list_buttons_plazos)):
            self.list_buttons_plazos[plazo].click()
            self.iterate_enganche(tipo_pago, plazo)

    def iterate_enganche(self, tipo_pago, plazo=2):
        for enganche in range(3):
            self.select_enganche.select_by_index(enganche)
            self.iterate_valor_vivienda(tipo_pago, plazo)

    def iterate_valor_vivienda(self, tipo_pago, plazo):
        self.input_valor_vivienda = self.driver.find_element_by_id('slider_valorCasa_txt')
        self.append_values(tipo_pago, plazo, self.input_valor_vivienda)

    def append_values(self, tipo_pago, plazo, input_element):
        self.fails = []
        for i in range(8, 21):
            self.process_value(i, tipo_pago, plazo, input_element)
        for i in range(25, 105, 5):
            self.process_value(i, tipo_pago, plazo, input_element)

    def process_value(self, value, tipo_pago, plazo, input_element):
        input_value = str(value) + '0'*5
        self.insert_value(input_element, input_value)
        self.find_tags()
        self.extract_data_from_tags(input_value)
        self.append_extracted_data(tipo_pago, plazo)

    def insert_value(self, input_control, value):
        try:
            webdriver.ActionChains(self.driver).click(input_control).send_keys(value, Keys.ENTER).perform()
            return True
        except:
            if not value in self.fails:
                self.fails.append(value)
            return False

    def process_cambiar_hipoteca(self):
        self.cambiar_hipoteca.click()
        self.get_controls_cambiar()
        for plazo in range(len(self.list_buttons_plazos)):
            self.list_buttons_plazos[plazo].click()
            for i in range(8, 21):
                self.insert_value_and_aforo(i)
                self.find_tags()
                self.extract_data_from_tags(str(i))
                self.append_extracted_data(2, plazo)
            for i in range(25, 105, 5):
                self.insert_value_and_aforo(i)
                self.find_tags()
                self.extract_data_from_tags(str(i))
                self.append_extracted_data(2, plazo)

    def get_controls_cambiar(self):
        self.valor_aprox = self.driver.find_element_by_xpath(self.valor_aprox_xpath)
        self.resta_credito = self.driver.find_element_by_xpath(self.resta_credito_xpath)

    def insert_value_and_aforo(self, value):
        numerical_value = int(str(value) + '0'*5)
        aforo = numerical_value*0.85
        self.insert_value(self.valor_aprox, str(numerical_value))
        self.insert_value(self.resta_credito, str(aforo)[:-2])

    def find_tags(self):
        self.cat_tag = self.driver.find_element_by_xpath(self.cat_xpath)
        self.aforo_tag = self.driver.find_element_by_xpath(self.aforo_xpath)
        self.ingresos_tag = self.driver.find_element_by_xpath(self.ingresos_xpath)
        self.tasa_tag = self.driver.find_element_by_xpath(self.tasa_xpath)
        self.pago_tag = self.driver.find_element_by_xpath(self.pago_xpath)
        self.avaluo_tag = self.driver.find_element_by_xpath(self.avaluo_xpath)
        self.comision_apertura_tag = self.driver.find_element_by_xpath(self.comision_apertura_xpath)
        self.gastos_notariales_tag = self.driver.find_element_by_xpath(self.gastos_notariales_xpath)
        self.desembolso_inicial_tag = self.driver.find_element_by_xpath(self.desembolso_inicial_xpath)

    def extract_data_from_tags(self, valor):
        self.value_vvienda = valor + '0'*5
        self.value_cat = self.cat_tag.text[:-2]
        self.value_aforo = self.aforo_tag.text[:-1]
        self.value_ingresos = self.ingresos_tag.text[2:].replace(',', '')
        self.value_tasa = self.tasa_tag.text[:-2]
        self.value_pago = self.pago_tag.text[2:].replace(',', '')
        self.value_avaluo = self.avaluo_tag.text[2:].replace(',', '')
        self.value_comision = self.comision_apertura_tag.text[2:].replace(',', '')
        self.value_gastos = self.gastos_notariales_tag.text[2:].replace(',', '')
        self.value_desembolso = self.desembolso_inicial_tag.text[2:].replace(',', '')

    def append_extracted_data(self, tipo_pago, plazo):
        self.data.append((
            self.ids_tipo_de_pago[tipo_pago],
            self.value_vvienda,
            self.value_aforo,
            self.plazos[plazo],
            self.value_ingresos,
            self.value_tasa,
            int(tipo_pago == 1),
            self.value_cat,
            0,
            self.value_pago,
            self.value_avaluo,
            self.value_comision,
            self.value_gastos,
            self.value_desembolso
        ))
