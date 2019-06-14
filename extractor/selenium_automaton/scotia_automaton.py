from . import selenium_automaton
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import csv

class ScotiaAutomaton(selenium_automaton.SeleniumAutomaton):
    def __init__(self):
        self.set_control_data()
        self.connect(60)
        self.get_data()
        self.driver.quit()

    def set_control_data(self):
        self.url = 'https://www.scotiabank.com.mx/personas/creditos/hipotecarios/hipotecario-credito-simulador.aspx'
        self.valor_vivienda_xpath = '//*[@id="costHouse"]'
        self.tasa_fija_xpath = '//*[@id="paymentFixed"]'
        self.tasa_creciente_xpath = '//*[@id="paymentIncreasing"]'
        self.plazo7_xpath = '//*[@id="terms7"]'
        self.plazo10_xpath = '//*[@id="terms10"]'
        self.plazo15_xpath = '//*[@id="terms15"]'
        self.plazo20_xpath = '//*[@id="terms20"]'
        self.pago_mensual_xpath = '//*[@id="calcMonthlyPayment"]'
        self.ingresos_min_xpath = '//*[@id="calcMinIncome"]'
        self.max_credito_xpath = '//*[@id="calcMinIncome"]'
        self.tasa_interes_xpath = '//*[@id="calcInterest"]'
        self.cat_xpath = '//*[@id="calcCat"]'
        self.gastos_iniciales_xpath = '//*[@id="calcExpenses"]'

    def get_controls(self):
        self.valor_vivienda = self.driver.find_element_by_xpath(self.valor_vivienda_xpath)
        self.tasa_fija = self.driver.find_element_by_xpath(self.tasa_fija_xpath)
        self.tasa_creciente = self.driver.find_element_by_xpath(self.tasa_creciente_xpath)
        self.plazo7 = self.driver.find_element_by_xpath(self.plazo7_xpath)
        self.plazo10 = self.driver.find_element_by_xpath(self.plazo10_xpath)
        self.plazo15 = self.driver.find_element_by_xpath(self.plazo15_xpath)
        self.plazo20 = self.driver.find_element_by_xpath(self.plazo20_xpath)
        self.tasas = [self.tasa_fija, self.tasa_creciente]
        self.plazos = [self.plazo7, self.plazo10, self.plazo15, self.plazo20]
        self.cat = self.driver.find_element_by_xpath(self.cat_xpath)
        self.max_credito = self.driver.find_element_by_xpath(self.max_credito_xpath)
        self.ingresos_min = self.driver.find_element_by_xpath(self.ingresos_min_xpath)
        self.tasa_interes = self.driver.find_element_by_xpath(self.tasa_interes_xpath)
        self.pago_mensual = self.driver.find_element_by_xpath(self.pago_mensual_xpath)

    def get_data(self):
        self.get_controls()
        self.data_dictionary = []
        self.subproducto_id = 1
        for tasa in self.tasas:
            for plazo in self.plazos:
                if tasa == self.tasa_creciente and plazo == self.plazo7:
                    continue
                else:
                    for valor in range(4, 16):
                        valor_vivienda_value = str(valor) + '0'*5
                        self.valor_vivienda.send_keys(Keys.BACK_SPACE*15, valor_vivienda_value)
                        time.sleep(1)
                        tasa.click()
                        plazo.click()
                        time.sleep(1)
                        max_credito_float = float(self.max_credito.text.replace(',', '').replace('.', '').replace('$ ', ''))
                        valor_vivienda_float = float(valor_vivienda_value)
                        self.data_dictionary.append({
                            'Subproducto': self.subproducto_id,
                            'Producto': 'Compra tu Casa',
                            'Valor Vivienda': valor_vivienda_value,
                            'AFORO': max_credito_float/valor_vivienda_float*100,
                            'Plazo': plazo.text,
                            'Ingresos Requeridos': self.ingresos_min.text,
                            'Tasa de Interes': self.tasa_interes.text,
                            'Tipo de Tasa': tasa.text,
                            'CAT sin IVA': self.cat.text,
                            'Pago': self.pago_mensual.text,
                            'Frecuencia de Pago': 'Mensual'
                        })
                        self.subproducto_id += 1
        print(self.data_dictionary[:10])
        self.export_csv('scotia.csv')