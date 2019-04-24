from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from . import selenium_automaton
import time
import csv

class BanamexAutomaton(selenium_automaton.SeleniumAutomaton):

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
        self.plazos = [120, 180, 240]
        #self.valores_vivienda = [5, 59, 60, 119, 120, 150]
        #self.montos_credito = [4, 5, 10, 44, 50, 51, 65, 100]
        self.valores_vivienda = [75, 590, 600, 1190, 1200, 1600]
        self.montos_credito = [75, 100, 440, 500, 510, 650, 1000]
        self.tipos_tasa = ['Fija', 'Creciente']
        self.nombre_fija = '//*[@id="seccMobile"]/picture[2]/figcaption/div[2]/div/h3'
        self.nombre_creciente = '//*[@id="seccMobile"]/picture[1]/figcaption/div[2]/div/h3'

    def get_controls(self):
        self.switch_to_frame('/html/body/section[5]/div[2]/div/div/iframe')
        self.comprar_casa = self.driver.find_element_by_id('dec1')
        self.cambiar_hipoteca = self.driver.find_element_by_id('dec2')
        self.pagos_fijos = self.driver.find_element_by_id('pfijos')
        self.pagos_crecientes = self.driver.find_element_by_id('pcrecientes')
        self.list_buttons_pagos = [self.pagos_fijos, self.pagos_crecientes]
        self.valor_vivienda = self.driver.find_element_by_id('vvivienda')
        self.monto_credito = self.driver.find_element_by_id('mcredito')
        self.select_enganche = Select(self.driver.find_element_by_id('enganche'))
        self.plazo_10_anios = self.driver.find_element_by_xpath('//*[@id="itiempo"]/div[2]/div[1]/div/button')
        self.plazo_15_anios = self.driver.find_element_by_xpath('//*[@id="itiempo"]/div[2]/div[2]/div/button')
        self.plazo_20_anios = self.driver.find_element_by_xpath('//*[@id="itiempo"]/div[2]/div[3]/div/button')
        self.list_buttons_plazos = [self.plazo_10_anios, self.plazo_15_anios, self.plazo_20_anios]

    def get_data(self):
        self.data_dictionary = []
        self.monto_credito.click()
        for tipo_pago in range(len(self.list_buttons_pagos)):
            self.list_buttons_pagos[tipo_pago].click()
            if tipo_pago == 0:
                self.iterate_plazo(tipo_pago)
            else:
                self.iterate_enganche(tipo_pago)
        self.export_csv('valor_vivienda.csv')

    def iterate_plazo(self, tipo_pago):
        for plazo in range(len(self.list_buttons_plazos)):
            self.list_buttons_plazos[plazo].click()
            self.iterate_enganche(tipo_pago, plazo)

    def iterate_enganche(self, tipo_pago, plazo=2):
        for enganche in range(3):
            self.select_enganche.select_by_index(enganche)
            #self.iterate_valor_vivienda(tipo_pago, plazo)
            self.iterate_monto_credito(tipo_pago, plazo)

    def iterate_valor_vivienda(self, tipo_pago, plazo):
        self.input_valor_vivienda = self.driver.find_element_by_id('slider_valorCasa_txt')
        self.append_values(tipo_pago, plazo, self.valores_vivienda, self.input_valor_vivienda)

    def iterate_monto_credito(self, tipo_pago, plazo):
        self.input_monto_credito = self.driver.find_element_by_id('slider_montoCredito_txt')
        self.valor_vivienda_tag = self.driver.find_element_by_xpath('/html/body/section/section/div/div/section/div[1]/p[2]')
        self.append_values(tipo_pago, plazo, self.montos_credito, self.input_monto_credito)

    def append_values(self, tipo_pago, plazo, values, input_element):
        self.fails = []
        for i in values:
            input_value = str(i) + '0'*4
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

    def find_tags(self):
        self.cat_tag = self.driver.find_element_by_xpath(self.cat_xpath)
        self.aforo_tag = self.driver.find_element_by_xpath(self.aforo_xpath)
        self.ingresos_tag = self.driver.find_element_by_xpath(self.ingresos_xpath)
        self.tasa_tag = self.driver.find_element_by_xpath(self.tasa_xpath)
        self.pago_tag = self.driver.find_element_by_xpath(self.pago_xpath)

    def extract_data_from_tags(self, valor):
        self.value_valor = self.valor_vivienda_tag.text[2:].replace(',', '')
        self.value_cat = self.cat_tag.text[:-2]
        self.value_aforo = self.aforo_tag.text[:-1]
        self.value_ingresos = self.ingresos_tag.text[2:].replace(',', '')
        self.value_tasa = self.tasa_tag.text[:-2]
        self.value_pago = self.pago_tag.text[2:].replace(',', '')

    def append_extracted_data(self, tipo_pago, plazo):
        self.data_dictionary.append({
            'Valor Vivienda': self.value_valor,
            'Plazo': self.plazos[plazo],
            'AFORO': self.value_aforo,
            'Ingresos Requeridos': self.value_ingresos,
            'Tasa de Interes': self.value_tasa,
            'Tipo de Tasa': self.tipos_tasa[tipo_pago],
            'CAT sin IVA': self.value_cat,
            'Pago Mensual': self.value_pago
        })

    def export_csv(self, file_name):
        with open(file_name, mode='w', newline='') as csv_file:
            fieldnames = ['Valor Vivienda', 'Plazo', 'AFORO', 'Ingresos Requeridos', 'Tasa de Interes', 'Tipo de Tasa', 'CAT sin IVA', 'Pago Mensual']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.data_dictionary:
                writer.writerow(row)
