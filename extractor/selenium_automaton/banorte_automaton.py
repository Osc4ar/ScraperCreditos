from . import selenium_automaton
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

class BanorteAutomaton(selenium_automaton.SeleniumAutomaton):
    def __init__(self):
        self.plazos_por_tipo_tasa = [2, 4]
        self.set_control_data()
        self.connect(60)
        self.get_data()
        self.driver.quit()

    def set_control_data(self):
        self.dialog_count = 1
        self.url = 'https://www.banorte.com/cms/banorte/originacion/hipoteca/#!/start'
        self.start_vvivienda_xpath = '//*[@id="bnte-container-forms"]/form/div/div[1]/input'
        self.start_cotizar_xpath = '//*[@id="bnte-container-forms"]/form/div/div[3]/button'
        self.detalle_xpath = '//*[@id="bnte-container"]/div[2]/div/div[1]/div[3]/div[3]/div[1]/button'
        self.ingresos_min_xpath = '//*[@id="bnte-container"]/div[2]/div/div[1]/div[3]/div[2]/div/strong'
        self.pago_mensual_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/div[2]/div[1]/strong'
        self.cat_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/div[2]/div[3]/strong'
        self.pago_inicial_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/div[2]/div[7]/strong'
        self.enganche_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/div[2]/div[10]/strong'
        self.tasa_interes_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/div[2]/div[2]/strong'
        self.cerrar_detalle_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/button'
        self.editar_xpath = '//*[@id="bnte-container"]/div[1]/div/div[2]/div[3]/span[2]'
        self.destinos_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/form/div[1]/select'
        self.valor_vivienda_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/form/div[6]/input'
        self.aforo_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/form/div[8]/span'
        self.contenedor_plazos_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/form/div[3]/div/div[3]'
        self.actualizar_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/form/div[11]/div/button'
        self.contenedor_tipo_tasas_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/form/div[2]/div/div[3]'

    def get_data(self):
        self.get_controls_start()
        self.move_to_simulador()
        self.data_dictionary = []
        self.subproducto_id = 1
        for destino in range(7):
            for tipo_tasa in range(2):
                rango_plazo = 2 if tipo_tasa == 0 else 4
                for plazo in range(rango_plazo): #rango plazo
                    rango_valor = range(4, 16)
                    if destino == 3 or destino == 4:
                        rango_valor = range(5, 17)
                    elif destino == 5:
                        rango_valor = range(8, 20)
                    for valor in rango_valor: #4, 6
                        self.update_value(valor, plazo, tipo_tasa, destino)
                        self.get_detalle()
                        self.subproducto_id += 1
                        if self.subproducto_id % 5 == 0:
                            self.driver.get(self.url)
                            time.sleep(2)
                            self.get_controls_start()
                            self.move_to_simulador()

        """for i in range(20, 165, 5):
            self.update_value(i)
            self.get_detalle()"""
        self.export_csv('banorte.csv')

    def get_controls_start(self):
        self.start_vvivienda = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, self.start_vvivienda_xpath)))
        self.start_cotizar = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, self.start_cotizar_xpath)))

    def move_to_simulador(self):
        self.start_vvivienda.clear()
        self.start_vvivienda.send_keys('4'+'0'*7)
        time.sleep(1)
        self.click_delay(self.start_cotizar, 5)

    def get_detalle(self):
        wait = True
        while wait:
            try:
                self.ingresos_min = self.get_data_by_xpath(self.ingresos_min_xpath)
                ingresos_min_val = self.ingresos_min.text
                self.detalle = self.get_button_by_xpath(self.detalle_xpath)
                self.detalle.click()
                self.pago_mensual_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/div[2]/div[1]/strong'
                self.cat_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/div[2]/div[3]/strong'
                self.tasa_interes_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/div[2]/div[2]/strong'
                self.cerrar_detalle_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/button'
                self.pago_mensual = self.get_data_by_xpath(self.pago_mensual_xpath)
                self.cat = self.get_data_by_xpath(self.cat_xpath)
                self.tasa_interes = self.get_data_by_xpath(self.tasa_interes_xpath)
                print(f'Pago: {self.pago_mensual.text}\tCAT: {self.cat.text}\tInteres: {self.tasa_interes.text}\tIngresos: {ingresos_min_val}')
                self.data_dictionary.append({
                    'Subproducto': self.subproducto_id,
                    'Producto': self.producto,
                    'Valor Vivienda': self.valor_vivienda_value,
                    'AFORO': self.aforo_value,
                    'Plazo': self.plazo_value,
                    'Ingresos Requeridos': ingresos_min_val,
                    'Tasa de Interes': self.tasa_interes.text.replace('*', ''),
                    'Tipo de Tasa': self.tipo_tasa,
                    'CAT sin IVA': self.cat.text,
                    'Pago': self.pago_mensual.text.split('\n')[0],
                    'Frecuencia de Pago': 'Mensual'
                })
                self.cerrar_detalle = self.get_button_by_xpath(self.cerrar_detalle_xpath)
                time.sleep(1)
                self.cerrar_detalle.click()
                self.dialog_count += 1
                time.sleep(1)
                wait = False
            except:
                wait = True
                time.sleep(5)

    def update_value(self, valor, plazo, tipo_tasa, destino):
        print(f'valor: {valor}\tplazo: {plazo}\ttipo_tasa: {tipo_tasa}\tdestino: {destino}')
        time.sleep(1)
        self.editar = self.get_button_by_xpath(self.editar_xpath)
        self.editar.click()
        time.sleep(3)
        self.contenedor_tipo_tasas_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/form/div[2]/div/div[3]'
        self.contenedor_tipo_tasas = self.driver.find_element_by_xpath(self.contenedor_tipo_tasas_xpath)
        self.tipo_tasas = self.contenedor_tipo_tasas.find_elements_by_tag_name('label')
        self.tipo_tasas[tipo_tasa].click()
        self.tipo_tasa = 'Fija' if tipo_tasa == 1 else 'Variable'
        time.sleep(1)
        self.contenedor_plazos_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/form/div[3]/div/div[3]'
        self.contenedor_plazos = self.driver.find_element_by_xpath(self.contenedor_plazos_xpath)
        self.plazos = self.contenedor_plazos.find_elements_by_tag_name('label')
        self.plazos[plazo].click()
        self.plazo_value = self.plazos[plazo].text
        time.sleep(1)
        self.valor_vivienda_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/form/div[{5+tipo_tasa}]/input'
        self.valor_vivienda = self.driver.find_element_by_xpath(self.valor_vivienda_xpath)
        self.valor_vivienda.clear()
        self.valor_vivienda.send_keys(str(valor)+'0'*7)
        self.valor_vivienda_value = '$' + str(valor)+'0'*7
        time.sleep(1)
        self.destinos_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/form/div[1]/select'
        self.destinos = Select(self.driver.find_element_by_xpath(self.destinos_xpath))
        self.destinos.options[destino].click()
        self.producto = self.tipo_tasas[tipo_tasa].text + ' - ' + self.destinos.options[destino].text
        time.sleep(1)
        self.aforo_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/form/div[{7+tipo_tasa}]/span'
        self.aforo_element = self.driver.find_element_by_xpath(self.aforo_xpath)
        self.aforo_value = self.aforo_element.text
        self.actualizar_xpath = f'//*[@id="ngdialog{self.dialog_count}"]/div[2]/div[2]/form/div[{10+tipo_tasa if destino != 1 else 12+tipo_tasa}]/div/button'
        self.actualizar = self.driver.find_element_by_xpath(self.actualizar_xpath)
        self.actualizar.click()
        self.dialog_count += 1
        time.sleep(11)

    def get_button_by_xpath(self, xpath):
        return self.get_element_with_wait(xpath, EC.element_to_be_clickable)

    def get_data_by_xpath(self, xpath):
        return self.get_element_with_wait(xpath, EC.presence_of_element_located)

    def get_element_with_wait(self, xpath, condition):
        return WebDriverWait(self.driver, 60).until(condition((By.XPATH, xpath)))