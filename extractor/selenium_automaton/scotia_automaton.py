from . import selenium_automaton
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import csv

class ScotiaAutomaton(selenium_automaton.SeleniumAutomaton):

    id_productos = (13, ) #CREDIRESIDENCIAL

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
        self.max_credito_xpath = '//*[@id="calcMaxCredit"]'
        self.tasa_interes_xpath = '//*[@id="calcInterest"]'
        self.cat_xpath = '//*[@id="calcCat"]'
        self.avaluo_xpath = '//*[@id="calcValueHouse"]'
        self.comision_por_apertura_xpath = '//*[@id="calcCommission"]'
        self.gastos_notariales_xpath = '//*[@id="calcNotary"]'
        self.desembolso_inicial_xpath = '//*[@id="calcExpenses"]'

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
        self.plazos_meses = [84, 120, 180, 240]
        self.cat = self.driver.find_element_by_xpath(self.cat_xpath)
        self.max_credito = self.driver.find_element_by_xpath(self.max_credito_xpath)
        self.ingresos_min = self.driver.find_element_by_xpath(self.ingresos_min_xpath)
        self.tasa_interes = self.driver.find_element_by_xpath(self.tasa_interes_xpath)
        self.pago_mensual = self.driver.find_element_by_xpath(self.pago_mensual_xpath)
        self.avaluo = self.driver.find_element_by_xpath(self.avaluo_xpath)
        self.comision_por_apertura = self.driver.find_element_by_xpath(self.comision_por_apertura_xpath)
        self.gastos_notariales = self.driver.find_element_by_xpath(self.gastos_notariales_xpath)
        self.desembolso_inicial = self.driver.find_element_by_xpath(self.desembolso_inicial_xpath)

    def get_data(self):
        self.get_controls()
        self.data = []
        for tasa in self.tasas:
            for ix_plazo, plazo in enumerate(self.plazos):
                if tasa == self.tasa_creciente and plazo == self.plazo7:
                    continue
                else:
                    for valor in range(4, 21):
                        self.get_values(tasa, ix_plazo, plazo, valor)
                    for valor in range(25, 105, 5):
                        self.get_values(tasa, ix_plazo, plazo, valor)
        self.save_data_to_db()

    def get_values(self, tasa, ix_plazo, plazo, valor):
        valor_vivienda_value = str(valor) + '0'*5
        self.valor_vivienda.send_keys(Keys.BACK_SPACE*15, valor_vivienda_value)
        time.sleep(1)
        tasa.click()
        plazo.click()
        time.sleep(1)
        max_credito_float = float(self.max_credito.text.replace(',', '').replace('$ ', ''))
        valor_vivienda_float = float(valor_vivienda_value)
        aforo = max_credito_float/valor_vivienda_float*100
        self.data.append((
            self.id_productos[0],
            valor_vivienda_value,
            aforo,
            self.plazos_meses[ix_plazo],
            self.clean_float_number(self.ingresos_min.text),
            self.clean_float_number(self.tasa_interes.text),
            int(tasa.text == 'Valora'),
            self.clean_float_number(self.cat.text),
            0,
            self.clean_float_number(self.pago_mensual.text),
            self.clean_float_number(self.avaluo.text),
            self.clean_float_number(self.comision_por_apertura.text),
            self.clean_float_number(self.gastos_notariales.text),
            self.clean_float_number(self.desembolso_inicial.text),
        ))
