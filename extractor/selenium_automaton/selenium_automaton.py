from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import db_manager

import time
import csv

class SeleniumAutomaton:
    def __init__(self):
        self.url = ''
        self.data = []
        self.data_dictionary = []

    def connect(self, wait):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(wait)
        self.driver.get(self.url)

    def get_controls(self):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError

    def click_delay(self, element, long):
        element.click()
        time.sleep(long)

    def switch_to_frame(self, xpath):
        wait = WebDriverWait(self.driver, 100)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))

    def clean_float_number(self, number):
        return number.replace('$', '').replace(',', '').replace('%', '').replace('*', '')

    def save_data_to_db(self):
        manager = db_manager.DBManager()
        for row in self.data:
            manager.insert_subproducto(row)
        manager.close_connection()

    def export_csv(self, file_name):
        with open(file_name, mode='w', newline='') as csv_file:
            fieldnames = ['Producto', 'Valor Vivienda', 'AFORO', 'Plazo', 'Ingresos Requeridos', 'Tasa de Interes', 'Tipo de Tasa', 'CAT', 'Incluye IVA', 'Pago', 'Avaluo', 'Comision', 'Gastos Notariales', 'Desembolso Inicial']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.data_dictionary:
                writer.writerow(row) 