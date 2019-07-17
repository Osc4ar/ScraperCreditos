from . import banregio_automaton as banregio
from selenium.webdriver.support.ui import Select
import time

class BanregioGeneral(banregio.BanregioAutomaton):
    def __init__(self, url, min, max):
        self.new_url = url
        self.min = min
        self.max = max
        self.is_second_type = 'cot_term.php' in self.new_url or 'mejora' in self.new_url
        super().__init__()

    def set_control_data(self):
        super().set_control_data()
        if self.is_second_type:
            self.submit_xpath = '/html/body/section[2]/div[2]/div[2]/div/div[1]/div/div/form/div[6]/div[2]/input'
        self.url = self.new_url

    def get_data(self):
        self.data_dictionary = []
        self.subproducto_id = 1
        for value in range(self.min, 21):
            self.send_values(value)
            self.subproducto_id += 1
        for value in range(25, self.max+5, 5):
            self.send_values(value)
            self.subproducto_id += 1
        self.export_csv(f'banregio_{self.url[29:33]}.csv')

    def get_controls(self):
        self.valor = self.driver.find_element_by_xpath(self.valor_xpath)
        self.ingresos = self.driver.find_element_by_xpath(self.ingresos_xpath)
        self.submit = self.driver.find_element_by_xpath(self.submit_xpath)
        self.select_seguro = Select(self.driver.find_element_by_xpath(self.select_seguro_xpath))
        self.select_plazos = Select(self.driver.find_element_by_xpath(self.select_plazos_xpath))
        self.select_financiamiento = Select(self.driver.find_element_by_xpath(self.select_financiamiento_xpath))
        if not self.is_second_type:
            self.select_estado = Select(self.driver.find_element_by_xpath(self.select_estado_xpath))

    def send_values(self, value):
        for plazo in [4, 9, 19]:
            self.perform_actions(value, plazo)

    def perform_actions(self, value, plazo):
        time.sleep(2)
        self.get_controls()
        self.select_seguro.options[0].click()
        self.select_plazos.options[plazo].click()
        self.valor.clear()
        self.valor.send_keys(str(value) + '0'*5)
        self.select_financiamiento.options[4].click()
        if not self.is_second_type:
            self.select_estado.options[9].click()
        self.ingresos.clear()
        self.ingresos.send_keys('1'+'0'*5)
        self.submit.click()
        self.extract_data()