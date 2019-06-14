from . import selenium_automaton

class BanregioAutomaton(selenium_automaton.SeleniumAutomaton):
    def __init__(self):
        self.set_control_data()
        self.connect(10)
        self.get_data()
        self.driver.quit()

    def set_control_data(self):
        self.url = 'https://www.banregio.com/cot_nueva.php'
        self.submit_xpath = '/html/body/section[2]/div[2]/div[2]/div/div[1]/div/div/form/div[7]/div[2]/input'
        self.tipos_pago_xpath = '/html/body/section[2]/div[2]/div[2]/div/div[1]/div/div/form/div[1]/div[1]'
        self.valor_xpath = '//*[@id="Valor"]'
        self.ingresos = '//*[@id="Sueldo"]'

    def get_data(self):
        self.get_controls()
        self.get_productos()

    def get_controls(self):
        pass

    def get_productos(self):
        pass