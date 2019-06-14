from . import selenium_automaton
from selenium.webdriver.support.ui import Select
import time
import csv

class ScotiaAutomaton(selenium_automaton.SeleniumAutomaton):
    def __init__(self):
        self.set_control_data()
        self.get_data()
        #self.driver.quit()

    def set_control_data(self):
        pass

    def get_data(self):
        pass

    def export_csv(self, file_name):
        with open(file_name, mode='w', newline='') as csv_file:
            fieldnames = ['Subproducto', 'Producto', 'Valor Vivienda', 'AFORO', 'Plazo', 'Ingresos Requeridos', 'Tasa de Interes', 'Tipo de Tasa', 'CAT sin IVA', 'Pago', 'Frecuencia de Pago']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.data_dictionary:
                writer.writerow(row)